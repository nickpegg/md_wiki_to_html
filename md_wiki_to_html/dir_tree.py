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

    def has_pages(self) -> bool:
        """
        Returns true if this tree has any pages or its children have any pages
        """
        if len(self.pages) > 0:
            return True

        for child in self.children:
            if child.has_pages():
                return True

        return False

    def to_html_navtree(self, dir_path: str) -> str:
        """
        Because doing this recursion in Jinja is just too hard
        """
        acc = "<ul>"
        page_names = set(self.pages)
        children = {c.name: c for c in self.children}

        for name in sorted(set(self.pages + list(children.keys()))):
            if name in page_names:
                acc += "<li>"
                p = Path(dir_path, name)
                acc += f'<a href="{p}.html">{name}</a>'
            else:
                acc += "<li>"
                acc += name
            acc += "</li>"

            if name in children and children[name].has_pages():
                acc += children[name].to_html_navtree(str(Path(dir_path, name)))

        acc += "</ul>"
        return acc


def build_tree(dir_: Path) -> DirTree:
    """
    Recursively build a DirTree from the given dir. Ignores all non-markdown files.
    """
    tree = DirTree(name=dir_.name, pages=[], children=[])

    for child in dir_.iterdir():
        if child.name.startswith("."):
            continue
        elif child.is_file() and child.name.endswith(".md"):
            tree.pages.append(child.name.replace(".md", ""))
        elif child.is_dir():
            child_tree = build_tree(child)
            tree.children.append(child_tree)

    return tree
