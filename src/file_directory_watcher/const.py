
# Operations
FILE_CHANGED = "file_changed"
FILE_ADDED = "file_added"
FILE_MODIFIED = "file_modified"
FILE_REMOVED = "file_removed"
DIRECTORY_CHANGED = "directory_changed"
DIRECTORY_ADDED = "directory_added"
DIRECTORY_MODIFIED = "directory_modified"
DIRECTORY_REMOVED = "directory_removed"

ALL_OPERATIONS: "tuple[str]" = (
    FILE_CHANGED,
    FILE_ADDED,
    FILE_MODIFIED,
    FILE_REMOVED,
    DIRECTORY_CHANGED,
    DIRECTORY_ADDED,
    DIRECTORY_MODIFIED,
    DIRECTORY_REMOVED,
)

# Compare methods
MTIME = "mtime"
MODE = "mode"
SIZE = "size"
MD5 = "md5"
UID = "uid"
GID = "gid"

FILE_COMPARE_METHODS: "tuple[str]" = (MTIME, SIZE, MD5, MODE, UID, GID)
DIRECTORY_COMPARE_METHODS: "tuple[str]" = (MTIME, MODE, UID, GID)

# Verbosity
LIMITED = 0
NORMAL = 1
FULL = 2

VERBOSITY_LEVELS: "tuple[int]" = ("limited", "normal", "full")
