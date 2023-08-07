from argparse import (
    ArgumentParser,
    Namespace,
    RawTextHelpFormatter,
    ONE_OR_MORE
)
from importlib.metadata import version
from sys import exit
from textwrap import dedent

from .const import (
    FILE_CHANGED,
    FILE_ADDED,
    FILE_MODIFIED,
    FILE_REMOVED,
    DIRECTORY_CHANGED,
    DIRECTORY_ADDED,
    DIRECTORY_MODIFIED,
    DIRECTORY_REMOVED,
    ALL_OPERATIONS,
    MTIME,
    MODE,
    UID,
    GID,
    FILE_COMPARE_METHODS,
    DIRECTORY_COMPARE_METHODS,
)
from .utils import verbose_time_to_seconds



class FDWArgumentParser(ArgumentParser):
    def error(self, message):
        print(f"Error: {message}")
        print("Try 'fdw --help' for more information.")
        exit(1)


parser = FDWArgumentParser(
    prog='fdw',
    description='CLI tool for monitoring changes, additions, removals in files and directories and optionally running commands on specified operations.',
    epilog=dedent(f'''
    Custom formats:
        TIME: e.g. 5s, 1m30s, 1h, 1h30m, 1d, 1d12h30m
        OPERATION: {', '.join(ALL_OPERATIONS)}

    Variable expansions available for commands:
        %name
        %relative_path
        %absolute_path
    '''),
    formatter_class=RawTextHelpFormatter,
)

patterns_subgroup = parser.add_argument_group("Patterns for files and directories")
patterns_subgroup.add_argument(
    "patterns",
    metavar="pattern",
    help="glob pattern to watch for changes\n ",
    nargs=ONE_OR_MORE,
)
patterns_subgroup.add_argument(
    "--exclude",
    metavar="pattern",
    dest="exclude_patterns",
    help="glob patterns to exclude from watching\n ",
    nargs=ONE_OR_MORE,
)

configuration_subgroup = parser.add_argument_group("Configuration options")
configuration_subgroup.add_argument(
    "-i", "--interval",
    metavar="TIME",
    dest="interval",
    help="interval between running the watcher (default: 1s)\n ",
    default='1s',
    type=verbose_time_to_seconds,
)
configuration_subgroup.add_argument(
    "-d", "--delay",
    metavar="TIME",
    dest="delay",
    help="delay between files (default: 0s)\n ",
    default='0s',
    type=verbose_time_to_seconds,
)
configuration_subgroup.add_argument(
    "-b", "--background",
    dest="background",
    help="run commands in background non-blocking processes (default: false)\n ",
    action="store_true",
)
watched_operations_group = configuration_subgroup.add_mutually_exclusive_group()
watched_operations_group.add_argument(
    "--watch",
    metavar="OPERATION",
    dest="watched_operations",
    help=f"operations to watch for (default: all)\n ",
    nargs=ONE_OR_MORE,
    choices=ALL_OPERATIONS,
    default=ALL_OPERATIONS,
)
watched_operations_group.add_argument(
    "--ignore",
    metavar="OPERATION",
    dest="ignored_operations",
    help=f"operations to ignore (default: none)\n ",
    nargs=ONE_OR_MORE,
    choices=ALL_OPERATIONS,
    default=[],
)
configuration_subgroup.add_argument(
    "--fcm",
    "--file-compare-method",
    dest="file_compare_methods",
    help="methods to compare files (default: mtime)\n ",
    choices=FILE_COMPARE_METHODS,
    nargs=ONE_OR_MORE,
    default=[MTIME, MODE, UID, GID],
)
configuration_subgroup.add_argument(
    "--dcm",
    "--directory-compare-method",
    dest="directory_compare_methods",
    help="methods to compare directories (default: mtime)\n ",
    choices=DIRECTORY_COMPARE_METHODS,
    nargs=ONE_OR_MORE,
    default=[MTIME, MODE, UID, GID],
)
configuration_subgroup.add_argument(
    "--no-color",
    dest="no_color",
    help="do not use colors in output (default: false)",
    action="store_true",
)


commands_subgroup = parser.add_argument_group("Commands to run on specified operations")
commands_subgroup.add_argument(
    "--oc", "--on-change",
    metavar="command",
    dest="commands_on_change",
    help=" commands to run when a file or directory is added, modified or removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--oa", "--on-add",
    metavar="command",
    dest="commands_on_add",
    help="commands to run when a file or directory is added\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--om", "--on-modify",
    metavar="command",
    dest="commands_on_modify",
    help="commands to run when a file or directory is modified\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--or", "--on-remove",
    metavar="command",
    dest="commands_on_remove",
    help="commands to run when a file or directory is removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--ofc", "--on-file-change",
    metavar="command",
    dest="commands_on_file_change",
    help=" commands to run when a file is added, modified or removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--ofa", "--on-file-add",
    metavar="command",
    dest="commands_on_file_add",
    help="commands to run when a file is added\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--ofm", "--on-file-modify",
    metavar="command",
    dest="commands_on_file_modify",
    help="commands to run when a file is modified\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--ofr", "--on-file-remove",
    metavar="command",
    dest="commands_on_file_remove",
    help="commands to run when a file is removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--odc", "--on-directory-change",
    metavar="command",
    dest="commands_on_directory_change",
    help="commands to run when a directory is added, modified or removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--oda", "--on-directory-add",
    metavar="command",
    dest="commands_on_directory_add",
    help="commands to run when a directory is added\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--odm", "--on-directory-modify",
    metavar="command",
    dest="commands_on_directory_modify",
    help="commands to run when a directory is modified\n ",
    nargs=ONE_OR_MORE,
    default=[],
)
commands_subgroup.add_argument(
    "--odr", "--on-directory-remove",
    metavar="command",
    dest="commands_on_directory_remove",
    help="commands to run when a directory is removed\n ",
    nargs=ONE_OR_MORE,
    default=[],
)

other_subgroup = parser.add_argument_group("Other options")
other_subgroup.add_argument(
    "--version",
    action="version",
    version=version("file-directory-watcher"),
)


# Reordering and customizing help
parser._action_groups = parser._action_groups[2:]  # Removing two default groups
parser._action_groups[-1]._group_actions.insert(0, parser._actions[0]) # Moving help argument to last group


class FDWArgs(Namespace):
    patterns: "list[str]"
    exclude_patterns: "list[str]"

    interval: float
    delay: float
    background: bool
    watched_operations: "list[str]"
    ignored_operations: "list[str]"
    no_color: bool
    file_compare_method: str
    directory_compare_method: str

    commands_on_change: "list[str]"
    commands_on_add: "list[str]"
    commands_on_modify: "list[str]"
    commands_on_remove: "list[str]"
    commands_on_file_change: "list[str]"
    commands_on_file_add: "list[str]"
    commands_on_file_modify: "list[str]"
    commands_on_file_remove: "list[str]"
    commands_on_directory_change: "list[str]"
    commands_on_directory_add: "list[str]"
    commands_on_directory_modify: "list[str]"
    commands_on_directory_remove: "list[str]"


cli_args: FDWArgs = parser.parse_args()

## Post-parse modifications

# Adding on change commands to other commands
cli_args.commands_on_file_add += cli_args.commands_on_file_change + cli_args.commands_on_change
cli_args.commands_on_file_modify += cli_args.commands_on_file_change + cli_args.commands_on_change
cli_args.commands_on_file_remove += cli_args.commands_on_file_change + cli_args.commands_on_change
cli_args.commands_on_directory_add += cli_args.commands_on_directory_change + cli_args.commands_on_change
cli_args.commands_on_directory_modify += cli_args.commands_on_directory_change + cli_args.commands_on_change
cli_args.commands_on_directory_remove += cli_args.commands_on_directory_change + cli_args.commands_on_change

# Determining operations to watch for
cli_args.watched_operations = set(cli_args.watched_operations)
cli_args.ignored_operations = set(cli_args.ignored_operations)

if FILE_CHANGED in cli_args.watched_operations:
    cli_args.watched_operations.update({FILE_ADDED, FILE_REMOVED, FILE_MODIFIED,})

if DIRECTORY_CHANGED in cli_args.watched_operations:
    cli_args.watched_operations.update({DIRECTORY_ADDED, DIRECTORY_REMOVED, DIRECTORY_MODIFIED})

if FILE_CHANGED in cli_args.ignored_operations:
    cli_args.ignored_operations.update({FILE_ADDED, FILE_REMOVED, FILE_MODIFIED,})

if DIRECTORY_CHANGED in cli_args.ignored_operations:
    cli_args.ignored_operations.update({DIRECTORY_ADDED, DIRECTORY_REMOVED, DIRECTORY_MODIFIED})

cli_args.watched_operations.difference_update(cli_args.ignored_operations)
