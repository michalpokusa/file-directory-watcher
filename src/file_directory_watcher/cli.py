from dataclasses import dataclass
from os.path import relpath, abspath

from .const import (
    LIMITED,
    NORMAL,
    FULL,
)
from .utils import formatted_current_time, File, Directory


class Colors:
    DARK_GRAY = "\x1b[38;5;8m"
    LIGHT_GRAY = "\x1b[38;5;249m"
    GREEN = "\x1b[38;5;40m"
    YELLOW = "\x1b[38;5;220m"
    RED = "\x1b[38;5;196m"
    UNDERLINE = "\x1b[4m"
    RESET = "\x1b[0m"


class NoColors:
    DARK_GRAY = ""
    LIGHT_GRAY = ""
    GREEN = ""
    YELLOW = ""
    RED = ""
    UNDERLINE = ""
    RESET = ""


@dataclass
class Operation:
    name: str
    symbol: str
    color: str


class CLI:
    def __init__(self, verbosity: int, no_color: bool):
        self.verbosity = verbosity
        self.colors = NoColors() if no_color else Colors()
        self.add_operation = Operation("added", "+", self.colors.GREEN)
        self.modify_operation = Operation("modified", "~", self.colors.YELLOW)
        self.remove_operation = Operation("removed", "-", self.colors.RED)

    def _print_prefix_timestamp(self):
        print(
            f"{self.colors.LIGHT_GRAY}[{self.colors.DARK_GRAY}{formatted_current_time()}{self.colors.LIGHT_GRAY}]{self.colors.RESET}",
            end=" ",
        )

    def _verbose_type_of_entries(self, entries: "set[str]"):
        nr_of_files = sum(1 for entry in entries if type(entry) == File)
        nr_of_directories = sum(1 for entry in entries if type(entry) == Directory)
        output_parts = []

        if nr_of_files > 0:
            output_parts.append(f'{nr_of_files} file{"" if nr_of_files == 1 else "s"}')
        if nr_of_directories > 0:
            output_parts.append(f'{nr_of_directories} director{"y" if nr_of_directories == 1 else "ies"}')

        return " and ".join(output_parts)

    def watching_entries(self, entries: "set[File | Directory]", max_displayed_entries = 10):
        sorted_entries: "list[File | Directory]" = sorted(entries, key=lambda entry: entry.path)
        types_of_entries = self._verbose_type_of_entries(sorted_entries)

        self._print_prefix_timestamp()
        if self.verbosity == LIMITED:
            print(f'Watching {types_of_entries}')

        elif self.verbosity == NORMAL:
            print(f'Watching {types_of_entries}:')
            for entry in sorted_entries[:max_displayed_entries]:
                print(relpath(entry.path))
            if len(sorted_entries) > max_displayed_entries:
                print(f'and {len(sorted_entries) - max_displayed_entries} more...')

        elif self.verbosity == FULL:
            print(f'Watching {types_of_entries}:')
            for entry in sorted_entries:
                print(abspath(entry.path))

    def _print_entry_operation(self, entry: "File | Directory", operation: Operation):
        self._print_prefix_timestamp()
        if self.verbosity == LIMITED:
            print(f"{operation.color}{operation.symbol}{self.colors.UNDERLINE}{relpath(entry.path)}{self.colors.RESET}")

        elif self.verbosity == NORMAL:
            print(f"{operation.color}{self.colors.UNDERLINE}{relpath(entry.path)}{self.colors.RESET} {operation.name}")

        elif self.verbosity == FULL:
            entry_type = type(entry) == File and "File" or "Directory"
            print(f"{entry_type} {operation.color}{self.colors.UNDERLINE}{abspath(entry.path)}{self.colors.RESET} was {operation.name}")

    def added_entry(self, entry: "File | Directory"):
        self._print_entry_operation(entry, self.add_operation)

    def modified_entry(self, entry: "File | Directory"):
        self._print_entry_operation(entry, self.modify_operation)

    def removed_entry(self, entry: "File | Directory"):
        self._print_entry_operation(entry, self.remove_operation)

    def running_command(self, command: str, background: bool = False):
        if self.verbosity == LIMITED:
            return

        self._print_prefix_timestamp()
        if self.verbosity == NORMAL:
            print(command)

        elif self.verbosity == FULL:
            print(f'Running in {"background" if background else "foreground"}: {command}')
