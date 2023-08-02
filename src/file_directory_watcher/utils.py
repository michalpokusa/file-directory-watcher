from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from hashlib import md5
from multiprocessing import Process
from os import stat, system, path as os_path
from pathlib import Path
from re import match as re_match


def formatted_current_time(format: str = "%Y-%m-%d %H:%M:%S"):
    return datetime.now().strftime(format)

@dataclass
class _FSEntry:
    path: str

    def __hash__(self) -> int:
        return hash(self.path)

class File(_FSEntry):
    pass

class Directory(_FSEntry):
    pass


def fs_entries_from_patterns(patterns: "list[str]") -> "File | Directory":
    for pattern in patterns:
        for _path in Path("./").glob(pattern):
            if os_path.isfile(_path):
                yield File(str(_path))
            elif os_path.isdir(_path):
                yield Directory(str(_path))


class OperationType(Enum):
    FILE_CHANGED = "file_changed"
    FILE_ADDED = "file_added"
    FILE_MODIFIED = "file_modified"
    FILE_REMOVED = "file_removed"
    DIRECTORY_CHANGED = "directory_changed"
    DIRECTORY_ADDED = "directory_added"
    DIRECTORY_MODIFIED = "directory_modified"
    DIRECTORY_REMOVED = "directory_removed"

    @staticmethod
    def all():
        return tuple(operation_type.value for operation_type in OperationType)


def changes_in_entries(
        previous_entries: "set[File | Directory]", current_entries: "set[File | Directory]"
    ) -> "tuple[File | Directory, bool, bool, bool]":

    # Added entries
    for entry in current_entries.difference(previous_entries):
        yield entry, True, False, False

    # Present in both sets
    for entry in previous_entries.intersection(current_entries):
        yield entry, False, True, False

    # Removed entries
    for entry in previous_entries.difference(current_entries):
        yield entry, False, False, True


class CompareMethod(Enum):
    MTIME = "mtime"
    SIZE = "size"
    MD5 = "md5"

    def for_files() -> "list[str]":
        return (CompareMethod.MTIME.value, CompareMethod.SIZE.value, CompareMethod.MD5.value)

    def for_directories() -> "list[str]":
        return (CompareMethod.MTIME.value,)


def compute_state(fs_entry: "File | Directory", compare_method = CompareMethod.MTIME):
    try:
        if compare_method == CompareMethod.MTIME.value:
            return stat(fs_entry.path).st_mtime

        if compare_method == CompareMethod.SIZE.value:
            return stat(fs_entry.path).st_size

        if compare_method == CompareMethod.MD5.value:
            with open(fs_entry.path, 'rb') as f:
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

def expand_command_variables(command: str, entry: "File | Directory") -> str:
    return command\
    .replace(r"%name", os_path.basename(entry.path))\
    .replace(r"%relative_path", entry.path)\
    .replace(r"%absolute_path", os_path.abspath(entry.path))

def run_commands(*commands: "str", background=False):
    for command in commands:
        if background:
            Process(target=system, args=(command,)).start()
        else:
            system(command)
