import typer
from rich import print
from module.cache_utils import read_json_configuration, write_json_configuration


CACHE_FILE_NAME = "odoo-cli.json"
app = typer.Typer()


def toggle_demo_flag():
    configuration = read_json_configuration(CACHE_FILE_NAME) or {}
    with_extra_demo = configuration.get("with_extra_demo")

    with_extra_demo = "n" if with_extra_demo == "y" else "y"

    result = write_json_configuration(CACHE_FILE_NAME, {
        **configuration,
        "with_extra_demo": with_extra_demo,

    })

    if not result:
        print("[bold red]Error toggling extra demo flag")
        return False

    print("[bold green]✓ Extra Demo flag is set to ", with_extra_demo)


def main():
    toggle_demo_flag()


if __name__ == "__main__":
    typer.run(main)
