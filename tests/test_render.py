"""
tests for the renderer
"""

from pathlib import Path
from typing import Iterator
from tempfile import TemporaryDirectory

import pytest

from md_wiki_to_html.render import render
from md_wiki_to_html.config import Config


@pytest.fixture
def config() -> Iterator[Config]:
    wiki_dir = Path(__file__).with_name("example_wiki")
    with TemporaryDirectory() as tmp:
        yield Config(
            source_dir_path=wiki_dir,
            output_dir_path=Path(tmp),
            template_path=wiki_dir.joinpath("template.html"),
        )


def test_render(config: Config) -> None:
    """
    Do some basic checks that output files exist and are non-empty after we render an
    example wiki
    """
    render(config)

    expected_files = [
        "index.html",
        "Some page.html",
        "Another top-level/Another.html",
        "Some dir/Nested.html",
        "Some dir/Another dir/Deeper.html",
    ]
    for expected_file in expected_files:
        expected = config.output_dir_path.joinpath(Path(expected_file))
        assert expected.is_file()
        assert expected.read_text() != ""
