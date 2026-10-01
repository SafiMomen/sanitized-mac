"""
File type detection utilities for Sanitized-Mac.

This module defines supported file categories, temporary file suffixes, and
helper functions used to classify files based on their filename extension.
"""

from pathlib import Path
import yaml;

DEFAULT_FILE_TYPES = (
    Path(__file__).resolve().parent.parent
    / "config"
    / "default.yaml"
);
with DEFAULT_FILE_TYPES.open("r") as default_file_types:
    file_types = yaml.safe_load(default_file_types);

TEMPORARY_SUFFIXES = file_types["temporary_suffixes"];
SUPPORTED_SUFFIXES = file_types["supported_suffixes"];

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
Determine the category associated with a file's extension.

The file suffix is normalized to lowercase and compared against the
suffixes registered in SUPPORTED_SUFFIXES. Files without an extension or
without a matching category are classified as unknown.

@param item (Path): File whose category should be determined.

@return (str): Supported file category associated with the file, or
"unknown" when no supported category can be determined.
"""
def get_file_type(item: Path) -> str:
    suffix = item.suffix.lower()
    if (not suffix): return "unknown"
    #TODO: use datastructures to make this search faster. 
    for file_type, suffixes in SUPPORTED_SUFFIXES.items():
        if (suffix in suffixes): return file_type;
    return ("unknown");

"""
Determine whether a file belongs to an unsupported file category.

@param item (Path): File whose type should be evaluated.

@return (bool): True if the file cannot be mapped to a supported category,
otherwise False.
"""
def is_unknown_item_type(item: Path) -> bool:
    return get_file_type(item) == "unknown"