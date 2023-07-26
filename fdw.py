from time import sleep

from src.argument_parser import FDWArgs, cli_args
from src.utils import (
    files_from_patterns,
    changes_in_file_lists,
    file_state,
)


class FDW:

    args: FDWArgs

    def __init__(self, args: FDWArgs):
        self.args = args

        self.states = {}

    def compute_starting_states(self):
        files = files_from_patterns(self.args.patterns)
        for relative_file_path in files:
            self.states.setdefault(relative_file_path, file_state(relative_file_path))

    def _compare_file_states(self, relative_file_path: str) -> bool:
        self._cached_file_state = file_state(relative_file_path)
        return self.states.get(relative_file_path) == self._cached_file_state

    def _handle_added_file(self, file_path: str):
        self.states.setdefault(file_path, file_state(file_path))

    def _handle_modified_file(self, file_path: str):
        self.states[file_path] = self._cached_file_state
        self._cached_file_state = None

    def _handle_removed_file(self, file_path: str):
        self.states.pop(file_path)

    def watch_for_changes(self):
        while True:

            previous_files = set(self.states.keys())
            current_files = files_from_patterns(self.args.patterns)

            for (relative_file_path, added, present_in_both, removed) in changes_in_file_lists(
                previous_files,
                current_files
            ):
                self.args.delay and sleep(self.args.delay)

                if added:
                    self._handle_added_file(relative_file_path)
                    continue

                if present_in_both and not self._compare_file_states(relative_file_path):
                    self._handle_modified_file(relative_file_path)
                    continue

                if removed:
                    self._handle_removed_file(relative_file_path)
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
        pass
