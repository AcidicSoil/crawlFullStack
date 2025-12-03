from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlparse, urlunparse

from ..utils_slug import numbered
from .base import SiteProfile

DOMAIN = "fullstackopen.com"
PATH_PREFIX = "/en"
PART_RE = re.compile(
    r"^https?://(?:www\.)?fullstackopen\.com/en/part\d+(?:/[a-z0-9_\-]+)*/?$",
    re.I,
)
SKIP_QUERY_PARAMS = ["utm_", "gclid", "fbclid", "ref", "share"]
DENY_REGEX = [
    re.compile(r".*\?(.*=){5,}.*"),
    re.compile(r"/en/.*calendar.*"),
    re.compile(r"^/(?!en/)"),
]
ALLOW_REGEX = [re.compile(r"^/en/.*")]
CONTENT_KEEP = ["main", "article", "#__next"]
CONTENT_DROP = [
    "nav",
    "footer",
    "aside",
    "script",
    "style",
    '[role="navigation"]',
    '[aria-label="breadcrumbs"]',
]
DEFAULT_SEEDS = ["https://fullstackopen.com/en/"]


class FullstackOpenProfile(SiteProfile):
    """Backward-compat mapping for the original Fullstack Open crawler."""

    asset_subdir = "assets"

    def __init__(self, output_root: Path):
        super().__init__(output_root)
        self._seeds = DEFAULT_SEEDS

    @property
    def id(self) -> str:
        return "fullstackopen"

    @property
    def domains(self) -> list[str]:
        return [DOMAIN, f"www.{DOMAIN}"]

    @property
    def entrypoints(self) -> list[str]:
        return list(self._seeds)

    @property
    def default_max_depth(self) -> int:
        return 3

    @property
    def content_selectors(self) -> list[str]:
        return CONTENT_KEEP

    @property
    def remove_selectors(self) -> list[str]:
        return CONTENT_DROP

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        scheme = "https"
        host = DOMAIN
        path = parsed.path or PATH_PREFIX
        if path.endswith("/") and path != PATH_PREFIX:
            path = path.rstrip("/")
        query = ""
        fragment = ""
        return urlunparse((scheme, host, path, "", query, fragment))

    def _path_allowed(self, path: str) -> bool:
        if path.rstrip("/") == PATH_PREFIX.rstrip("/"):
            return True
        if any(rx.search(path) for rx in DENY_REGEX):
            return False
        return any(rx.search(path) for rx in ALLOW_REGEX)

    def in_scope(self, url: str) -> bool:
        parsed_orig = urlparse(url)
        host = (parsed_orig.hostname or "").lower()
        if host and host not in (DOMAIN, f"www.{DOMAIN}"):
            return False
        normalized = self.normalize_url(url)
        parsed = urlparse(normalized)
        if parsed.hostname not in self.domains:
            return False
        path = parsed.path or "/"
        if not path.startswith(PATH_PREFIX):
            return False
        qs = parsed_orig.query or ""
        for param in SKIP_QUERY_PARAMS:
            if param in qs:
                return False
        return self._path_allowed(path)

    def should_enqueue(self, url: str) -> bool:
        normalized = self.normalize_url(url)
        return bool(PART_RE.match(normalized))

    def derive_output_path(self, url: str, *, title: str | None = None) -> Path:
        normalized = self.normalize_url(url)
        path = re.sub(r"https?://[^/]+", "", normalized)
        parts = [p for p in path.strip("/").split("/") if p]
        base = self.output_root
        if len(parts) <= 1:
            subdir = base / "course"
            fname = "00-index.md"
        else:
            subdir = base / parts[1]
            fname = f"{numbered(title or parts[-1], 1)}.md"
        return subdir / fname

    def is_internal_link(self, href: str) -> bool:
        if href.startswith("/"):
            return href.startswith(PATH_PREFIX)
        return super().is_internal_link(href)


__all__ = ["FullstackOpenProfile"]
