from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import yaml

from .base import SiteProfile
from .config_profile import ConfigSiteProfile
from .fullstackopen import FullstackOpenProfile
from .nextjs_learn import NextjsLearnProfile

PROJECT_ROOT = Path(__file__).resolve().parents[3]
PROFILES_DIR = PROJECT_ROOT / "profiles"


def _load_profile_config(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    if path.suffix.lower() in {".json"}:
        return cast(dict[str, Any], json.loads(text))
    data = yaml.safe_load(text)
    if not isinstance(data, dict):
        raise ValueError(f"Profile config {path} must be a mapping")
    return cast(dict[str, Any], data)


def _config_profile(name: str, output_root: Path) -> SiteProfile | None:
    if not PROFILES_DIR.exists():
        return None
    for ext in (".yml", ".yaml", ".json"):
        candidate = PROFILES_DIR / f"{name}{ext}"
        if candidate.exists():
            cfg = _load_profile_config(candidate)
            cfg.setdefault("id", name)
            return ConfigSiteProfile(cfg, output_root)
    return None


def load_profile(name: str, output_root: Path | None = None) -> SiteProfile:
    data_root = output_root or (PROJECT_ROOT / "src" / "data")
    if name == "fullstackopen":
        return FullstackOpenProfile(data_root)
    if name == "nextjs-learn":
        return NextjsLearnProfile(data_root)
    profile = _config_profile(name, data_root)
    if profile:
        return profile
    discovered = sorted(PROFILES_DIR.glob("*.yml")) if PROFILES_DIR.exists() else []
    available = ", ".join(p.stem for p in discovered)
    raise ValueError(f"Unknown site profile '{name}'. Available: {available}")


__all__ = ["load_profile"]
