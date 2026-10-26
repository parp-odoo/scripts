"""Terminal presentation shared by the CLI command handlers."""

import typer
from rich.console import Console
from simple_term_menu import TerminalMenu


def get_selection(entries, title="", clear_screen=True):
    return TerminalMenu(
        list(entries), title=title, menu_cursor="> ",
        menu_cursor_style=("fg_yellow", "bold"),
        menu_highlight_style=("fg_cyan", "bold", "italics"),
        cycle_cursor=True, clear_screen=clear_screen,
    ).show()


class TerminalUI:
    def __init__(self):
        self.console = Console()

    def info(self, message):
        self.console.print(message, style="bold cyan", markup=False)

    def error(self, message):
        # Error messages can contain paths, Git output, or selectors with brackets.
        self.console.print("Error:", message, style="bold red", markup=False)

    def warning(self, message):
        self.console.print("Warning:", message, style="bold yellow", markup=False)

    def prompt(self, message, default=None, type=str):
        return typer.prompt(message, default=default, type=type)

    def select(self, entries, title, clear_screen=False):
        return get_selection(entries, title, clear_screen)
