from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    ONE_OR_MORE
)
from importlib.metadata import version
from sys import exit

from .utils import verbose_time_to_seconds, CompareMethod, OperationType

from textwrap import dedent


class FDWArgumentParser(ArgumentParser):
    def error(self, message):
        print(f"Error: {message}")
        exit(1)


parser = FDWArgumentParser(
    prog='fdw',
    description='...',
    epilog=dedent(r'''
    Variable expansions available for commands:
        %name
        %relative_path
        %absolute_path
    '''),
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
    "--ofc", "--on-file-change",
    metavar="command",
    dest="commands_on_file_change",
    help=" Commands to run when a file is added, modified or removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--ofa", "--on-file-add",
    metavar="command",
    dest="commands_on_file_add",
    help="Commands to run when a file is added\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--ofm", "--on-file-modify",
    metavar="command",
    dest="commands_on_file_modify",
    help="Commands to run when a file is modified\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--ofr", "--on-file-remove",
    metavar="command",
    dest="commands_on_file_remove",
    help="Commands to run when a file is removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--odc", "--on-directory-change",
    metavar="command",
    dest="commands_on_directory_change",
    help="Commands to run when a directory is added, modified or removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--oda", "--on-directory-add",
    metavar="command",
    dest="commands_on_directory_add",
    help="Commands to run when a directory is added\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--odm", "--on-directory-modify",
    metavar="command",
    dest="commands_on_directory_modify",
    help="Commands to run when a directory is modified\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
parser.add_argument(
    "--odr", "--on-directory-remove",
    metavar="command",
    dest="commands_on_directory_remove",
    help="Commands to run when a directory is removed\n ",
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

watched_operations_group = parser.add_mutually_exclusive_group()

watched_operations_group.add_argument(
    "--watch",
    metavar="operation",
    dest="_watched_operations",
    help=f"Operations to watch for [{', '.join(OperationType.all())}]\n ",
    nargs=ONE_OR_MORE,
    choices=OperationType.all(),
    default=[],
)
watched_operations_group.add_argument(
    "--ignore",
    metavar="operation",
    dest="_ignored_operations",
    help=f"Operations to ignore [{', '.join(OperationType.all())}]\n ",
    nargs=ONE_OR_MORE,
    choices=OperationType.all(),
    default=[],
)

parser.add_argument(
    "--fcm",
    "--file-compare-method",
    dest="file_compare_method",
    help="method to compare files (default: mtime)",
    choices=CompareMethod.for_files(),
    default=CompareMethod.MTIME.value,
)
parser.add_argument(
    "--dcm",
    "--directory-compare-method",
    dest="directory_compare_method",
    help="method to compare directories (default: mtime)",
    choices=CompareMethod.for_directories(),
    default=CompareMethod.MTIME.value,
)

parser.add_argument(
    "--version",
    action="version",
    version=version("file-directory-watcher"),
)


class FDWArgs(Namespace):
    patterns: "list[str]"

    interval: float
    delay: float
    background: bool

    commands_on_file_change: "list[str]"
    commands_on_file_add: "list[str]"
    commands_on_file_modify: "list[str]"
    commands_on_file_remove: "list[str]"
    commands_on_directory_change: "list[str]"
    commands_on_directory_add: "list[str]"
    commands_on_directory_modify: "list[str]"
    commands_on_directory_remove: "list[str]"

    _watched_operations: "list[str]"
    _ignored_operations: "list[str]"
    operations: "set[str]"

    color: bool
    file_compare_method: CompareMethod
    directory_compare_method: CompareMethod


cli_args: FDWArgs = parser.parse_args()

# Adding commands_on_..._change to other commands
cli_args.commands_on_file_add.extend(cli_args.commands_on_file_change)
cli_args.commands_on_file_modify.extend(cli_args.commands_on_file_change)
cli_args.commands_on_file_remove.extend(cli_args.commands_on_file_change)
cli_args.commands_on_directory_add.extend(cli_args.commands_on_directory_change)
cli_args.commands_on_directory_modify.extend(cli_args.commands_on_directory_change)
cli_args.commands_on_directory_remove.extend(cli_args.commands_on_directory_change)


# Determining operations to watch for
cli_args._watched_operations = set(cli_args._watched_operations)
if OperationType.FILE_CHANGED.value in cli_args._watched_operations:
    cli_args._watched_operations.update({
        OperationType.FILE_ADDED.value,
        OperationType.FILE_REMOVED.value,
        OperationType.FILE_MODIFIED.value,
    })

cli_args._ignored_operations = set(cli_args._ignored_operations)
if OperationType.FILE_CHANGED.value in cli_args._ignored_operations:
    cli_args._ignored_operations.update({
        OperationType.FILE_ADDED.value,
        OperationType.FILE_REMOVED.value,
        OperationType.FILE_MODIFIED.value,
    })

cli_args.operations = set(OperationType.all()).intersection(
    cli_args._watched_operations
).difference(
    cli_args._ignored_operations
)
