from __future__ import annotations

import re
from typing import Literal

from .profiles import SiteProfile

LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def rewrite_markdown_links(
    markdown: str,
    *,
    mode: Literal["none", "local"],
    profile: SiteProfile,
    from_url: str,
) -> str:
    """Rewrite markdown links according to the chosen mode."""

    if mode == "none":
        return markdown

    def repl(match: re.Match[str]) -> str:
        text, href = match.group(1), match.group(2)
        absolute = profile.to_absolute(href, from_url)
        if not profile.is_internal_link(absolute):
            return match.group(0)
        rel = profile.map_url_to_relpath(from_url, absolute)
        return f"[{text}]({rel})"

    return LINK_RE.sub(repl, markdown)


__all__ = ["rewrite_markdown_links"]
