from time import sleep

from .argument_parser import FDWArgs
from .cli import CLI
from .const import (
    FILE_ADDED,
    FILE_MODIFIED,
    FILE_REMOVED,
    DIRECTORY_ADDED,
    DIRECTORY_MODIFIED,
    DIRECTORY_REMOVED,
)
from .utils import (
    File,
    Directory,
    fs_entries_from_patterns,
    changes_in_entries,
    compute_state,
    expand_command_variables,
    run_command,
)


class FDW:

    args: FDWArgs

    def __init__(self, args: FDWArgs):
        self.args = args

        self.cli = CLI(self.args.verbosity, self.args.no_color)
        self.states: "dict[File | Directory]" = {}

    def _compute_state_for_entry(self, entry: "File | Directory"):
        compare_methods = type(entry) == File and self.args.file_compare_methods or self.args.directory_compare_methods
        return compute_state(entry, compare_methods)

    def compute_starting_states(self):
        for entry in fs_entries_from_patterns(self.args.patterns, self.args.exclude_patterns):
            self.states.setdefault(entry, self._compute_state_for_entry(entry))

    def _should_handle_added(self, entry: "File | Directory") -> bool:
        if type(entry) == File:
            return FILE_ADDED in self.args.watched_operations
        if type(entry) == Directory:
            return DIRECTORY_ADDED in self.args.watched_operations

    def _handle_added(self, entry: "File | Directory"):
        self.states.setdefault(entry, self._compute_state_for_entry(entry))

        if not self._should_handle_added(entry):
            return

        commands = type(entry) == File and self.args.commands_on_file_add or self.args.commands_on_directory_add
        expanded_commands = [expand_command_variables(command, entry) for command in commands]

        self.cli.added_entry(entry)
        for command in expanded_commands:
            self.cli.running_command(command, self.args.background)
            run_command(command, self.args.background)

    def _compare_file_states(self, entry: "File | Directory") -> bool:
        self._cached_entry_state = self._compute_state_for_entry(entry)

        return self.states.get(entry) == self._cached_entry_state

    def _should_handle_modified(self, entry: "File | Directory") -> bool:
        if type(entry) == File:
            return FILE_MODIFIED in self.args.watched_operations
        if type(entry) == Directory:
            return DIRECTORY_MODIFIED in self.args.watched_operations

    def _handle_modified(self, entry: "File | Directory"):
        self.states[entry] = self._cached_entry_state
        self._cached_entry_state = None

        if not self._should_handle_modified(entry):
            return

        commands = type(entry) == File and self.args.commands_on_file_modify or self.args.commands_on_directory_modify
        expanded_commands = [expand_command_variables(command, entry) for command in commands]

        self.cli.modified_entry(entry)
        for command in expanded_commands:
            self.cli.running_command(command, self.args.background)
            run_command(command, self.args.background)

    def _should_handle_removed(self, entry: "File | Directory") -> bool:
        if type(entry) == File:
            return FILE_REMOVED in self.args.watched_operations
        if type(entry) == Directory:
            return DIRECTORY_REMOVED in self.args.watched_operations

    def _handle_removed(self, entry: "File | Directory"):
        self.states.pop(entry)

        if not self._should_handle_removed(entry):
            return

        commands = type(entry) == File and self.args.commands_on_file_remove or self.args.commands_on_directory_remove
        expanded_commands = [expand_command_variables(command, entry) for command in commands]

        self.cli.removed_entry(entry)
        for command in expanded_commands:
            self.cli.running_command(command, self.args.background)
            run_command(command, self.args.background)

    def watch_for_changes(self):
        self.cli.watching_entries(self.states)

        while True:
            previous_entries = set(self.states.keys())
            current_entries = set(fs_entries_from_patterns(self.args.patterns, self.args.exclude_patterns))

            for (entry, added, present_in_both, removed) in changes_in_entries(previous_entries, current_entries):
                self.args.delay and sleep(self.args.delay)

                if added:
                    self._handle_added(entry)
                    continue

                if present_in_both and not self._compare_file_states(entry):
                    self._handle_modified(entry)
                    continue

                if removed:
                    self._handle_removed(entry)
                    continue

            sleep(self.args.interval)
