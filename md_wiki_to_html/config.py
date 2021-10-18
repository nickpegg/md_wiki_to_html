from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config(object):
    source_dir_path: Path
    output_dir_path: Path
    template_path: Path
