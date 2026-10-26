"""Switch Odoo repositories and optionally recreate and launch the database."""

from dataclasses import replace

from configuration.defaults import ALL_VERSIONS
from configuration.settings import ConfigError
from services.odoo import LaunchOptions
from services.repositories import RepositoryError
from services.versions import switch_extra_demo

from .server import run_server


def change_version(runtime):
    try:
        settings = runtime.store.load()
        selected = runtime.ui.select(ALL_VERSIONS, "Target Version")
        if selected is None:
            return 0
        version = ALL_VERSIONS[selected]
        should_run = runtime.ui.select(["Yes", "No"], f"Run the Odoo server on {version}?")
        if should_run is None:
            return 0
        if not settings.community_path:
            raise ConfigError("Configure the Community repository before changing versions.")
        runtime.repositories.switch_all(
            [settings.community_path, settings.enterprise_path], version,
        )
        settings = replace(settings, version=version)
        switch_extra_demo(runtime, settings)
        runtime.store.save(settings)
        runtime.ui.info(f"Version changed to {version}")
        if should_run == 0:
            return run_server(runtime, LaunchOptions(drop_database=True))
        return 0
    except (ConfigError, RepositoryError) as error:
        runtime.ui.error(str(error))
        return 1
