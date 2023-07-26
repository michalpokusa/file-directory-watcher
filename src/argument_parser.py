from sys import exit

from argparse import (
    ArgumentParser,
    Namespace,
    ONE_OR_MORE
)

from src.utils import verbose_time_to_seconds


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

# Optional arguments
parser.add_argument(
    "-i", "--interval",
    metavar="seconds",
    dest="interval",
    help="interval between running the watcher in seconds (default: 1s)",
    default='1s',
    type=verbose_time_to_seconds,
)
parser.add_argument(
    "-d", "--delay",
    metavar="seconds",
    dest="delay",
    help="delay between files in seconds (default: 0s)",
    default='0s',
    type=verbose_time_to_seconds,
)
parser.add_argument(
    "-b", "--background",
    dest="background",
    help="run commands in background non-blocking processes",
    action="store_true",
)


class FDWArgs(Namespace):
    patterns: "list[str]"

    interval: float
    delay: float
    background: bool


cli_args: FDWArgs = parser.parse_args()
