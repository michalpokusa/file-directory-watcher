from src.utils import formatted_current_time


class CLI:
    DARK_GRAY = "\x1b[38;5;8m"
    LIGHT_GRAY = "\x1b[38;5;249m"
    GREEN = "\x1b[38;5;40m"
    YELLOW = "\x1b[38;5;220m"
    RED = "\x1b[38;5;196m"
    RESET = "\x1b[0m"

    def __init__(self, color: bool):
        if not color:
            self.DARK_GRAY = ""
            self.LIGHT_GRAY = ""
            self.GREEN = ""
            self.YELLOW = ""
            self.RED = ""
            self.RESET = ""

    def _print_prefix(self):
        print(f"{self.LIGHT_GRAY}[{self.DARK_GRAY}{formatted_current_time()}{self.LIGHT_GRAY}]{self.RESET}", end=" ",)

    def watching_files(self, files: "set[str]", _max = 10):
        self._print_prefix()
        print(
            f"Watching files:\n{', '.join(sorted(files)[:_max])}",
            f"{f'and {len(files) - _max} more...' if len(files) > _max else ''}"
        )

    def added_file(self, file_path: str):
        self._print_prefix()
        print(f"File {self.GREEN}{file_path}{self.RESET} was added")

    def modified_file(self, file_path: str):
        self._print_prefix()
        print(f"File {self.YELLOW}{file_path}{self.RESET} was modified")

    def removed_file(self, file_path: str):
        self._print_prefix()
        print(f"File {self.RED}{file_path}{self.RESET} was removed")

    def running_commands(self, commands: "list[str]"):
        commands and print('\n'.join(commands))
