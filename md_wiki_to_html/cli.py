from argparse import ArgumentParser, Namespace, ArgumentDefaultsHelpFormatter
from pathlib import Path

from .config import Config, FLAVORS
from .render import render


def main() -> None:
    args = parse_args()
    if args.action == "render":
        config = Config(
            source_dir_path=Path(args.source),
            output_dir_path=Path(args.output),
            template_path=Path(args.template),
            flavor=FLAVORS[args.flavor],
        )
        try:
            render(config)
        except Exception as e:
            if args.verbose:
                raise
            else:
                print(e)
    elif args.action == "init":
        pass


def parse_args() -> Namespace:
    arg_parser = ArgumentParser(
        description="Convert Markdown wikis (vimwiki, Obsidian, etc.) to HTML files",
        formatter_class=ArgumentDefaultsHelpFormatter,
    )
    arg_parser.add_argument("-v", "--verbose", action="store_true")
    subparsers = arg_parser.add_subparsers()

    # TODO: finish init subcommand to spit out some default example HTML and CSS
    init_parser = subparsers.add_parser("init")
    init_parser.set_defaults(action="init")

    render_parser = subparsers.add_parser("render")
    render_parser.set_defaults(action="render")
    render_parser.add_argument(
        "--source",
        default=".",
        help="Path to the directory containing the markdown wiki",
    )
    render_parser.add_argument(
        "--output",
        default="_output",
        help="Path to output the rendered HTML to",
    )
    render_parser.add_argument(
        "--template",
        default="_source/template.html",
        help="Path to the template to use for rendering HTML",
    )
    render_parser.add_argument(
        "--flavor",
        default="obsidian",
        choices=FLAVORS.keys(),
        help="Flavor of Markdown to use",
    )

    return arg_parser.parse_args()


if __name__ == "__main__":
    main()
