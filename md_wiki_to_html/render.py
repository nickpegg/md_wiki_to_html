from markdown import Markdown
from pathlib import Path

from jinja2 import Template

from .config import Config
from .dir_tree import DirTree, build_tree


def render(config: Config) -> None:
    # Pass 1: build the directory tree, which will get used when rendering a page tree
    # on the page.
    tree = build_tree(config.source_dir_path)
    tree.name = "root"

    # Pass 2: render the files
    md = Markdown(
        extensions=[
            "nl2br",
            "wikilinks",
            "pymdownx.superfences",
            "pymdownx.tasklist",
        ],
    )

    template = Template(Path(config.template_path).read_text())

    q = [config.source_dir_path]

    while len(q) > 0:
        dir_ = q.pop()

        # Make sure this dir exists in the output
        rel_dir = dir_.relative_to(config.source_dir_path)
        output_dir = config.output_dir_path.joinpath(rel_dir)
        output_dir.mkdir(exist_ok=True)

        for child in dir_.iterdir():
            if child.is_file():
                print(child)
                if child.name.endswith(".md"):
                    dest_file_name = child.with_suffix(".html").name
                    dest_file_path = output_dir.joinpath(dest_file_name)

                    contents = md.convert(child.read_text())
                    # TODO: pass tree to template
                    html = template.render(contents=contents)
                    dest_file_path.write_text(html)
                    print(f"Wrote {dest_file_path}")
            elif child.is_dir():
                q.append(child)

    # TODO: copy over static files (CSS, JS, etc.)
