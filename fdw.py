from sys import exit as sys_exit
from time import sleep

from src.argument_parser import FDWArgs, cli_args
from src.cli import CLI
from src.utils import (
    File,
    Directory,
    fs_entries_from_patterns,
    changes_in_entries,
    compute_state,
    expand_variables,
    run_commands,
)


class FDW:

    args: FDWArgs

    def __init__(self, args: FDWArgs):
        self.args = args
        self.args.commands_on_add += self.args.commands_on_change
        self.args.commands_on_modify += self.args.commands_on_change
        self.args.commands_on_remove += self.args.commands_on_change

        self.cli = CLI(self.args.color)
        self.states: "dict[File | Directory]" = {}

    def compute_starting_states(self):
        for entry in fs_entries_from_patterns(self.args.patterns):
            self.states.setdefault(
                entry,
                compute_state(
                    entry,
                    self.args.file_compare_method,
                    self.args.directory_compare_method
                )
            )

    def _compare_file_states(self, entry: "File | Directory") -> bool:
        self._cached_entry_state = compute_state(
            entry,
            self.args.file_compare_method,
            self.args.directory_compare_method
        )
        return self.states.get(entry) == self._cached_entry_state

    def _handle_added(self, entry: "File | Directory"):
        self.states.setdefault(
            entry,
            compute_state(
                entry,
                self.args.file_compare_method,
                self.args.directory_compare_method
            )
        )

        expanded_commands = [
            expand_variables(command, entry)
            for command in self.args.commands_on_add
        ]

        self.cli.added_entry(entry)
        self.cli.running_commands(expanded_commands)
        run_commands(*expanded_commands, background=self.args.background)

    def _handle_modified(self, entry: "File | Directory"):
        self.states[entry] = self._cached_entry_state
        self._cached_entry_state = None

        expanded_commands = [
            expand_variables(command, entry)
            for command in self.args.commands_on_modify
        ]

        self.cli.modified_entry(entry)
        self.cli.running_commands(expanded_commands)
        run_commands(*expanded_commands, background=self.args.background)

    def _handle_removed(self, entry: "File | Directory"):
        self.states.pop(entry)

        expanded_commands = [
            expand_variables(command, entry)
            for command in self.args.commands_on_remove
        ]

        self.cli.removed_entry(entry)
        self.cli.running_commands(expanded_commands)
        run_commands(*expanded_commands, background=self.args.background)

    def watch_for_changes(self):
        self.cli.watching_files([fse.path for fse in self.states])

        while True:
            previous_entries = set(self.states.keys())
            current_entries = set(fs_entries_from_patterns(self.args.patterns))

            for (entry, added, present_in_both, removed) in changes_in_entries(
                previous_entries,
                current_entries
            ):
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


def main():
    app = FDW(cli_args)
    app.compute_starting_states()
    app.watch_for_changes()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys_exit(0)
