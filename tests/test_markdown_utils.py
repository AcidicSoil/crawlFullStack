from fullstackopen_en_repo.markdown_utils import split_frontmatter


def test_split_frontmatter_json():
    text = "---\n{\"key\": \"value\"}\n---\nBody"
    meta, body, block = split_frontmatter(text)
    assert meta["key"] == "value"
    assert body.strip() == "Body"
    assert block.startswith("---")


def test_split_frontmatter_yaml():
    text = "---\nid: abc\ntitle: Hello\nchecksum: '123'\n---\nContent"
    meta, body, _ = split_frontmatter(text)
    assert meta["id"] == "abc"
    assert meta["checksum"] == "123"
    assert body.strip() == "Content"
