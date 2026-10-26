"""Interactive menu and argument parsing; dispatch to the command handlers."""

import argparse
from functools import partial

import typer
from commands.configure import initialize_configuration
from commands.run_tests import run_tests
from commands.server import run_server
from commands.versions import change_version
from services.odoo import LaunchOptions
from services.runtime import Runtime


def main():
    runtime = Runtime()
    actions = [
        ("Run Odoo server", partial(run_server, runtime)),
        ("Drop database & run server", partial(run_server, runtime, LaunchOptions(drop_database=True))),
        ("Initialize configuration", partial(initialize_configuration, runtime)),
        ("Change version", partial(change_version, runtime)),
    ]
    try:
        selection = runtime.ui.select(
            [f"{index + 1}. {label}" for index, (label, _) in enumerate(actions)],
            "Welcome to Odoo CLI — what do you want to do?", clear_screen=True,
        )
        result = 0 if selection is None else actions[selection][1]()
    except (KeyboardInterrupt, typer.Abort):
        result = 130
    raise typer.Exit(result)


def tests_main(argv=None):
    parser = argparse.ArgumentParser(description="Run Odoo tests and remember the last test tags.")
    parser.add_argument("test_tags", nargs="?", help="Odoo test selector; defaults to the saved test tags")
    args = parser.parse_args(argv)
    try:
        return run_tests(Runtime(), args.test_tags)
    except (KeyboardInterrupt, typer.Abort):
        return 130
