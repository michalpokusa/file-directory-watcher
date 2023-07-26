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

    def watch_for_changes(self):
        while True:

            previous_files = set(self.states.keys())
            current_files = files_from_patterns(self.args.patterns)

            for (relative_file_path, added, present_in_both, removed) in changes_in_file_lists(
                previous_files,
                current_files
            ):
                self.args.delay and sleep(self.args.delay)

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
