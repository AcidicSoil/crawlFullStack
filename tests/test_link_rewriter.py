from pathlib import Path

from fullstackopen_en_repo.link_rewriter import rewrite_markdown_links
from fullstackopen_en_repo.profiles.nextjs_learn import NextjsLearnProfile


def test_rewrite_links_none(tmp_path: Path) -> None:
    profile = NextjsLearnProfile(tmp_path)
    markdown = "[Intro](https://nextjs.org/learn)"
    assert (
        rewrite_markdown_links(
            markdown,
            mode="none",
            profile=profile,
            from_url="https://nextjs.org/learn",
        )
        == markdown
    )


def test_rewrite_links_local(tmp_path: Path) -> None:
    profile = NextjsLearnProfile(tmp_path)
    markdown = (
        "[Overview](https://nextjs.org/learn/dashboard-app) "
        "[Chapter](/learn/dashboard-app/css-styling) "
        "[External](https://example.com)"
    )
    rewritten = rewrite_markdown_links(
        markdown,
        mode="local",
        profile=profile,
        from_url="https://nextjs.org/learn/dashboard-app/getting-started",
    )
    assert "[Overview](index.md)" in rewritten
    assert "[Chapter](css-styling.md)" in rewritten
    assert "[External](https://example.com)" in rewritten
