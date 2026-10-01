"""
Directory polling and file readiness utilities for Sanitized-Mac.

This module defines a lightweight directory watchdog responsible for polling
a managed sub-directory, detecting files that appear stable and safe to
process, and forwarding those files to a configured processing callback.

The official watchdog library might be too heavy for simple application.
"""

from pathlib import Path;
from collections.abc import Callable;
import time

from src.core.sub_directories import SubDirectoriesHandler
from src.core.weak_file_detection import *

"""
Monitor a managed sub-directory for files that are ready for processing.

The watchdog periodically scans a configured directory and filters out
directories, temporary files, unsupported file types, and files that
appear to still be changing.

Files that pass all readiness checks are forwarded to the configured
file-processing callback.
"""
class DirectoryWatchdog:
    """
    Initialize the directory watchdog.

    @param observing_directory_name (str): Name of the managed
    sub-directory that should be monitored.
    @param directory_handler (SubDirectoriesHandler): Handler responsible
    for creating and resolving managed sub-directories.
    @param file_processed (Callable[[Path], None]): Callback invoked for
    each file determined to be ready for processing.
    """
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

    """
    Determine whether a file has remained unchanged between polling cycles.

    File stability is determined by comparing the current file size and
    modification timestamp against the values recorded during the previous
    polling cycle.

    A file that has not previously been observed is considered unstable
    until a subsequent poll confirms that its state has not changed.

    @param item (Path): File whose stability should be evaluated.

    @return (bool): True if the file size and modification timestamp are
    unchanged since the previous poll, otherwise False.
    """
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

    """
    Remove stored state for items no longer present in the watched directory.

    Prevents the internal file-state collection from retaining information
    about files that have already been moved, deleted, or otherwise removed.

    @param children (list[Path]): Current contents of the watched directory.
    """
    def _remove_stale_file_states(self, children: list[Path]) -> None:
        current_items = set(children)

        stale_items = [
            path
            for path in self._previous_file_states
            if path not in current_items
        ]

        for path in stale_items:
            del self._previous_file_states[path]

    """
    Scan a directory and identify files that are ready for processing.

    Directories, missing items, temporary files, unsupported file types,
    and unstable files are excluded from the returned collection.

    @param directory (Path): Directory whose immediate contents should be
    inspected.

    @return (list[Path]): Files that passed all readiness checks and may
    safely be forwarded for processing.
    """
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

    """
    Perform a single polling cycle on the configured directory.

    Ensures that the watched sub-directory exists, resolves its path, and
    scans its contents for files that are ready for processing.

    @return (list[Path]): Files determined to be ready during the current
    polling cycle.
    """
    def poll_once(self) -> list[Path]:
        self._directory_handler.process_sub_directory(
            self._observing_directory_name
        )
        directory = self._directory_handler.get_sub_directory(
            self._observing_directory_name
        )
        return self._scan_directory(directory)

    """
    Continuously poll the configured directory for processable files.

    Each polling cycle identifies ready files and forwards them to the
    configured processing callback. Polling continues until stop_polling()
    is called or the process receives a keyboard interruption.

    @param interval (float): Number of seconds to wait between polling
    cycles.
    """
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

    """
    Request termination of the active polling loop.

    The polling loop exits after the current cycle completes and evaluates
    the updated running state.
    """
    def stop_polling(self) -> None:
        self._program_running = False