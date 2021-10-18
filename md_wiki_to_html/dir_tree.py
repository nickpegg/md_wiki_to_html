from dataclasses import dataclass
from typing import List
from pathlib import Path


@dataclass
class DirTree(object):
    """
    Represents a directory tree
    """

    name: str
    pages: List[str]
    children: List["DirTree"]

    def sort(self) -> None:
        """
        Sort the pages in this DirTree in-place alphabetically, as well as the pages in
        all of the child trees.
        """
        q = [self]

        while len(q) > 0:
            current = q.pop()
            current.pages = sorted(current.pages)
            current.children = sorted(current.children, key=lambda c: c.name)
            q.extend(current.children)


def build_tree(dir_: Path) -> DirTree:
    """
    Recursively build a DirTree from the given dir. Ignores all non-markdown files.
    """
    tree = DirTree(name=dir_.name, pages=[], children=[])

    for child in dir_.iterdir():
        if child.is_file() and child.name.endswith(".md"):
            tree.pages.append(child.name.replace(".md", ""))
        elif child.is_dir():
            child_tree = build_tree(child)
            tree.children.append(child_tree)

    return tree
