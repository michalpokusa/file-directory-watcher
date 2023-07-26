from src.utils import formatted_current_time


class CLI:
    DARK_GRAY = "\x1b[38;5;8m"
    LIGHT_GRAY = "\x1b[38;5;249m"
    GREEN = "\x1b[38;5;40m"
    YELLOW = "\x1b[38;5;220m"
    RED = "\x1b[38;5;196m"
    RESET = "\x1b[0m"


    @staticmethod
    def _print_prefix():
        print(f"{CLI.LIGHT_GRAY}[{CLI.DARK_GRAY}{formatted_current_time()}{CLI.LIGHT_GRAY}]{CLI.RESET}", end=" ",)

    @staticmethod
    def watching_files(files: "set[str]", _max = 10):
        CLI._print_prefix()
        print(
            f"Watching files:\n{', '.join(sorted(files)[:_max])}",
            f"{f'and {len(files) - _max} more...' if len(files) > _max else ''}"
        )

    @staticmethod
    def added_file(file_path: str):
        CLI._print_prefix()
        print(f"File {CLI.GREEN}{file_path}{CLI.RESET} was added")

    @staticmethod
    def modified_file(file_path: str):
        CLI._print_prefix()
        print(f"File {CLI.YELLOW}{file_path}{CLI.RESET} was modified")

    @staticmethod
    def removed_file(file_path: str):
        CLI._print_prefix()
        print(f"File {CLI.RED}{file_path}{CLI.RESET} was removed")

    @staticmethod
    def running_commands(commands: "list[str]"):
        commands and print('\n'.join(commands))
