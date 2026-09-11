from pathlib import Path
import shutil

from textual import work
from textual.app import App, ComposeResult
from textual.containers import Horizontal
from textual.widgets import Button, Input, Log, Static
from rich.text import Text

from sub_directories import SubDirectoriesHandler
from weak_file_detection import *
from weak_watchdog import DirectoryWatchdog
from file_utils import confirm_large_file_move
from style import WINDOW_STYLING

class FileJanitorApp(App):
    CSS = WINDOW_STYLING;
    # BINDINGS = [
    #     ("super+s,ctrl+s", "start", "Start"),
    #     ("super+e,ctrl+e", "stop", "Stop"),
    #     ("ctrl+q", "quit", "Quit"),
    #     ("super+l,ctrl+l", "sanitize", "Sanitize")
    # ]
    # greater than 2 gigabytes is a risk to move 
    # as it can be interrupted and hence corrupted.
    LARGE_FILE_SIZE = 2 * 1024 * 1024 * 1024

    def __init__(self) -> None:
        super().__init__()
        self._sub_directory_handler: SubDirectoriesHandler | None = None
        self._directory_watchdog: DirectoryWatchdog | None = None

    def compose(self) -> ComposeResult:
        yield Static("sanitized-os\n", id="title")
        yield Input(placeholder="parent directory: ~/Downloads", id="path")
        with Horizontal(id="controls"):
            yield Button(Text("[ start ]"), id="start")
            yield Button(Text("[ stop ]"), id="stop")
            yield Button(Text("[ quit ]"), id="quit")
        yield Static("status: stopped", id="status")
        yield Log(id="log")

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if (event.button.id == "start"):
            self.action_start()
        elif (event.button.id == "stop"):
            self.action_stop()
        elif (event.button.id == "quit"):
            self.action_quit()

    def _init_sub_directory_handler(self, parent_folder: Path) -> None :
        if (not parent_folder.is_dir()):
            self._log(f"(error) invalid directory: {parent_folder}")
            return

        sub_directories = ["%sort", "%unknown", "%unsorted"]
        for file_type, suffixes in SUPPORTED_SUFFIXES.items():
            sub_directories.append("%" + file_type)

        self._sub_directory_handler = SubDirectoriesHandler(
            parent_folder,
            sub_directories,
        )

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
            destination = self._sub_directory_handler.get_sub_directory("%" + file_type)

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
            "%sort",
            self._sub_directory_handler,
            file_processed=self._file_ready_for_processing,
        )

        self.query_one("#status", Static).update(
            f"status: watching {observing_path_folder / '%sort'}"
        )
        self._log(f"(program) watching {observing_path_folder / '%sort'}")

        self._start_watchdog()

    #otherwise the application would stop since we are running 
    #on a while loop that sleeps the thread. 
    @work(thread=True) 
    def _start_watchdog(self) -> None:
        if (self._directory_watchdog is None):
            return

        self._directory_watchdog.start_polling()

    def action_stop(self) -> None:
        if (self._directory_watchdog is None): 
            self._log(f"(error) no files are being watched")
            return

        self._directory_watchdog.stop_polling()
        self._directory_watchdog = None

        self.query_one("#status", Static).update("status: stopped")
        self._log("(program) watchdog stopped")

    def action_quit(self) -> None:
        if (self._directory_watchdog is not None):
            self._directory_watchdog.stop_polling()
        # quit the application, user doesn't want to run in the background. 
        self.exit()

    def _file_ready_for_processing(self, item_file: Path) -> None:
        if (self._sub_directory_handler is None): return

        file_type = get_file_type(item_file)
        destination = (self._sub_directory_handler.get_sub_directory(("%" + file_type)))
        shutil.move(item_file, destination)

        self.call_from_thread(
            self._file_moved,
            item_file,
            destination,
        )

    def _file_moved(self, item_file: Path, destination: Path) -> None:
        self._log(f"(program) moved {item_file.name} -> {destination.name}")

    def _log(self, message: str) -> None:
        self.query_one("#log", Log).write_line(f"[debug]::{message}")

# Main application call #
if (__name__ == "__main__"):
    FileJanitorApp().run()