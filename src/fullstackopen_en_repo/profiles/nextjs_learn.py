from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from .config_profile import ConfigSiteProfile, sanitize_segment

COURSE_PREFIX = "/learn"
BASE_DOMAIN = "nextjs.org"
INTERNAL_RE = re.compile(r"^https?://(?:www\.)?nextjs\.org/learn")

CONFIG = {
    "id": "nextjs-learn",
    "domains": [BASE_DOMAIN, f"www.{BASE_DOMAIN}"],
    "entrypoints": ["https://nextjs.org/learn"],
    "default_max_depth": 5,
    "scope": {
        "allow": [r"^/learn(/.*)?$"],
        "strip_prefix": COURSE_PREFIX,
        "canonical_host": BASE_DOMAIN,
        "canonical_scheme": "https",
        "strip_query": True,
        "strip_fragment": True,
        "canonicalize_trailing_slash": True,
    },
    "content": {
        "keep": ["main", "article"],
        "remove": ["header", "nav", "footer"],
    },
    "output": {
        "site_dir": "nextjs-learn",
        "root_index": "index.md",
        "section_index": "index.md",
        "leaf_extension": ".md",
    },
}


class NextjsLearnProfile(ConfigSiteProfile):
    """SiteProfile implementation for https://nextjs.org/learn."""

    def __init__(self, output_root: Path):
        super().__init__(CONFIG, output_root)

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        scheme = "https"
        host = BASE_DOMAIN
        path = parsed.path or COURSE_PREFIX
        if path.rstrip("/") == COURSE_PREFIX:
            path = COURSE_PREFIX
        elif path.endswith("/"):
            path = path.rstrip("/")
        if not path.startswith(COURSE_PREFIX):
            path = COURSE_PREFIX
        return urlunparse((scheme, host, path, "", "", ""))

    def in_scope(self, url: str) -> bool:
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower()
        if host.startswith("www."):
            host = host[4:]
        if host != BASE_DOMAIN:
            return False
        path = parsed.path or "/"
        if not (path == COURSE_PREFIX or path.startswith(COURSE_PREFIX + "/")):
            return False
        return super().in_scope(url)

    def derive_output_path(self, url: str, *, title: str | None = None) -> Path:
        normalized = self.normalize_url(url)
        path = urlparse(normalized).path or COURSE_PREFIX
        segments = [
            sanitize_segment(seg)
            for seg in path[len(COURSE_PREFIX) :].split("/")
            if seg
        ]
        base = self.output_root / self.id
        if not segments:
            return base / "index.md"
        if len(segments) == 1:
            return base / segments[0] / "index.md"
        return base.joinpath(*segments[:-1], f"{segments[-1]}.md")

    def is_internal_link(self, href: str) -> bool:
        if href.startswith("/"):
            return href.startswith(COURSE_PREFIX)
        return bool(INTERNAL_RE.match(href))


__all__ = ["NextjsLearnProfile"]
