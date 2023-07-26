from sys import exit

from argparse import (
    ArgumentParser,
    Namespace,
    ONE_OR_MORE
)


class FDWArgumentParser(ArgumentParser):
    def error(self, message):
        print(f"Error: {message}\n")
        self.print_help()
        exit(1)


parser = FDWArgumentParser(
    prog='fdw',
    description='...',
)

# Positional arguments
parser.add_argument(
    "patterns",
    metavar="pattern",
    help="glob pattern to watch for changes",
    nargs=ONE_OR_MORE,
)


class FDWArgs(Namespace):
    patterns: "list[str]"


cli_args: FDWArgs = parser.parse_args()
