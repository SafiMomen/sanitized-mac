"""
Utility functions for filesystem operations requiring user confirmation.

This module provides confirmation helpers used when a filesystem operation
may require explicit user approval before proceeding.
"""

import tkinter
from tkinter import messagebox
from pathlib import Path
from collections.abc import Callable
from textual.widgets import Input

"""
Request user confirmation before moving a large file.

Displays a native confirmation dialog containing the file name, file size,
and destination directory. The operation is approved only when the user
explicitly selects the affirmative option.

@param item_file (Path): File that is being considered for movement.
@param destination (Path): Destination directory for the file.

@return (bool): True if the user approves the move, otherwise False.
"""
def confirm_large_file_move(item_file: Path, destination: Path) -> bool:
    file_size_mb = item_file.stat().st_size / (1024 * 1024)

    root = tkinter.Tk()
    root.withdraw()

    should_move = messagebox.askyesno(
        "Large File",
        (
            f"{item_file.name} is {file_size_mb:.2f} MB.\n\n"
            f"Move it to {destination.name}?"
        ),
    )
    root.destroy()
    return should_move

"""
Resolve a filesystem path from a Textual input widget.

If the input contains no path, the supplied failure callback is invoked
with an error message and no path is returned.

@param path_input (Input): Textual input widget containing the filesystem
path supplied by the user.
@param failure (Callable[[str], None]): Callback invoked when the input is
empty. The callback receives an error message describing the failure.

@return (Path | None): Expanded filesystem path when valid input is
provided, otherwise None.
"""
def get_path_from_input(
        path_input: Input, 
        failure: Callable[[], None] | None 
) -> Path | None:
    path_folder_input = path_input.value.strip()

    if (path_folder_input):
        return Path(path_folder_input).expanduser();

    if (failure == None): return None; 
    failure("(error) enter a parent directory")