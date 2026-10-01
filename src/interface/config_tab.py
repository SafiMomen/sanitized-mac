"""
Config tab for the Sanitized-Mac interface.

This module defines the configuration view responsible for configuring
the supported file types, temporary file types, and polling rate.
"""
import subprocess;
from pathlib import Path

from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widget import Widget
from textual.widgets import Static, Button

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
        self.actions_config_location = {
            "file-type-config": self.CONFIG_DIR / "file_types.yaml",
            "secured-config": self.CONFIG_DIR / "config.yaml"
        };

    """
    Compose the configuration tab interface.

    @return (ComposeResult): Widgets that open up configuraton files.
    """
    def compose(self) -> ComposeResult:
        yield Static("configuration\n", id="title")
        with Vertical(id="display_buttons"):
            yield Button(r"\[ open file-type config ]", id="file-type-config");
            yield Button(r"\[ open secured config ]"  , id="secured-config");

    """
    Dispatch the selected button to its corresponding configuration action.

    @param event (Button.Pressed): Event containing information about the
    button pressed by the user.
    """
    def on_button_pressed(self, event: Button.Pressed) -> None:
        config_location = self.actions_config_location.get(
            event.button.id
        );
        if (config_location == None): return None;
        subprocess.Popen(["open", config_location]);
