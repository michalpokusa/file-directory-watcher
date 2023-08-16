from dataclasses import dataclass
from datetime import datetime
from hashlib import md5
from multiprocessing import Process
from os import stat, path as os_path
from pathlib import Path
from subprocess import run, PIPE

from .const import MTIME, ATIME, CTIME, MODE, SIZE, MD5, UID, GID


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


def fs_entries_from_patterns(
    patterns: "list[str]",
    exclude_patterns: "list[str]",
) -> "File | Directory":
    entries = set()

    for pattern in patterns:

        # Direct path without glob
        if "*" not in pattern:
            if os_path.isfile(pattern):
                entries.add(File(os_path.abspath(pattern)))
            elif os_path.isdir(pattern):
                entries.add(Directory(os_path.abspath(pattern)))
            continue

        # Path with glob
        split_point = pattern.index("*")
        base_path, glob_pattern = pattern[:split_point], pattern[split_point:]

        for entry in Path(base_path).expanduser().resolve().glob(glob_pattern):
            if os_path.isfile(entry):
                entries.add(File(str(entry)))
            elif os_path.isdir(entry):
                entries.add(Directory(str(entry)))

    if not exclude_patterns:
        return entries

    return entries - fs_entries_from_patterns(exclude_patterns, [])

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

def compute_state(fs_entry: "File | Directory", compare_methods = MTIME):
    state = ""
    fs_entry_stat = stat(fs_entry.path)

    for compare_method in compare_methods:
        try:
            if compare_method == MTIME:
                state += f"mtime={fs_entry_stat.st_mtime};"

            if compare_method == ATIME:
                state += f"atime={fs_entry_stat.st_atime};"

            if compare_method == CTIME:
                state += f"ctime={fs_entry_stat.st_ctime};"

            if compare_method == MODE:
                state += f"mode={fs_entry_stat.st_mode};"

            if compare_method == SIZE:
                state += f"size={fs_entry_stat.st_size};"

            if compare_method == UID:
                state += f"uid={fs_entry_stat.st_uid};"

            if compare_method == GID:
                state += f"gid={fs_entry_stat.st_gid};"

            if compare_method == MD5:
                with open(fs_entry.path, 'rb') as f:
                    file_content = f.read()
                state += f"md5={md5(file_content).hexdigest()};"
        except FileNotFoundError:
            return None
    return state

def expand_command_variables(command: str, entry: "File | Directory") -> str:
    return command\
    .replace(r"%name", os_path.basename(entry.path))\
    .replace(r"%relative_path", os_path.relpath(entry.path))\
    .replace(r"%absolute_path", os_path.abspath(entry.path))

def run_command(command: str, background:bool = False):
    if background:
        Process(
            target=run,
            args=(command,),
            kwargs={
                "stdin": PIPE,
                "shell": True
            }
        ).start()
    else:
        run(command, stdin=PIPE, shell=True)
