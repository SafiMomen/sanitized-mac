"""
File type detection utilities for Sanitized-Mac.

This module defines supported file categories, temporary file suffixes, and
helper functions used to classify files based on their filename extension.
"""

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

"""
Determine whether a filesystem item should be considered temporary.

Hidden files and files using a known temporary download or processing
suffix are considered temporary and should not be processed normally.

@param item (Path): Filesystem item to inspect.

@return (bool): True if the item is considered temporary, otherwise False.
"""
def is_temporary_item(item: Path) -> bool:
    if item.name.startswith("."):
        return True

    return item.suffix.lower() in TEMPORARY_SUFFIXES

"""
Determine whether a file belongs to an unsupported file category.

@param item (Path): File whose type should be evaluated.

@return (bool): True if the file cannot be mapped to a supported category,
otherwise False.
"""
def is_unknown_item_type(item: Path) -> bool:
    return get_file_type(item) == "unknown"


def get_file_type(item: Path) -> str:
    suffix = item.suffix.lower()
    if (not suffix): return "unknown"
    #TODO: use datastructures to make this search faster. 
    for file_type, suffixes in SUPPORTED_SUFFIXES.items():
        if (suffix in suffixes): return file_type;
    return ("unknown")