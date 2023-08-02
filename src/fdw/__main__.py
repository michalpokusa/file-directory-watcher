from sys import exit as sys_exit

from file_directory_watcher.argument_parser import cli_args
from file_directory_watcher.app import FDW


def main():
    try:
        app = FDW(cli_args)
        app.compute_starting_states()
        app.watch_for_changes()
    except KeyboardInterrupt:
        sys_exit(0)

if __name__ == "__main__":
    main()
