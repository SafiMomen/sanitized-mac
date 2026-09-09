from pathlib import Path

TEMPORARY_SUFFIXES = {
    ".crdownload",
    ".download",
    ".part",
    ".partial",
    ".tmp",
    ".temp",
}

SUPPORTED_SUFFIXES = {
    "document": {
        ".pdf",
        ".txt",
        ".doc",
        ".docx",
        ".rtf",
        ".odt",
        ".md",
        ".tex",
    },
    "spreadsheet": {
        ".csv",
        ".xls",
        ".xlsx",
        ".ods",
    },
    "presentation": {
        ".ppt",
        ".pptx",
        ".odp",
    },
    "image": {
        ".png",
        ".jpg",
        ".jpeg",
        ".gif",
        ".webp",
        ".heic",
        ".bmp",
        ".tiff",
        ".tif",
        ".svg",
    },
    "audio": {
        ".mp3",
        ".wav",
        ".aac",
        ".flac",
        ".m4a",
        ".ogg",
        ".opus",
    },
    "video": {
        ".mp4",
        ".mov",
        ".avi",
        ".mkv",
        ".webm",
        ".m4v",
    },
    "archive": {
        ".zip",
        ".tar",
        ".gz",
        ".rar",
        ".7z",
        ".bz2",
        ".xz",
    },
    "installer": {
        ".dmg",
        ".pkg",
        ".exe",
        ".msi",
        ".deb",
        ".rpm",
    },
}


def is_temporary_item(item: Path) -> bool:
    if item.name.startswith("."):
        return True

    return item.suffix.lower() in TEMPORARY_SUFFIXES


def is_unknown_item_type(item: Path) -> bool:
    return get_file_type(item) == "unknown"


def get_file_type(item: Path) -> str:
    suffix = item.suffix.lower()
    if (not suffix): return "unknown"
    #TODO: use datastructures to make this search faster. 
    for file_type, suffixes in SUPPORTED_SUFFIXES.items():
        if (suffix in suffixes): return file_type;
    return ("unknown")