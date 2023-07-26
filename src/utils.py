from enum import Enum
from hashlib import md5
from os import stat
from pathlib import Path


def files_from_patterns(patterns: "list[str]") -> "list[str]":
    return {
        str(filename)
        for pattern in patterns
        for filename in Path("./").glob(pattern)
        if Path(filename).is_file()
    }


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
