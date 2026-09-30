"""
Application tab for the Sanitized-Mac interface.

This module defines the main application view responsible for configuring
a target directory, starting and stopping directory monitoring, manually
sanitizing directories, and displaying file-processing activity.
"""

from pathlib import Path
import shutil

from textual import work
from textual.app import ComposeResult
from textual.widget import Widget
from textual.containers import Horizontal
from textual.widgets import Button, Input, Log, Static
from rich.text import Text

from sub_directories import SubDirectoriesHandler
from weak_file_detection import *
from weak_watchdog import DirectoryWatchdog
from file_utils import confirm_large_file_move
from style import WINDOW_STYLING

class ApplicationTab(Widget):
    """
    Main application interface for directory sanitization and monitoring.

    The tab allows the user to select a parent directory, manually sanitize
    its files, or start a background watchdog that continuously processes
    files placed inside the `.sort` subdirectory.
    """
    DEFAULT_CSS = WINDOW_STYLING;
    """
    greater than 2 gigabytes is a risk to move 
    as it can be interrupted and hence corrupted.
    """
    LARGE_FILE_SIZE = (2 * 1024 * 1024 * 1024)

    """
    Initializes references to the sub-directory handler and watchdog.
    These components are created when the user starts monitoring or
    sanitizing a directory.

    _sub_directory_handler is a utility class for persisting folders search.
    _directory_watchdog is the polling implementation for the sort folder. 
    """
    def __init__(self) -> None:
        super().__init__()
        self._sub_directory_handler: SubDirectoriesHandler | None = None
        self._directory_watchdog: DirectoryWatchdog | None = None

    """
    Compose the application tab interface.

    @return (ComposeResult): Widgets that make up the application tab.
    """
    def compose(self) -> ComposeResult:
        yield Static("sanitized-os\n", id="title")
        yield Input(placeholder="parent directory: ~/Downloads", id="path")
        with Horizontal(id="controls"):
            yield Button(Text("[ start ]"), id="start")
            yield Button(Text("[ stop ]"), id="stop")
            yield Button(Text("[ sanitize ]"), id="sanitize")
        yield Static("status: stopped", id="status")
        yield Log(id="log")

    """
    Dispatch the selected button to its corresponding application action.

    @param event (Button.Pressed): Event containing information about the
    button pressed by the user.
    """
    def on_button_pressed(self, event: Button.Pressed) -> None:
        actions_method_map = {
            "start": self.action_start,
            "stop": self.action_stop,
            "sanitize": self.action_sanitize
        }
        method_callback = actions_method_map.get(event.button.id);
        if (method_callback): method_callback();

    """
    Initialize the managed sub-directory structure for a parent folder.

    Creates the standard `.sort`, `.unknown`, and `.unsorted` directories,
    along with a generated directory for each supported file type.

    @param parent_folder (Path): Parent folder where managed sub-directories
    should be initialized.
    """
    def _init_sub_directory_handler(self, parent_folder: Path) -> None :
        if (not parent_folder.is_dir()):
            self._log(f"(error) invalid directory: {parent_folder}")
            return

        sub_directories = [".sort", ".unknown", ".unsorted"]
        for file_type, suffixes in SUPPORTED_SUFFIXES.items():
            sub_directories.append("." + file_type)

        self._sub_directory_handler = SubDirectoriesHandler(
            parent_folder,
            sub_directories,
        )

    """
    Sanitize all regular files in the selected parent directory.
    This is for one-time usage for users, as opposed to polling.

    Each supported file is classified and moved into its corresponding
    generated sub-directory. Temporary files are skipped. Files larger
    than or equal to LARGE_FILE_SIZE require user confirmation before
    being moved.
    """
    def action_sanitize(self) -> None:
        path_input = self.query_one("#path", Input)
        sanitizing_path_folder_input = path_input.value.strip()
        if (not sanitizing_path_folder_input):
            self._log("(error) enter a parent directory")
            return

        sanitizing_path_folder = Path(
            sanitizing_path_folder_input
        ).expanduser()

        self._init_sub_directory_handler(sanitizing_path_folder);
        self._log(f"(program) attempting to sanitize: {sanitizing_path_folder}")

        files = [
            item_file
            for item_file in sanitizing_path_folder.iterdir()
            if item_file.is_file()
        ]
        for item_file in files:
            file_type = get_file_type(item_file)
            destination = self._sub_directory_handler.get_sub_directory("." + file_type)

            if (is_temporary_item(item_file)): continue

            if (item_file.stat().st_size >= self.LARGE_FILE_SIZE):
                should_move = confirm_large_file_move(
                    item_file,
                    destination,
                )
                if (not should_move):
                    self._log(f"(program) skipped large file: {item_file.name}")
                    continue

            shutil.move(item_file, destination)

            self._file_moved(item_file, destination)

        self._log(f"(program) sanitize complete")

    """
    Start monitoring the selected directory's `.sort` sub-directory.
    Meant to run in the user background. 

    Initializes the managed sub-directory structure and starts a
    DirectoryWatchdog configured to process files placed inside `.sort`.
    """
    def action_start(self) -> None:
        path_input = self.query_one("#path", Input)
        observing_path_folder_input = path_input.value.strip()

        if (not observing_path_folder_input):
            self._log("(error) enter a parent directory")
            return

        observing_path_folder = Path(
            observing_path_folder_input
        ).expanduser()

        self._init_sub_directory_handler(observing_path_folder)
        self._directory_watchdog = DirectoryWatchdog(
            ".sort",
            self._sub_directory_handler,
            file_processed=self._file_ready_for_processing,
        )

        self.query_one("#status", Static).update(
            f"status: watching {observing_path_folder / '.sort'}"
        )
        self._log(f"(program) watching {observing_path_folder / '.sort'}")

        self._start_watchdog()

    """
    Start the directory watchdog on a background worker thread.

    Running the watchdog on a worker thread prevents its polling loop from
    blocking the Textual interface.

    otherwise the application would stop since we are running 
    on a while loop that sleeps the thread. 
    """
    @work(thread=True) 
    def _start_watchdog(self) -> None:
        if (self._directory_watchdog is None):
            return

        self._directory_watchdog.start_polling()

    """
    Stop the currently active directory watchdog.

    If no watchdog is active, an error is written to the application log.
    """
    def action_stop(self) -> None:
        if (self._directory_watchdog is None): 
            self._log(f"(error) no files are being watched")
            return

        self._directory_watchdog.stop_polling()
        self._directory_watchdog = None

        self.query_one("#status", Static).update("status: stopped")
        self._log("(program) watchdog stopped")

    """
    Process a file reported as ready by the directory watchdog.

    The file type is detected, the corresponding destination directory is
    resolved, and the file is moved into that directory.

    This is needed because downloading items might be moved, and the download linkage might break. 

    @param item_file (Path): File determined by the watchdog to be ready
    for processing.
    """
    def _file_ready_for_processing(self, item_file: Path) -> None:
        if (self._sub_directory_handler is None): return

        file_type = get_file_type(item_file)
        destination = (self._sub_directory_handler.get_sub_directory(("." + file_type)))
        shutil.move(item_file, destination)

        self.app.call_from_thread(
            self._file_moved,
            item_file,
            destination,
        )

    """
    Record a successful file movement in the application log.

    @param item_file (Path): File that was moved.
    @param destination (Path): Destination directory receiving the file.
    """
    def _file_moved(self, item_file: Path, destination: Path) -> None:
        self._log(f"(program) moved {item_file.name} -> {destination.name}")

    """
    Append a formatted message to the application activity log.

    @param message (str): Message to display in the log.
    """
    def _log(self, message: str) -> None:
        self.query_one("#log", Log).write_line(f"[debug]::{message}")
