from simple_term_menu import TerminalMenu

DEFAULT_MENU_OPTIONS = {
    "menu_cursor": "> ",
    "menu_cursor_style": ("fg_yellow", "bold"),
    "menu_highlight_style": ("fg_cyan", "bold", "italics"),
    "cycle_cursor": True,
    "clear_screen": True,
}


def get_selection(menu_items, title="", should_enumerate=False, **kwargs):
    # menu_entries=[f"{i + 1}. {label}" for i, (label, _) in enumerate(menu_items)],
    # title="Welcome to Odoo CLI — what do you want to do?",
    menu_entries = menu_items
    if should_enumerate:
        menu_entries = [f"{i + 1}. {label}" for i, (label, _) in enumerate(menu_items)]

    menu_options = {
        **DEFAULT_MENU_OPTIONS,
        **kwargs,
    }

    terminal_menu = TerminalMenu(
        menu_entries=menu_entries,
        title=title,
        **menu_options
    )
    selected_index = terminal_menu.show()
    return selected_index
