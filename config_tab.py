
from textual.app import ComposeResult
from textual.widget import Widget
from textual.widgets import Static, Button

from style import WINDOW_STYLING

class ConfigTab(Widget):
    DEFAULT_CSS = WINDOW_STYLING;

    def __init__(self) -> None:
        super().__init__()

    def Compose(self) -> ComposeResult:
        yield Static("configuration\n")
        yield Button("[ open data-type file ]")
        yield Button("[ open ignored data-type file ]")
