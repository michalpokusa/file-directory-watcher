from src.argument_parser import FDWArgs, cli_args
from src.utils import (
    files_from_patterns,
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

def main():

    app = FDW(cli_args)
    app.compute_starting_states()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
