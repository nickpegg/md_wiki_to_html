from dataclasses import dataclass
from pathlib import Path
from typing import List, Type


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
    md_extensions: List[str]


# Various flavors, which define what markdown extensions should be used
FLAVORS = {
    "obsidian": Flavor(
        name="obsidian",
        md_extensions=[
            "nl2br",
            "wikilinks",
            "pymdownx.superfences",
            "pymdownx.tasklist",
        ],
    ),
}
