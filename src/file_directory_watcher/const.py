
# Operations
FILE_CHANGED, FC = "file_changed", "fc"
FILE_ADDED, FA = "file_added", "fa"
FILE_MODIFIED, FM = "file_modified", "fm"
FILE_REMOVED, FR = "file_removed", "fr"
DIRECTORY_CHANGED, DC = "directory_changed", "dc"
DIRECTORY_ADDED, DA = "directory_added", "da"
DIRECTORY_MODIFIED, DM = "directory_modified", "dm"
DIRECTORY_REMOVED, DR = "directory_removed", "dr"

ALL_OPERATIONS: "tuple[str]" = (
    FILE_CHANGED, FC,
    FILE_ADDED, FA,
    FILE_MODIFIED, FM,
    FILE_REMOVED, FR,
    DIRECTORY_CHANGED, DC,
    DIRECTORY_ADDED, DA,
    DIRECTORY_MODIFIED, DM,
    DIRECTORY_REMOVED, DR,
)

# Compare methods
MTIME = "mtime"
ATIME = "atime"
CTIME = "ctime"
MODE = "mode"
SIZE = "size"
MD5 = "md5"
UID = "uid"
GID = "gid"

FILE_COMPARE_METHODS: "tuple[str]" = (MTIME, ATIME, CTIME, SIZE, MD5, MODE, UID, GID)
DIRECTORY_COMPARE_METHODS: "tuple[str]" = (MTIME, ATIME, CTIME, MODE, UID, GID)

# Verbosity
LIMITED = 0
NORMAL = 1
FULL = 2

VERBOSITY_LEVELS: "tuple[int]" = ("limited", "normal", "full")
