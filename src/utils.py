from enum import Enum
from hashlib import md5
from multiprocessing import Process
from os import stat, system, path
from pathlib import Path
from re import match as re_match


def files_from_patterns(patterns: "list[str]") -> "list[str]":
    return {
        str(filename)
        for pattern in patterns
        for filename in Path("./").glob(pattern)
        if path.isfile(filename)
    }

def changes_in_file_lists(
        previous_files: "set[str]", current_files: "set[str]"
    ) -> "tuple[str, bool, bool, bool]":

    # Added files
    for file in current_files.difference(previous_files):
        yield file, True, False, False

    # Present in both lists
    for file in previous_files.intersection(current_files):
        yield file, False, True, False

    # Removed files
    for file in previous_files.difference(current_files):
        yield file, False, False, True


class ComparisonMethod(Enum):
    MTIME = "mtime"
    MD5 = "md5"

def file_state(
    file_path: str, comparison_method = ComparisonMethod.MTIME
):
    try:
        if comparison_method == ComparisonMethod.MTIME:
            return stat(file_path).st_mtime

        if comparison_method == ComparisonMethod.MD5:
            with open(file_path, 'rb') as f:
                file_content = f.read()
            return md5(file_content).hexdigest()
    except FileNotFoundError:
        return None

def verbose_time_to_seconds(time: str) -> float:
    pattern = r"""((?P<days>\d+)d)?((?P<hours>\d+)h)?((?P<minutes>\d+)m)?((?P<seconds>\d+(\.\d{1,2})?)s)?"""

    match = re_match(pattern, time)
    groups = match.groupdict()

    if time and tuple(groups.values()) == (None, None, None, None):
        raise ValueError(f"Invalid time format: {time}")

    days = int(groups["days"] or 0)
    hours = int(groups["hours"] or 0)
    minutes = int(groups["minutes"] or 0)
    seconds = float(groups["seconds"] or 0)

    return days * 24 * 60 * 60 + hours * 60 * 60 + minutes * 60 + seconds

def expand_variables(command: str, file_path: str) -> str:
    return command\
    .replace(r"%file_name", path.basename(file_path))\
    .replace(r"%relative_file_path", file_path)\
    .replace(r"%absolute_file_path", path.abspath(file_path))

def run_commands(*commands: "str", background=False):
    for command in commands:
        if background:
            Process(target=system, args=(command,)).start()
        else:
            system(command)
