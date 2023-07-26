from sys import exit

from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    ONE_OR_MORE
)

from src.utils import verbose_time_to_seconds, ComparisonMethod


class FDWArgumentParser(ArgumentParser):
    def error(self, message):
        print(f"Error: {message}\n")
        self.print_help()
        exit(1)


parser = FDWArgumentParser(
    prog='fdw',
    description='...',
    formatter_class=RawTextHelpFormatter,
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

parser.add_argument(
    "--oc", "--on-change",
    metavar="command",
    dest="commands_on_change",
    help="commands to run when a file is added, modified or removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--oa", "--on-add",
    metavar="command",
    dest="commands_on_add",
    help="commands to run when a file is added\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--om", "--on-modify",
    metavar="command",
    dest="commands_on_modify",
    help="commands to run when a file is modified\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--or", "--on-remove",
    metavar="command",
    dest="commands_on_remove",
    help="commands to run when a file is removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)

parser.add_argument(
    "--no-color",
    dest="color",
    help="do not use colors in output",
    action="store_const",
    const=False,
    default=True,
)

comparison_method_group = parser.add_mutually_exclusive_group()
comparison_method_group.add_argument(
    "--mtime",
    help="use modification time to compare files (default)",
    dest="comparison_method",
    action="store_const",
    const=ComparisonMethod.MTIME,
    default=ComparisonMethod.MTIME,
)
comparison_method_group.add_argument(
    "--size",
    dest="comparison_method",
    help="use file size to compare files",
    action="store_const",
    const=ComparisonMethod.SIZE,
)
comparison_method_group.add_argument(
    "--md5",
    dest="comparison_method",
    help="use MD5 hash to compare files",
    action="store_const",
    const=ComparisonMethod.MD5,
)


class FDWArgs(Namespace):
    patterns: "list[str]"

    interval: float
    delay: float
    background: bool

    commands_on_change: "list[str]"
    commands_on_add: "list[str]"
    commands_on_modify: "list[str]"
    commands_on_remove: "list[str]"

    color: bool
    comparison_method: str


cli_args: FDWArgs = parser.parse_args()
