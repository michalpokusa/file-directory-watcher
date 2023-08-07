from re import match as re_match

from .const import (
    FILE_CHANGED, FC,
    FILE_ADDED, FA,
    FILE_MODIFIED, FM,
    FILE_REMOVED, FR,
    DIRECTORY_CHANGED, DC,
    DIRECTORY_ADDED, DA,
    DIRECTORY_MODIFIED, DM,
    DIRECTORY_REMOVED, DR,
)

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

def determine_operations(only: "set[str]", ignored: "set[str]"):
    output = set()

    translate_map = {
        FC: (FC, FILE_CHANGED, FA, FILE_ADDED, FM, FILE_MODIFIED, FR, FILE_REMOVED),
        FILE_CHANGED: (FC, FILE_CHANGED, FA, FILE_ADDED, FM, FILE_MODIFIED, FR, FILE_REMOVED),
        FA: (FA, FILE_ADDED),
        FILE_ADDED: (FA, FILE_ADDED),
        FM: (FM, FILE_MODIFIED),
        FILE_MODIFIED: (FM, FILE_MODIFIED),
        FR: (FR, FILE_REMOVED),
        FILE_REMOVED: (FR, FILE_REMOVED),
        DC: (DC, DIRECTORY_CHANGED, DA, DIRECTORY_ADDED, DM, DIRECTORY_MODIFIED, DR, DIRECTORY_REMOVED),
        DIRECTORY_CHANGED: (DC, DIRECTORY_CHANGED, DA, DIRECTORY_ADDED, DM, DIRECTORY_MODIFIED, DR, DIRECTORY_REMOVED),
        DA: (DA, DIRECTORY_ADDED),
        DIRECTORY_ADDED: (DA, DIRECTORY_ADDED),
        DM: (DM, DIRECTORY_MODIFIED),
        DIRECTORY_MODIFIED: (DM, DIRECTORY_MODIFIED),
        DR: (DR, DIRECTORY_REMOVED),
        DIRECTORY_REMOVED: (DR, DIRECTORY_REMOVED),
    }

    for value in only:
        output.update(translate_map.get(value, []))

    for value in ignored:
        output.difference_update(translate_map.get(value, []))

    return output
