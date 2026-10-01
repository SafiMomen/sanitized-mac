"""
Sub-directory management utilities for Sanitized-Mac.

This module defines the handler responsible for creating, retrieving, and
enumerating application-managed sub-directories within a parent directory.
"""

from pathlib import Path;

"""
Manage application sub-directories within a parent folder.

The handler maintains a collection of expected sub-directory names and
ensures that each directory exists when the handler is initialized.
"""
class SubDirectoriesHandler:
    """
    Initialize the sub-directory handler.

    Each configured directory is processed during initialization to ensure
    that the required directory structure exists.

    @param parent_folder (Path): Parent folder containing the managed
    sub-directories.
    @param directories (list[str]): Names of the sub-directories managed
    by this handler.
    """
    def __init__(self, parent_folder: Path, directories: list[str]) -> None:
        self._parent_folder = parent_folder
        self._directories = directories
        for directory in self._directories:
            self.process_sub_directory(directory_name=directory)

    """
    Resolve the path of a managed sub-directory.

    @param directory_name (str): Name of the sub-directory to resolve.

    @return (Path): Path representing the requested sub-directory within
    the configured parent folder.
    """
    def get_sub_directory(self, directory_name: str) -> Path:
        return self._parent_folder / directory_name;

    """
    Retrieve all managed sub-directory paths.

    @return (list[Path]): Paths representing each configured
    sub-directory.
    """
    def get_sub_directories(self) -> list[Path]:
        sub_directories: list[Path] = []
        for directory in self._directories:
            directory_path = self.get_sub_directory(directory)
            sub_directories.append(directory_path)
        return sub_directories        

    """
    Ensure that a managed sub-directory exists.

    If the requested directory already exists, no filesystem changes are
    made. Otherwise, the directory and any missing parent directories are
    created.

    @param directory_name (str): Name of the sub-directory to process.
    """
    def process_sub_directory(self, directory_name: str) -> None:
        directory_path = self.get_sub_directory(directory_name)
        if (directory_path.exists()):
            return
        # doesn't exist, make it, it is save to retrieve later. 
        directory_path.mkdir(parents=True, exist_ok=True);