"""Run Odoo's selected tests and remember the selector."""

from dataclasses import replace

from configuration.settings import ConfigError
from services.odoo import LaunchOptions

from .server import run_server


def run_tests(runtime, test_tags=None):
    try:
        settings = runtime.store.load()
        if test_tags is None:
            test_tags = settings.test_tags or runtime.ui.prompt("Test tags")
        test_tags = test_tags.strip()
        if not test_tags:
            raise ConfigError("Test tags cannot be empty.")
        runtime.store.save(replace(settings, test_tags=test_tags))
    except ConfigError as error:
        runtime.ui.error(str(error))
        return 1
    runtime.ui.info(f"Running tests with tags: {test_tags}")
    return run_server(runtime, LaunchOptions(test_tags=test_tags))
