import typer
import os
from rich import print
from module.cache_utils import read_json_configuration, write_json_configuration


CACHE_FILE_NAME = "odoo-cli.json"
app = typer.Typer()


def re_run_previous_error():
    configuration = read_json_configuration(CACHE_FILE_NAME) or {}
    command = configuration.get("command")
    port = configuration.get("port")

    print(f"[bold green]✓ Launching Odoo server on port {port}")
    os.system(command)


def main():
    re_run_previous_error()


if __name__ == "__main__":
    typer.run(main)
