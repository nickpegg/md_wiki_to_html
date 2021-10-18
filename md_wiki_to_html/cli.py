from argparse import ArgumentParser, Namespace
from pathlib import Path

from .config import Config


def main() -> None:
    pass


def parse_args() -> Config:
    arg_parser = ArgumentParser()

    arg_parser.add_argument(
        "--source",
        default=str(Path.cwd()),
        help="Path to the directory containing the markdown wiki",
    )
    arg_parser.add_argument(
        "--output",
        default="_output",
        help="Path to output the rendered HTML to",
    )
    arg_parser.add_argument(
        "--template",
        default="_source/template.html",
        help="Path to the template to use for rendering HTML",
    )

    # TODO: add init subcommand to spit out some default example HTML and CSS

    args = arg_parser.parse_args()
    return Config(
        source_dir_path=Path(args.source),
        output_dir_path=Path(args.output),
        template_path=Path(args.template),
    )


if __name__ == "__main__":
    main()
