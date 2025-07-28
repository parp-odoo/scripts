import typer
from rich import print
from module.cache_utils import read_json_configuration, write_json_configuration


CACHE_FILE_NAME = "odoo-cli.json"
app = typer.Typer()


def toggle_extra_flag():
    configuration = read_json_configuration(CACHE_FILE_NAME) or {}
    with_extra = configuration.get("with_extra")

    with_extra = "n" if with_extra == "y" else "y"

    result = write_json_configuration(CACHE_FILE_NAME, {
        **configuration,
        "with_extra": with_extra,

    })

    if not result:
        print("[bold red]Error toggling extra flag")
        return False

    print("[bold green]Extra flag is set to ", with_extra)


def main():
    toggle_extra_flag()


if __name__ == "__main__":
    typer.run(main)
