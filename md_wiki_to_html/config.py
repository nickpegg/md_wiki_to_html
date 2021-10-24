from dataclasses import dataclass
from pathlib import Path
from typing import List, Type, Union

from markdown.extensions import Extension

from .extensions.highlight import HighlightExtension



@dataclass
class Config(object):
    source_dir_path: Path
    output_dir_path: Path
    template_path: Path
    flavor: "Flavor"


@dataclass
class Flavor(object):
    """
    Represents various Markdown flavors
    """

    name: str
    md_extensions: List[Union[str, Extension]]


# Various flavors, which define what markdown extensions should be used
FLAVORS = {
    "obsidian": Flavor(
        # https://help.obsidian.md/How+to/Format+your+notes
        name="obsidian",
        md_extensions=[
            "nl2br",
            "tables",
            "wikilinks",
            "pymdownx.arithmatex",
            "pymdownx.superfences",
            "pymdownx.tasklist",
            HighlightExtension(),
        ],
    ),
}
