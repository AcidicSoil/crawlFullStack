from __future__ import annotations
import asyncio
import hashlib
import json
import os
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Set, Tuple

import typer
from bs4 import BeautifulSoup
from rich import print
from rich.progress import Progress

from crawl4ai import AsyncWebCrawler
from crawl4ai.async_configs import BrowserConfig, CrawlerRunConfig
from crawl4ai.markdown_generation_strategy import DefaultMarkdownGenerator

import tomli
import requests

from .utils_slug import slug, numbered, path_from_parts

APP = typer.Typer(add_completion=False)
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
ASSET_DIR = ROOT / "assets"
LOG_DIR = ROOT / "logs"
CONFIG_PATH = ROOT / "crawl.config.yml"
SEEDS_PATH = ROOT / "seeds.txt"

UA_DEFAULT = "Mozilla/5.0 (compatible; FullstackOpenMirror/1.0; +https://example.invalid/personal-use)"
DOMAIN = "fullstackopen.com"
PATH_PREFIX = "/en/"

# --------- helpers ---------
@dataclass
class CrawlItem:
    url: str
    depth: int


def load_yaml(path: Path) -> dict:
    # allow YAML subset via tomli (valid for simple key: value)
    with open(path, "rb") as f:
        return tomli.loads(f.read().decode("utf-8"))


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return load_yaml(CONFIG_PATH)


def allowed_url(url: str, cfg: dict) -> bool:
    if not url.startswith(f"https://{DOMAIN}") and not url.startswith(f"http://{DOMAIN}"):
        return False
    path = re.sub(r"https?://[^/]+", "", url)
    if not path.startswith(PATH_PREFIX):
        return False
    for rx in cfg.get("deny_path_regex", []):
        if re.search(rx, path):
            return False
    if cfg.get("allow_path_regex"):
        ok = any(re.search(rx, path) for rx in cfg["allow_path_regex"])
        if not ok:
            return False
    qpos = url.find("?")
    if qpos != -1:
        qs = url[qpos + 1 :]
        if qs.count("=") >= 5:
            return False
        for p in cfg.get("skip_query_params", []):
            if p in qs:
                return False
    return True


def canonicalize(url: str, cfg: dict) -> str:
    # strip fragments
    url = url.split("#", 1)[0]
    # normalize trailing slash
    if cfg.get("sitemap", {}).get("canonicalize_trailing_slash", True):
        if url.endswith("/"):
            url = url[:-1]
    return url


def discover_children(html: str, base_url: str, cfg: dict) -> List[str]:
    soup = BeautifulSoup(html, "lxml")
    urls = []
    for a in soup.find_all("a", href=True):
        href = a["href"].strip()
        if href.startswith("//"):
            href = "https:" + href
        elif href.startswith("/"):
            href = f"https://{DOMAIN}{href}"
        elif href.startswith("http"):
            pass
        else:
            # relative
            prefix = base_url.rsplit("/", 1)[0]
            href = f"{prefix}/{href}"
        href = canonicalize(href, cfg)
        if allowed_url(href, cfg):
            urls.append(href)
    return urls


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


# --------- core crawl ---------
async def crawl_once(url: str, browser_cfg: BrowserConfig, run_cfg: CrawlerRunConfig, save_html: bool) -> Tuple[str, str, str]:
    async with AsyncWebCrawler(config=browser_cfg) as crawler:
        result = await crawler.arun(url=url, config=run_cfg)
        if not getattr(result, "success", True):
            raise RuntimeError(f"crawl failed {url}: {result.error_message}")
        md = result.markdown or ""
        html = result.html or ""
        title = result.title or BeautifulSoup(html, "lxml").title.string if html else ""
        title = (title or "untitled").strip()
        return md, html, title


def build_run_config(cfg: dict) -> Tuple[BrowserConfig, CrawlerRunConfig]:
    ua = cfg.get("user_agent", UA_DEFAULT)
    browser = BrowserConfig(
        headless=True,
        user_agent=ua,
        verbose=False,
    )
    mdgen = DefaultMarkdownGenerator(
        options={"preserve_links": True, "code_fences": True}
    )
    run = CrawlerRunConfig(
        markdown_generator=mdgen,
        css_selector=cfg.get("content", {}).get("keep_selectors", None),
        excluded_selector=",".join(cfg.get("content", {}).get("drop_selectors", [])) or None,
        wait_until="domcontentloaded",
        page_timeout=cfg.get("timeouts", {}).get("page_ms", 60000),
        mean_delay=cfg.get("rate_limits", {}).get("mean_delay", 0.25),
        max_range=cfg.get("rate_limits", {}).get("jitter_seconds", [0.3, 1.0])[1],
        semaphore_count=min(int(cfg.get("max_concurrency", 3)), 4),
        check_robots_txt=True,
        exclude_external_links=True,
    )
    return browser, run


def derive_output_path(url: str, title: str) -> Path:
    # Map /en/partX/... to /data/partx/nn-slug.md
    path = re.sub(r"https?://[^/]+", "", url)  # /en/partX/... or /en
    parts = [p for p in path.strip("/").split("/") if p]
    if len(parts) == 1:  # /en
        subdir = DATA_DIR / "course"
        fname = "00-index.md"
    else:
        subdir = DATA_DIR / parts[1]  # part1, part2, ...
        fname = f"{numbered(title or parts[-1], 1)}.md"
    return subdir / fname


def frontmatter(title: str, source_url: str, content_md: str) -> str:
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    checksum = sha256(content_md)
    fm = {
        "title": title,
        "source_url": source_url,
        "crawl_timestamp": ts,
        "checksum": checksum,
    }
    return "---" + json.dumps(fm, ensure_ascii=False, indent=2) + "\n---"


def download_images(md: str, url: str, cfg: dict) -> Tuple[str, list[str]]:
    # Replace remote images with local /assets paths. Return updated md and list of files written.
    written = []
    def repl(m):
        alt, src = m.group(1), m.group(2)
        if src.startswith("http"):
            ext = os.path.splitext(src.split("?")[0])[1] or ".png"
            fname = sha256(src)[:16] + ext
            out = ASSET_DIR / fname
            out.parent.mkdir(parents=True, exist_ok=True)
            try:
                r = requests.get(src, timeout=20)
                if r.ok:
                    out.write_bytes(r.content)
                    written.append(str(out))
                    return f"![{alt}](../assets/{fname})"
            except Exception:
                pass
        return m.group(0)
    new_md = re.sub(r"!\\[([^\\]*)\\]\\(([^)]+)\")", repl, md)
    return new_md, written


def fix_links(md: str) -> str:
    # Convert absolute course links to relative .md paths inside /data
    def repl(m):
        text, href = m.group(1), m.group(2)
        if href.startswith(f"https://{DOMAIN}{PATH_PREFIX}"):
            rel = href.replace(f"https://{DOMAIN}", "")
            rel = rel.strip("/")
            parts = rel.split("/")
            if len(parts) >= 2:
                target = f"../{parts[1]}/01-{slug(parts[-1] or 'index')}.md"
                return f"[{text}]({target})"
        return m.group(0)
    return re.sub(r"\\[([^\\]+)\\]\\(([^)]+)\")", repl, md)


@APP.command()
def main(
    fresh: bool = typer.Option(False, "--fresh", help="Ignore cache and rewrite outputs"),
    since: str = typer.Option(None, "--since", help="Only re-crawl pages updated since date (YYYY-MM-DD)"),
    dry_run: bool = typer.Option(False, "--dry-run", help="Plan only; do not fetch or write"),
    save_html: bool = typer.Option(False, "--save-html", help="Store raw HTML next to Markdown"),
):
    cfg = load_config()
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    with open(SEEDS_PATH, "r", encoding="utf-8") as f:
        seeds = [canonicalize(line.strip(), cfg) for line in f if line.strip()]

    # BFS with depth control
    depth_limit = int(cfg.get("sitemap", {}).get("depth_limit", 3))
    queue: List[CrawlItem] = []
    seen: Set[str] = set()
    for s in sorted(seeds):
        if allowed_url(s, cfg):
            queue.append(CrawlItem(s, 0))
    browser_cfg, run_cfg = build_run_config(cfg)

    planned: List[str] = []

    while queue:
        item = queue.pop(0)
        if item.url in seen:
            continue
        seen.add(item.url)
        planned.append(item.url)

        if dry_run:
            continue

        try:
            md, html, title = asyncio.run(crawl_once(item.url, browser_cfg, run_cfg, save_html))
        except Exception as e:
            write_text(LOG_DIR / "errors.log", f"{item.url}\t{e}\n")
            continue

        # Trimming boilerplate with BeautifulSoup fallback
        soup = BeautifulSoup(html, "lxml")
        for sel in cfg.get("content", {}).get("drop_selectors", []):
            for node in soup.select(sel):
                node.decompose()
        main_sel = cfg.get("content", {}).get("keep_selectors", [])
        if main_sel:
            body_nodes = []
            for s in main_sel:
                body_nodes.extend(soup.select(s))
            html_main = "\n".join(str(n) for n in body_nodes) or html
        else:
            html_main = html

        # Use crawl4ai markdown or fallback to markdownify (already provided by crawl4ai)
        content_md = md.strip()
        if not content_md:
            content_md = ""  # as last resort leave empty

        # Images → assets
        if cfg.get("assets", {}).get("download_images", True):
            content_md, _ = download_images(content_md, item.url, cfg)

        content_md = fix_links(content_md)

        out_path = derive_output_path(item.url, title)
        body = frontmatter(title, item.url, content_md) + content_md
        if save_html:
            write_text(out_path.with_suffix(".html"), html_main)
        write_text(out_path, body)

        # enqueue children
        if item.depth < depth_limit:
            kids = discover_children(html_main, item.url, cfg)
            for u in sorted(set(kids)):
                if u not in seen and allowed_url(u, cfg):
                    queue.append(CrawlItem(u, item.depth + 1))

    # index.json
    index = {}
    for p in DATA_DIR.rglob("*.md"):
        rel = p.relative_to(DATA_DIR).as_posix()
        with open(p, "r", encoding="utf-8") as f:
            first = f.readline()
            meta = json.loads(f.read().split("---", 1)[0]) if first.strip() == "---" else {}
        index[rel] = {"title": meta.get("title", p.stem), "path": rel}
    write_text(ROOT / "index.json", json.dumps(index, ensure_ascii=False, indent=2))

    # summary
    print({
        "planned": len(planned),
        "written_md": len(list(DATA_DIR.rglob("*.md"))),
        "assets": len(list(ASSET_DIR.glob("*" ))),
    })

if __name__ == "__main__":
    APP()
