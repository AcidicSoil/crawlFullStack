from pathlib import Path

from fullstackopen_en_repo.profiles.nextjs_learn import NextjsLearnProfile


def test_nextjs_path_mapping(tmp_path: Path) -> None:
    profile = NextjsLearnProfile(tmp_path)
    assert (
        profile.normalize_url("https://nextjs.org/learn/") == "https://nextjs.org/learn"
    )
    assert (
        profile.normalize_url("https://www.nextjs.org/learn/dashboard-app/")
        == "https://nextjs.org/learn/dashboard-app"
    )

    root = profile.derive_output_path("https://nextjs.org/learn")
    assert root == tmp_path / "nextjs-learn" / "index.md"

    overview = profile.derive_output_path("https://nextjs.org/learn/dashboard-app")
    assert overview == tmp_path / "nextjs-learn" / "dashboard-app" / "index.md"

    chapter = profile.derive_output_path(
        "https://nextjs.org/learn/dashboard-app/getting-started"
    )
    assert chapter == tmp_path / "nextjs-learn" / "dashboard-app" / "getting-started.md"

    rel = profile.map_url_to_relpath(
        "https://nextjs.org/learn/dashboard-app/getting-started",
        "https://nextjs.org/learn/dashboard-app",
    )
    assert rel == "index.md"


def test_nextjs_scope_and_enqueue(tmp_path: Path) -> None:
    profile = NextjsLearnProfile(tmp_path)
    assert profile.in_scope("https://nextjs.org/learn/dashboard-app")
    assert profile.should_enqueue("https://nextjs.org/learn/dashboard-app/css-styling")
    assert not profile.in_scope("https://nextjs.org/docs")
