"""
Main Textual application for Sanitized-Mac.

This module defines the primary application window and coordinates navigation
between the application's main interface and configuration interface.
"""

from textual.app import App, ComposeResult
from textual.widgets import Footer, TabbedContent, TabPane

from src.interface.application_tab import ApplicationTab;
from src.interface.config_tab import ConfigTab;

from src.interface.style import *;

class FileJanitorApp(App):
    """
    The application contains two primary tabs:

    - Application: Provides access to the core File Janitor functionality.
    - Config: Provides access to application configuration options.
    """
    BINDINGS = [
        ("k", "show_tab('application')", "Application"),
        ("l", "show_tab('config')", "Config"),
    ]
    CSS = WINDOW_STYLING;

    """
    Creates the application and configuration tab components that are
    mounted into the application's tabbed interface during composition.

    Created in constructor to cache the functionality; and Textual re-composes upon update. 

    @return: None
    """
    def __init__(self) -> None:
        super().__init__()
        self._application_tab = ApplicationTab();
        self._config_tab = ConfigTab();

    """
    Compose the application's user interface.

    The Application tab is selected by default when the program starts.

    Yields:
        Textual widgets that make up the application's primary interface.
    
    @return: A ComposeResult containing the widgets that make up the primary
        application interface. It is used internally when called .run() by Textual.
    """
    def compose(self) -> ComposeResult:
        yield Footer();

        with TabbedContent(initial="application"):
            with TabPane("Application", id="application"):
                yield self._application_tab;
            with TabPane("Config", id="config"):
                yield self._config_tab;

    """
    Switch the currently active application tab.

    @param tab (str): Identifier of the tab to activate. Must correspond
        to the ID of a TabPane contained within the application's
        TabbedContent widget.
    """
    def action_show_tab(self, tab: str) -> None:
        self.get_child_by_type(TabbedContent).active = tab

"""
Only start the Textual application when this file is executed directly.
Importing this module from another file will not automatically run the app.
"""
if (__name__ == "__main__"):
    FileJanitorApp().run()