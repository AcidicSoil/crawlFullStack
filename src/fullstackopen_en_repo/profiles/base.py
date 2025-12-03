from __future__ import annotations

import os
from abc import ABC, abstractmethod
from pathlib import Path
from urllib.parse import urljoin, urlparse


class SiteProfile(ABC):
    """Abstraction that encapsulates per-site crawl and output rules."""

    asset_subdir: str = "assets"
    download_images: bool = True

    def __init__(self, output_root: Path):
        self.output_root = output_root

    @property
    @abstractmethod
    def id(self) -> str:  # pragma: no cover - attribute contract
        raise NotImplementedError

    @property
    @abstractmethod
    def domains(self) -> list[str]:  # pragma: no cover - attribute contract
        raise NotImplementedError

    @property
    @abstractmethod
    def entrypoints(self) -> list[str]:  # pragma: no cover - attribute contract
        raise NotImplementedError

    @property
    def start_urls(self) -> list[str]:
        return self.entrypoints

    @property
    @abstractmethod
    def default_max_depth(self) -> int:  # pragma: no cover - attribute contract
        raise NotImplementedError

    @property
    def content_selectors(self) -> list[str]:
        return []

    @property
    def remove_selectors(self) -> list[str]:
        return []

    def normalize_url(self, url: str) -> str:
        """Return canonical absolute URL for the site."""
        return url

    @abstractmethod
    def in_scope(self, url: str) -> bool:
        """Return True when URL should be considered by the crawler."""

    def should_enqueue(self, url: str) -> bool:
        return self.in_scope(url)

    @abstractmethod
    def derive_output_path(self, url: str, *, title: str | None = None) -> Path:
        """Map an URL to a markdown path under output_root."""

    def is_internal_link(self, href: str) -> bool:
        parsed = urlparse(href)
        if not parsed.netloc:  # root-relative path
            return parsed.path.startswith("/")
        return parsed.hostname in self.domains

    def to_absolute(self, href: str, from_url: str) -> str:
        if href.startswith("mailto:") or href.startswith("tel:"):
            return href
        if href.startswith("//"):
            parsed_from = urlparse(from_url)
            return f"{parsed_from.scheme}:{href}"
        return urljoin(from_url, href)

    def map_url_to_relpath(self, from_url: str, target_url: str) -> str:
        source = self.derive_output_path(from_url)
        target = self.derive_output_path(target_url)
        rel = os.path.relpath(target, source.parent)
        return Path(rel).as_posix()


__all__ = ["SiteProfile"]
