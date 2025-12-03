from __future__ import annotations

from pathlib import Path
from typing import Literal

import typer
from rich import print

from .indexing import write_index
from .link_rewriter import rewrite_markdown_links
from .markdown_utils import split_frontmatter
from .profiles import load_profile

APP = typer.Typer(add_completion=False)
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"
LinkRewriteMode = Literal["none", "local"]


@APP.command()
def main(
    site: str = typer.Option(
        "fullstackopen", "--site", help="Site profile id to postprocess"
    ),
    rewrite_links: LinkRewriteMode = typer.Option(
        "none",
        "--rewrite-links",
        case_sensitive=False,
        help="Rewrite internal links after crawl",
    ),
):
    profile = load_profile(site, output_root=DATA_DIR)
    rewritten = 0

    for path in profile.output_root.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        meta, body, front = split_frontmatter(text)
        source_url = meta.get("source_url")
        if not source_url:
            continue
        canonical_source = profile.normalize_url(source_url)
        if not profile.in_scope(canonical_source):
            continue
        new_body = body
        if rewrite_links == "local":
            new_body = rewrite_markdown_links(
                body,
                mode=rewrite_links,
                profile=profile,
                from_url=canonical_source,
            )
        if new_body != body:
            prefix = front or ""
            path.write_text(f"{prefix}{new_body}", encoding="utf-8")
            rewritten += 1

    write_index(profile.output_root, ROOT / "index.json")
    print({"rewritten": rewritten, "site": profile.id})


if __name__ == "__main__":
    APP()
