from pathlib import Path

from fullstackopen_en_repo.profiles.config_profile import ConfigSiteProfile

SAMPLE_CONFIG = {
    "id": "sample",
    "domains": ["example.com"],
    "entrypoints": ["https://example.com/root"],
    "default_max_depth": 2,
    "scope": {
        "allow": [r"^/root(/.*)?$"],
        "strip_prefix": "/root",
        "canonical_host": "example.com",
        "canonical_scheme": "https",
    },
    "output": {
        "site_dir": "example",
        "root_index": "index.md",
        "section_index": "index.md",
        "leaf_extension": ".md",
    },
}


def test_config_profile_output(tmp_path: Path) -> None:
    profile = ConfigSiteProfile(SAMPLE_CONFIG, tmp_path)
    normalized = profile.normalize_url("https://www.example.com/root/guide/?foo=bar")
    assert normalized == "https://example.com/root/guide"
    assert profile.in_scope("https://example.com/root/guide")
    assert not profile.in_scope("https://example.com/other")

    root = profile.derive_output_path("https://example.com/root")
    assert root == tmp_path / "example" / "index.md"

    child = profile.derive_output_path("https://example.com/root/getting-started")
    assert child == tmp_path / "example" / "getting-started" / "index.md"
