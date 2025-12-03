from __future__ import annotations

import asyncio
import hashlib
import json
import os
import re
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Literal, Tuple

import requests
import typer
import yaml
from bs4 import BeautifulSoup, Tag
from crawl4ai import AsyncWebCrawler  # type: ignore[import-untyped]
from crawl4ai.async_configs import (  # type: ignore[import-untyped]
    BrowserConfig,
    CrawlerRunConfig,
)
from crawl4ai.markdown_generation_strategy import (  # type: ignore[import-untyped]
    DefaultMarkdownGenerator,
)
from rich import print

from .indexing import write_index
from .link_rewriter import rewrite_markdown_links
from .markdown_utils import split_frontmatter
from .profiles import SiteProfile, load_profile

APP = typer.Typer(add_completion=False)
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LOG_DIR = ROOT / "logs"
CONFIG_PATH = ROOT / "crawl.config.yml"

# Crawl4AI writes robots cache into ~/.crawl4ai by default. That location can be
# read-only in sandboxed environments, so redirect into the project tree unless
# the caller already set a base directory.
os.environ.setdefault("CRAWL4_AI_BASE_DIRECTORY", str(ROOT))

UA_DEFAULT = "Mozilla/5.0 (compatible; FullstackOpenMirror/1.0; +https://example.invalid/personal-use)"
LinkRewriteMode = Literal["none", "local"]
FrontmatterMode = Literal["metadata", "simple"]


@dataclass
class CrawlItem:
    url: str
    depth: int


def load_yaml(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return load_yaml(CONFIG_PATH)


def _extract_href(value: Any) -> str | None:
    if isinstance(value, str):
        return value
    return None


def discover_children(html: str, base_url: str, profile: SiteProfile) -> list[str]:
    soup = BeautifulSoup(html, "lxml")
    children: set[str] = set()
    for a in soup.select("a[href]"):
        raw = _extract_href(a.get("href"))
        if not raw:
            continue
        href = raw.strip()
        if not href or href.startswith("#"):
            continue
        absolute = profile.to_absolute(href, base_url)
        normalized = profile.normalize_url(absolute)
        if profile.should_enqueue(normalized):
            children.add(normalized)
    return sorted(children)


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def sha256(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load_existing_metadata(profile: SiteProfile) -> Dict[str, Tuple[Path, str | None]]:
    mapping: Dict[str, Tuple[Path, str | None]] = {}
    root = profile.output_root
    if not root.exists():
        return mapping
    for path in root.rglob("*.md"):
        try:
            text = path.read_text(encoding="utf-8")
        except OSError:
            continue
        meta, _, _ = split_frontmatter(text)
        source = meta.get("source_url")
        if not source:
            continue
        canonical = profile.normalize_url(str(source))
        if not profile.in_scope(canonical):
            continue
        mapping[canonical] = (path, meta.get("checksum"))
    return mapping


async def crawl_once(
    url: str,
    browser_cfg: BrowserConfig,
    run_cfg: CrawlerRunConfig,
    profile: SiteProfile,
) -> tuple[str, str, str, list[str]]:
    """Fetch one URL and extract markdown/html/children."""

    async with AsyncWebCrawler(config=browser_cfg, base_directory=str(ROOT)) as crawler:
        result = await crawler.arun(url=url, config=run_cfg)
        if not getattr(result, "success", True):
            raise RuntimeError(
                f"crawl failed {url}: {getattr(result, 'error_message', 'unknown error')}"
            )

        md_obj = result.markdown
        md = (
            getattr(md_obj, "raw_markdown", None)
            or getattr(md_obj, "fit_markdown", None)
            or md_obj
            or ""
        )
        html = result.html or ""

        title = None
        for line in md.splitlines() if isinstance(md, str) else []:
            if line.startswith("# "):
                title = line[2:].strip()
                break
        if not title:
            dom = BeautifulSoup(html, "lxml") if html else None
            title = (
                getattr(result, "title", None)
                or (dom.title.string if dom and dom.title else "")
                or "untitled"
            ).strip()

        children: set[str] = set()

        def consider(href: str | None) -> None:
            if not href:
                return
            absolute = profile.to_absolute(href, url)
            normalized = profile.normalize_url(absolute)
            if profile.should_enqueue(normalized):
                children.add(normalized)

        links = getattr(result, "links", None)
        if links and isinstance(links, dict):
            for link in links.get("internal") or []:
                consider(_extract_href(link.get("href")))

        if not children and html:
            soup = BeautifulSoup(html, "lxml")
            for a in soup.select("a[href]"):
                consider(_extract_href(a.get("href")))

        return md or "", html, title, sorted(children)


def build_run_config(
    cfg: dict, profile: SiteProfile
) -> tuple[BrowserConfig, CrawlerRunConfig]:
    ua = cfg.get("user_agent", UA_DEFAULT)
    browser = BrowserConfig(
        headless=True,
        user_agent=ua,
        verbose=False,
    )
    mdgen = DefaultMarkdownGenerator(
        options={"preserve_links": True, "code_fences": True}
    )
    def _normalize_selectors(value: Any) -> str | None:
        if not value:
            return None
        if isinstance(value, str):
            return value
        if isinstance(value, (list, tuple)):
            joined = ",".join(str(v) for v in value if v)
            return joined or None
        return None

    keep_sel = _normalize_selectors(
        profile.content_selectors or cfg.get("content", {}).get("keep_selectors")
    )
    drop_sel = _normalize_selectors(
        profile.remove_selectors or cfg.get("content", {}).get("drop_selectors", [])
    )
    run = CrawlerRunConfig(
        markdown_generator=mdgen,
        css_selector=keep_sel,
        excluded_selector=drop_sel,
        wait_until="domcontentloaded",
        page_timeout=cfg.get("timeouts", {}).get("page_ms", 60000),
        mean_delay=cfg.get("rate_limits", {}).get("mean_delay", 0.25),
        max_range=cfg.get("rate_limits", {}).get("jitter_seconds", [0.3, 1.0])[1],
        semaphore_count=min(int(cfg.get("max_concurrency", 3)), 4),
        check_robots_txt=True,
        exclude_external_links=True,
    )
    return browser, run


def frontmatter(
    title: str,
    source_url: str,
    content_md: str,
    checksum: str | None = None,
    *,
    doc_id: str = "",
    mode: FrontmatterMode = "metadata",
) -> str:
    ts = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    checksum_value = checksum or sha256(content_md)
    if mode == "simple":
        lines = [
            "---",
            f"id: {doc_id}",
            f"title: {title or ''}",
            f"source_url: {source_url}",
            f"crawl_timestamp: {ts}",
            f"checksum: {checksum_value}",
            "---",
            "",
        ]
        return "\n".join(lines)

    fm = {
        "title": title,
        "source_url": source_url,
        "crawl_timestamp": ts,
        "checksum": checksum_value,
    }
    return "---\n" + json.dumps(fm, ensure_ascii=False, indent=2) + "\n---\n"


def relative_asset_href(out_path: Path, asset_path: Path) -> str:
    rel = os.path.relpath(asset_path, out_path.parent)
    return Path(rel).as_posix()


def resolve_asset_dir(profile: SiteProfile) -> Path:
    subdir = Path(profile.asset_subdir)
    if not subdir.is_absolute():
        return ROOT / subdir
    return subdir


def download_images(md: str, out_path: Path, asset_dir: Path) -> tuple[str, list[str]]:
    written: list[str] = []
    asset_dir.mkdir(parents=True, exist_ok=True)

    def repl(match: re.Match[str]) -> str:
        alt, src = match.group(1), match.group(2)
        if not src.lower().startswith("http"):
            return match.group(0)
        ext = os.path.splitext(src.split("?")[0])[1] or ".png"
        fname = sha256(src)[:16] + ext
        out = asset_dir / fname
        try:
            resp = requests.get(src, timeout=20)
            if resp.ok:
                out.write_bytes(resp.content)
                written.append(str(out))
                href = relative_asset_href(out_path, out)
                return f"![{alt}]({href})"
        except Exception:
            pass
        return match.group(0)

    new_md = re.sub(r"!\[([^\]]*)\]\(([^)]+)\)", repl, md)
    return new_md, written


def extract_main_html(html: str, profile: SiteProfile) -> str:
    if not html:
        return ""
    soup = BeautifulSoup(html, "lxml")
    for selector in profile.remove_selectors:
        for node in soup.select(selector):
            node.decompose()
    keepers: list[Tag] = []
    for selector in profile.content_selectors:
        keepers.extend(soup.select(selector))
    if keepers:
        return "\n".join(str(node) for node in keepers)
    return html


@APP.command()
def main(
    fresh: bool = typer.Option(
        False, "--fresh", help="Ignore cache and rewrite outputs"
    ),
    since: str | None = typer.Option(
        None, "--since", help="Only re-crawl pages updated since date (YYYY-MM-DD)"
    ),
    dry_run: bool = typer.Option(
        False, "--dry-run", help="Plan only; do not fetch or write"
    ),
    save_html: bool = typer.Option(
        False, "--save-html", help="Store raw HTML next to Markdown"
    ),
    site: str = typer.Option(
        "fullstackopen", "--site", help="Site profile id to crawl"
    ),
    rewrite_links: LinkRewriteMode = typer.Option(
        "none",
        "--rewrite-links",
        case_sensitive=False,
        help="Rewrite internal links: 'local' rewrites to relative paths",
    ),
    depth_limit: int | None = typer.Option(
        None,
        "--depth-limit",
        help="Override crawl depth limit (defaults to profile setting)",
    ),
    frontmatter_template: FrontmatterMode = typer.Option(
        "metadata",
        "--frontmatter-template",
        case_sensitive=False,
        help="Frontmatter format: 'metadata' JSON (default) or 'simple' YAML id/title style",
    ),
):
    cfg = load_config()
    if fresh:
        print(
            "[yellow]--fresh flag is not implemented; continuing with existing outputs[/yellow]"
        )
    if since:
        print("[yellow]--since filter is not implemented; crawling all pages[/yellow]")
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    profile = load_profile(site, output_root=DATA_DIR)
    asset_dir = resolve_asset_dir(profile)
    asset_dir.mkdir(parents=True, exist_ok=True)
    existing_meta = load_existing_metadata(profile) if not fresh else {}
    depth_limit = depth_limit or profile.default_max_depth
    browser_cfg, run_cfg = build_run_config(cfg, profile)

    queue: list[CrawlItem] = []
    seen: set[str] = set()
    for seed in profile.start_urls:
        normalized = profile.normalize_url(seed)
        if profile.in_scope(normalized):
            queue.append(CrawlItem(normalized, 0))

    planned: list[str] = []
    skipped_existing = 0

    while queue:
        item = queue.pop(0)
        normalized = profile.normalize_url(item.url)
        if normalized in seen or not profile.in_scope(normalized):
            continue
        seen.add(normalized)
        planned.append(normalized)

        if dry_run:
            continue

        try:
            md, html, title, children = asyncio.run(
                crawl_once(normalized, browser_cfg, run_cfg, profile)
            )
        except Exception as exc:
            write_text(LOG_DIR / "errors.log", f"{normalized}\t{exc}\n")
            continue

        content_md = md.strip() if isinstance(md, str) else ""
        html_main = extract_main_html(html, profile)
        out_path = profile.derive_output_path(normalized, title=title)

        if profile.download_images and content_md:
            content_md, _ = download_images(content_md, out_path, asset_dir)

        rewritten = rewrite_markdown_links(
            content_md,
            mode=rewrite_links,
            profile=profile,
            from_url=normalized,
        )

        new_checksum = sha256(rewritten)
        if not fresh:
            existing_info = existing_meta.get(normalized)
            if existing_info and existing_info[1] == new_checksum:
                skipped_existing += 1
                continue

        rel_doc_id = ""
        try:
            rel_doc_id = out_path.relative_to(profile.output_root).as_posix()
        except ValueError:
            rel_doc_id = out_path.as_posix()

        body = (
            frontmatter(
                title,
                normalized,
                rewritten,
                checksum=new_checksum,
                doc_id=rel_doc_id,
                mode=frontmatter_template,
            )
            + rewritten
        )
        if save_html:
            write_text(out_path.with_suffix(".html"), html_main)
        write_text(out_path, body)
        existing_meta[normalized] = (out_path, new_checksum)

        if item.depth < depth_limit:
            kids = set(children)
            kids.update(discover_children(html, normalized, profile))
            for child in sorted(kids):
                if child not in seen and profile.should_enqueue(child):
                    queue.append(CrawlItem(child, item.depth + 1))

    write_index(DATA_DIR, ROOT / "index.json")

    print(
        {
            "planned": len(planned),
            "written_md": len(list(DATA_DIR.rglob("*.md"))),
            "assets": len(list(asset_dir.glob("*"))),
            "skipped_existing": skipped_existing,
        }
    )


if __name__ == "__main__":
    APP()
