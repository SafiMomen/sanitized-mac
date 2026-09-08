from pathlib import Path;
from collections.abc import Callable;
import time

from sub_directories import SubDirectoriesHandler
from weak_file_detection import *

class DirectoryWatchdog:
    def __init__(
        self,
        observing_directory_name: str,
        directory_handler: SubDirectoriesHandler,
        file_processed: Callable[[Path], None]
    ) -> None:
        self._observing_directory_name = observing_directory_name;
        self._directory_handler = directory_handler;
        self._file_processed = file_processed;
        self._program_running = False;
        self._previous_file_states: dict[Path, tuple[int, float]] = {};

    def is_file_stable(self, item: Path) -> bool:
        try:
            file_stats = item.stat()
        except FileNotFoundError:
            # The file disappeared between iterdir() and stat().
            return False
        current_state = (
            file_stats.st_size,
            file_stats.st_mtime,
        )
        previous_state = self._previous_file_states.get(item)
        # Record the current state for the next poll.
        self._previous_file_states[item] = current_state
        # We have never seen this file before.
        # Wait until at least the next poll.
        if (previous_state is None):
            return False

        return (previous_state == current_state)

    def _remove_stale_file_states(self, children: list[Path]) -> None:
        current_items = set(children)

        stale_items = [
            path
            for path in self._previous_file_states
            if path not in current_items
        ]

        for path in stale_items:
            del self._previous_file_states[path]

    def _scan_directory(self, directory: Path) -> list[Path]:
        try:
            children = list(directory.iterdir())
        except FileNotFoundError:
            return []
        # Remove remembered state belonging to files that have
        # already left the directory.
        self._remove_stale_file_states(children)
        ready_files: list[Path] = []
        # Case 1: nothing needs processing.
        if (len(children) == 0): 
            return ready_files

        for item in children:
            # Case 2: don't process directories.
            if (item.is_dir()): continue
            # The item might disappear between iterdir() and here.
            if (not item.exists()): continue
            # Case 3: don't process temporary files.
            if (is_temporary_item(item)): continue
            # Case 4: unsupported file type.
            if (is_unknown_item_type(item)): continue
            # Case 5: don't touch a file while it appears to
            # still be changing.
            if (not self.is_file_stable(item)): continue
            # At this point the file appears safe for the sorter.
            ready_files.append(item)
        return ready_files

    def poll_once(self) -> list[Path]:
        self._directory_handler.process_sub_directory(
            self._observing_directory_name
        )
        directory = self._directory_handler.get_sub_directory(
            self._observing_directory_name
        )
        return self._scan_directory(directory)

    def start_polling(self, interval: float = 2.0) -> None:
        self._program_running = True
        #TODO: handle asynchronux operation so that it can run the background of computer. 
        try:
            while self._program_running:
                ready_files = self.poll_once()
                for file in ready_files:
                    self._file_processed(file);

                time.sleep(interval)
        except KeyboardInterrupt:
            print("\n[debug]::application stopped.")

        finally:
            self._program_running = False

    def stop_polling(self) -> None:
        self._program_running = False