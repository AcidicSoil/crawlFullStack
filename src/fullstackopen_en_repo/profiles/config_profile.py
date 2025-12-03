from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, cast
from urllib.parse import unquote, urlparse, urlunparse

from .base import SiteProfile

SAFE_FILE_CHARS = re.compile(r"[^-_.A-Za-z0-9]")


def sanitize_segment(segment: str) -> str:
    text = unquote(segment.strip()) or "index"
    return SAFE_FILE_CHARS.sub("-", text)


def _to_str_list(value: Any) -> list[str]:
    if isinstance(value, (list, tuple)):
        return [str(v) for v in value]
    if value:
        return [str(value)]
    return []


@dataclass
class ConfigSiteProfile(SiteProfile):
    """Profile defined by a config dictionary (YAML/JSON)."""

    _config: dict[str, Any]

    def __init__(self, config: dict[str, Any], output_root: Path):
        super().__init__(output_root)
        self._config = dict(config)
        scope = config.get("scope", {})
        self._allow = [re.compile(p) for p in scope.get("allow", [])]
        self._deny = [re.compile(p) for p in scope.get("deny", [])]
        self._strip_query = scope.get("strip_query", True)
        self._strip_fragment = scope.get("strip_fragment", True)
        host = scope.get("canonical_host")
        self._canonical_host: str | None = str(host) if host else None
        scheme_val = scope.get("canonical_scheme", "https")
        self._canonical_scheme: str = str(scheme_val) if scheme_val else "https"
        self._strip_prefix: str = str(scope.get("strip_prefix", ""))
        self._canonicalize_trailing_slash = scope.get(
            "canonicalize_trailing_slash", True
        )
        output_cfg = config.get("output", {}) or {}
        self._site_dir: str = str(output_cfg.get("site_dir", config.get("id", "site")))
        self._root_index: str = str(output_cfg.get("root_index", "index.md"))
        self._section_index: str = str(output_cfg.get("section_index", "index.md"))
        self._leaf_extension: str = str(output_cfg.get("leaf_extension", ".md"))
        content_cfg = config.get("content", {}) or {}
        self._content_keep: list[str] = _to_str_list(content_cfg.get("keep", []))
        self._content_remove: list[str] = _to_str_list(content_cfg.get("remove", []))

    @property
    def id(self) -> str:
        return cast(str, self._config["id"])

    @property
    def domains(self) -> list[str]:
        return _to_str_list(self._config.get("domains", []))

    @property
    def entrypoints(self) -> list[str]:
        return _to_str_list(self._config.get("entrypoints", []))

    @property
    def default_max_depth(self) -> int:
        return int(self._config.get("default_max_depth", 3))

    @property
    def content_selectors(self) -> list[str]:
        return list(self._content_keep)

    @property
    def remove_selectors(self) -> list[str]:
        return list(self._content_remove)

    def normalize_url(self, url: str) -> str:
        parsed = urlparse(url)
        scheme = self._canonical_scheme or parsed.scheme or "https"
        host = parsed.hostname or ""
        if self._canonical_host:
            host = self._canonical_host
        path = parsed.path or "/"
        if self._canonicalize_trailing_slash and path.endswith("/") and path != "/":
            path = path.rstrip("/")
        query = "" if self._strip_query else parsed.query
        fragment = "" if self._strip_fragment else parsed.fragment
        return urlunparse((scheme, host, path or "/", "", query, fragment))

    def _path_in_scope(self, path: str) -> bool:
        if self._allow and not any(rx.search(path) for rx in self._allow):
            return False
        if any(rx.search(path) for rx in self._deny):
            return False
        return True

    def in_scope(self, url: str) -> bool:
        normalized = self.normalize_url(url)
        parsed = urlparse(normalized)
        if parsed.hostname not in self.domains:
            return False
        return self._path_in_scope(parsed.path or "/")

    def derive_output_path(self, url: str, *, title: str | None = None) -> Path:
        normalized = self.normalize_url(url)
        parsed = urlparse(normalized)
        path = parsed.path or "/"
        rel = path
        prefix = self._strip_prefix or ""
        if prefix and rel.startswith(prefix):
            rel = rel[len(prefix) :]
        segments = [sanitize_segment(seg) for seg in rel.split("/") if seg]
        base = self.output_root / self._site_dir
        if not segments:
            return base / self._root_index
        if len(segments) == 1:
            return (base / segments[0]) / self._section_index
        return base.joinpath(*segments[:-1], f"{segments[-1]}{self._leaf_extension}")

    def is_internal_link(self, href: str) -> bool:
        if href.startswith("/"):
            return self._path_in_scope(href)
        return super().is_internal_link(href)


__all__ = ["ConfigSiteProfile"]
