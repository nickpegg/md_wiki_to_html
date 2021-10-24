"""
Tests for dir_tree module
"""

from pathlib import Path
from md_wiki_to_html.dir_tree import build_tree, DirTree


wiki_dir = Path(__file__).with_name("example_wiki")


def test_build_tree() -> None:
    tree = build_tree(wiki_dir)
    assert tree.name == "example_wiki"
    assert {"index", "Some page", "obsidian"} == set(tree.pages)
    assert {"Another top-level", "Some dir"} == {c.name for c in tree.children}

    for child in tree.children:
        if child.name == "Some dir":
            assert set(child.pages) == {"Nested"}
            assert {c.name for c in child.children} == {"Another dir"}


def test_sort() -> None:
    tree = DirTree(
        name="root",
        pages=["foo", "bar", "jawn"],
        children=[
            DirTree(name="some dir", pages=[], children=[]),
            DirTree(name="dir1", pages=[], children=[]),
        ],
    )

    # Sort, and make sure things are sorted
    tree.sort()
    assert tree.pages == sorted(tree.pages)
    assert [c.name for c in tree.children] == sorted([c.name for c in tree.children])
