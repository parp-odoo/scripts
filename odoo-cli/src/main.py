import typer
from config import init_config
from server import drop_and_run_server, run_server
from utils.terminal_menu import get_selection
from version import change_version


def main():
    menu_items = [
        ("Run Odoo server", run_server),
        ("Drop database & run server", drop_and_run_server),
        ("Initialize configuration", init_config),
        ("Change version", change_version),
    ]
    selected_menu = get_selection(menu_items, "Welcome to Odoo CLI — what do you want to do?", True)
    if selected_menu is None:
        return  # user exited menu
    _, handler = menu_items[selected_menu]
    result = handler()
    if handler in (run_server, drop_and_run_server):
        raise typer.Exit(1 if result is False else result)


if __name__ == "__main__":
    typer.run(main)
