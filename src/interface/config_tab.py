"""
Config tab for the Sanitized-Mac interface.

This module defines the configuration view responsible for configuring
the supported file types, temporary file types, and polling rate.
"""
import subprocess;
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widget import Widget
from textual.widgets import Static, Button, Input

from src.process.migrate_process import migrate_to_current_version;
from src.process.uninstall_process import uninstall_directory;
from src.core.file_utils import *

from src.interface.style import WINDOW_STYLING

class ConfigTab(Widget):
    CONFIG_DIR = Path(__file__).resolve().parent.parent / "config";

    DEFAULT_CSS = WINDOW_STYLING;

    """
    TODO: Possibly check if certain files are missing, and if so make them.
    TODO: Possibly save these configuration in user files in the OS 
    as opposed to locally to avoid re-configuration upon installing.
    """
    def __init__(self) -> None:
        super().__init__()
        self._actions_config_location = {
            "file-type-config": self.CONFIG_DIR / "file_types.yaml",
            "secured-config": self.CONFIG_DIR / "config.yaml"
        };
        self._actions_processes = {
            "migrate-action": self._migrate_process,
            "uninstall-action": self._uninstall_process
        };

    """
    Compose the configuration tab interface.

    @return (ComposeResult): Widgets that open up configuraton files.
    """
    def compose(self) -> ComposeResult:
        yield Static("configuration\n", id="title")
        with Vertical(id="display_buttons"):
            yield Button(r"\[ open file-type config ]", id="file-type-config");
            yield Button(r"\[ open secured config ]", id="secured-config");

            yield Input(placeholder="directory: ~/Downloads", id="process-path");
            with Horizontal(id="process_buttons"):
                yield Button(r"\[ migrate version ]", id="migrate-action");
                yield Button(r"\[ uninstall ]", id="uninstall-action");

    """
    Dispatch the selected button to its corresponding configuration action.

    @param event (Button.Pressed): Event containing information about the
    button pressed by the user.
    """
    def on_button_pressed(self, event: Button.Pressed) -> None:
        config_location = self._actions_config_location.get(
            event.button.id
        );
        if (config_location != None):
            subprocess.Popen(["open", config_location]);
            return;

        process = self._actions_processes.get(event.button.id);
        if (process != None): process();

    """
    Migrate a selected directory to the application's current version.

    Retrieves the directory from the path input and passes
    the supplied path to the version migration process. The migration process
    is responsible for updating the directory structure or configuration to
    match the application's current expected format.
    """
    def _migrate_process(self) -> None: 
        path_input = self.query_one("#process-path", Input);
        migrating_path = get_path_from_input(path_input);
        if (migrating_path == None): return;
        migrate_to_current_version(migrating_path);

    """
    uninstall a selected directory and remove mac-os sanitizer.

    Retrieves the directory from the path input and passes
    the supplied path to the uninstall process. The uninstall process
    is responsible for removing all Sanitized-Mac formatting.
    The children of folders will return back to parent input directory, 
    and the folders will be destroyed. 
    """
    def _uninstall_process(self) -> None:
        path_input = self.query_one("#process-path", Input);
        uninstall_path = get_path_from_input(path_input);
        if (uninstall_path == None): return;
        uninstall_directory(uninstall_path);

        
