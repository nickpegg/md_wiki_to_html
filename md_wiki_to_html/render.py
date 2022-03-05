import re
import shutil

from markdown import Markdown
from pathlib import Path

from jinja2 import Template

from .common import FILENAME_BAD_CHARS_RE
from .config import Config
from .dir_tree import DirTree, build_tree


def render(config: Config) -> None:
    # Pass 1: build the directory tree, which will get used when rendering a page tree
    # on the page.
    tree = build_tree(config.source_dir_path)
    tree.name = "root"

    # Pass 2: render the files
    md = Markdown(
        extensions=config.flavor.md_extensions,
    )

    template = Template(Path(config.template_path).read_text())

    q = [config.source_dir_path]

    while len(q) > 0:
        dir_ = q.pop()

        # Make sure this dir exists in the output
        rel_dir = str(dir_.relative_to(config.source_dir_path))
        rel_dir = re.sub(FILENAME_BAD_CHARS_RE, "_", rel_dir)

        output_dir = config.output_dir_path.joinpath(rel_dir)
        output_dir.mkdir(exist_ok=True)

        for child in dir_.iterdir():
            if child.name.startswith("."):
                continue
            elif child.is_dir():
                if child.name == output_dir.name:
                    # skip over the output dir if it already exists
                    continue
                q.append(child)
            elif child.is_file():
                if child.name.endswith(".md"):
                    # Render the markdown
                    page_name = child.stem
                    page_dirs = child.parent.parts

                    dest_file_name = child.with_suffix(".html").name
                    dest_file_name = re.sub("[ ]+", "_", dest_file_name)

                    dest_file_path = output_dir.joinpath(dest_file_name)

                    content = md.convert(child.read_text())
                    html = template.render(
                        content=content, page_dirs=page_dirs, title=page_name, tree=tree
                    )
                    dest_file_path.write_text(html)
                    print(f"Wrote {dest_file_path}")

    for static_dir in (".static", "img"):
        static_path = Path(config.source_dir_path, static_dir)
        if static_path.is_dir():
            shutil.copytree(
                static_path,
                Path(config.output_dir_path, static_dir.replace(".", "")),
                dirs_exist_ok=True,
            )
