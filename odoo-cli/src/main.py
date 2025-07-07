import typer
import sys

from module import odoo_utils
from rich import print

app = typer.Typer()


def main():
    """
    This function is the main entry point for the CLI

    Odoo CLI: Allow you to start a server, initialize the configuration,
    change the version, pull the latest changes, and drop the database.
    """
    odoo_cli()


def odoo_cli():
    odoo_utils.choices()


if __name__ == "__main__":
    typer.run(main)
