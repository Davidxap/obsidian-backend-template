import common


def test_update_frontmatter_is_idempotent_and_preserves_body(tmp_path):
    note = tmp_path / "n.md"
    note.write_text("---\na: 1\n---\nbody\n")
    common.update_frontmatter(note, {"b": 2})
    common.update_frontmatter(note, {"b": 2})
    assert note.read_text() == "---\na: 1\nb: 2\n---\nbody\n"


def test_none_becomes_empty_value(tmp_path):
    note = tmp_path / "n.md"
    common.update_frontmatter(note, {"x": None})
    assert common.read_note(note)[0] == {"x": ""}


def test_mark_failed_never_overwrites_a_real_value(tmp_path):
    note = tmp_path / "n.md"
    common.update_frontmatter(note, {"github_stars": 8})
    common.mark_failed(note, ["github_stars", "github_followers"])
    props, _ = common.read_note(note)
    assert props["github_stars"] == "8"
    assert props["github_followers"] == ""
