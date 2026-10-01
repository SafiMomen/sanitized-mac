"""
Utility functions for filesystem operations requiring user confirmation.

This module provides confirmation helpers used when a filesystem operation
may require explicit user approval before proceeding.
"""

import tkinter
from tkinter import messagebox
from pathlib import Path

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