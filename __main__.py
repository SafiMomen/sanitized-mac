from textual.app import App, ComposeResult
from textual.widgets import Footer, TabbedContent, TabPane

from application_tab import ApplicationTab;
from config_tab import ConfigTab;

from style import *;

class FileJanitorApp(App):
    BINDINGS = [
        ("k", "show_tab('application')", "Application"),
        ("l", "show_tab('config')", "Config"),
    ]
    CSS = WINDOW_STYLING;

    def __init__(self) -> None:
        super().__init__()
        self._application_tab = ApplicationTab();
        self._config_tab = ConfigTab();

    def compose(self) -> ComposeResult:
        yield Footer();

        with TabbedContent(initial="application"):
            with TabPane("Application", id="application"):
                yield self._application_tab;
            with TabPane("Config", id="config"):
                yield self._config_tab;

    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab

# Main application call #
if (__name__ == "__main__"):
    FileJanitorApp().run()