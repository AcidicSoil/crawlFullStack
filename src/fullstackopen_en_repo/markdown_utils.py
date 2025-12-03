from __future__ import annotations

import json
from typing import Any, Tuple

import yaml


def split_frontmatter(text: str) -> Tuple[dict[str, Any], str, str | None]:
    if not text.startswith("---"):
        return {}, text, None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text, None
    raw_meta = parts[1]
    body = parts[2]
    try:
        meta = json.loads(raw_meta.strip())
    except Exception:
        try:
            loaded = yaml.safe_load(raw_meta)
        except Exception:
            loaded = None
        meta = loaded if isinstance(loaded, dict) else {}
    front_block = f"---{raw_meta}---"
    return meta, body, front_block


__all__ = ["split_frontmatter"]
