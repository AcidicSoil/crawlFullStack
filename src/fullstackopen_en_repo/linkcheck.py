from __future__ import annotations

from pathlib import Path

import typer
from rich import print

from .link_rewriter import LINK_RE
from .markdown_utils import split_frontmatter
from .profiles import load_profile

APP = typer.Typer(add_completion=False)
ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "data"


@APP.command()
def main(
    site: str = typer.Option(
        "fullstackopen", "--site", help="Site profile id to check"
    ),
):
    profile = load_profile(site, output_root=DATA_DIR)
    broken = 0

    for path in profile.output_root.rglob("*.md"):
        text = path.read_text(encoding="utf-8", errors="ignore")
        meta, body, _ = split_frontmatter(text)
        source_url = meta.get("source_url")
        if not source_url:
            continue
        base_url = profile.normalize_url(source_url)
        if not profile.in_scope(base_url):
            continue

        for match in LINK_RE.finditer(body):
            href = match.group(2)
            if href.startswith("mailto:") or href.startswith("tel:"):
                continue
            target_path: Path | None
            if href.startswith("http") or href.startswith("/"):
                absolute = profile.normalize_url(profile.to_absolute(href, base_url))
                if not profile.is_internal_link(absolute):
                    continue
                target_path = profile.derive_output_path(absolute)
            else:
                target_path = (path.parent / href).resolve()
            if not target_path.exists():
                print(f"[red]BROKEN[/red] {path.relative_to(ROOT)} -> {href}")
                broken += 1

    if broken:
        print(f"[red]broken links: {broken}[/red]")
        raise typer.Exit(code=1)
    print("[green]linkcheck ok[/green]")


if __name__ == "__main__":
    APP()
