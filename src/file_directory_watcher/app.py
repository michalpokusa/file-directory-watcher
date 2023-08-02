from time import sleep

from .argument_parser import FDWArgs
from .cli import CLI
from .utils import (
    File,
    Directory,
    OperationType,
    fs_entries_from_patterns,
    changes_in_entries,
    compute_state,
    expand_command_variables,
    run_commands,
)


class FDW:

    args: FDWArgs

    def __init__(self, args: FDWArgs):
        self.args = args

        self.cli = CLI(self.args.color)
        self.states: "dict[File | Directory]" = {}

    def _compute_state_for_entry(self, entry: "File | Directory"):
        compare_method = type(entry) == File and self.args.file_compare_method or self.args.directory_compare_method
        return compute_state(entry, compare_method)

    def compute_starting_states(self):
        for entry in fs_entries_from_patterns(self.args.patterns):
            self.states.setdefault(entry, self._compute_state_for_entry(entry))

    def _should_handle_added(self, entry: "File | Directory") -> bool:
        if type(entry) == File:
            return OperationType.FILE_ADDED.value in self.args.operations
        if type(entry) == Directory:
            return OperationType.DIRECTORY_ADDED.value in self.args.operations

    def _handle_added(self, entry: "File | Directory"):
        self.states.setdefault(entry, self._compute_state_for_entry(entry))

        if not self._should_handle_added(entry):
            return

        commands = type(entry) == File and self.args.commands_on_file_add or self.args.commands_on_directory_add
        expanded_commands = [expand_command_variables(command, entry) for command in commands]

        self.cli.added_entry(entry)
        self.cli.running_commands(expanded_commands)
        run_commands(*expanded_commands, background=self.args.background)

    def _compare_file_states(self, entry: "File | Directory") -> bool:
        self._cached_entry_state = self._compute_state_for_entry(entry)

        return self.states.get(entry) == self._cached_entry_state

    def _should_handle_modified(self, entry: "File | Directory") -> bool:
        if type(entry) == File:
            return OperationType.FILE_MODIFIED.value in self.args.operations
        if type(entry) == Directory:
            return OperationType.DIRECTORY_MODIFIED.value in self.args.operations

    def _handle_modified(self, entry: "File | Directory"):
        self.states[entry] = self._cached_entry_state
        self._cached_entry_state = None

        if not self._should_handle_modified(entry):
            return

        commands = type(entry) == File and self.args.commands_on_file_modify or self.args.commands_on_directory_modify
        expanded_commands = [expand_command_variables(command, entry) for command in commands]

        self.cli.modified_entry(entry)
        self.cli.running_commands(expanded_commands)
        run_commands(*expanded_commands, background=self.args.background)

    def _should_handle_removed(self, entry: "File | Directory") -> bool:
        if type(entry) == File:
            return OperationType.FILE_REMOVED.value in self.args.operations
        if type(entry) == Directory:
            return OperationType.DIRECTORY_REMOVED.value in self.args.operations

    def _handle_removed(self, entry: "File | Directory"):
        self.states.pop(entry)

        if not self._should_handle_removed(entry):
            return

        commands = type(entry) == File and self.args.commands_on_file_remove or self.args.commands_on_directory_remove
        expanded_commands = [expand_command_variables(command, entry) for command in commands]

        self.cli.removed_entry(entry)
        self.cli.running_commands(expanded_commands)
        run_commands(*expanded_commands, background=self.args.background)

    def watch_for_changes(self):
        self.cli.watching_files([fse.path for fse in self.states])

        while True:
            previous_entries = set(self.states.keys())
            current_entries = set(fs_entries_from_patterns(self.args.patterns))

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
