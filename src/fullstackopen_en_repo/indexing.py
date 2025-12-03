from __future__ import annotations

import json
from pathlib import Path
from typing import Dict

from .markdown_utils import split_frontmatter


def build_index_map(data_dir: Path) -> Dict[str, dict[str, str]]:
    index: Dict[str, dict[str, str]] = {}
    for path in data_dir.rglob("*.md"):
        rel = path.relative_to(data_dir).as_posix()
        meta, _, _ = split_frontmatter(path.read_text(encoding="utf-8"))
        index[rel] = {"title": meta.get("title", path.stem), "path": rel}
    return index


def write_index(data_dir: Path, output_path: Path) -> None:
    index = build_index_map(data_dir)
    output_path.write_text(
        json.dumps(index, ensure_ascii=False, indent=2), encoding="utf-8"
    )


__all__ = ["build_index_map", "write_index"]
