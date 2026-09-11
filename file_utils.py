import tkinter
from tkinter import messagebox
from pathlib import Path

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