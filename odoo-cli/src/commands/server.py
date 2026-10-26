"""Validate settings and launch Odoo, optionally recreating its database."""

import os
import shlex
import sys
from pathlib import Path

from configuration.settings import ConfigError
from services.odoo import LaunchOptions, build_server_command
from services.versions import resolve_version, switch_extra_demo


def _validate_paths(runtime, settings):
    if not settings.community_path or not Path(settings.community_path).is_dir():
        raise ConfigError(f"Community path not found ({settings.community_path})")
    if not settings.config_path or not Path(settings.config_path).is_file():
        raise ConfigError(f"Odoo configuration file not found ({settings.config_path})")
    binary = Path(settings.community_path) / "odoo-bin"
    if not binary.is_file():
        raise ConfigError("odoo-bin binary not found")
    if not os.access(binary, os.X_OK):
        raise ConfigError("odoo-bin binary is not executable")
    if not settings.enterprise_path or not Path(settings.enterprise_path).is_dir():
        runtime.ui.warning("Enterprise path not provided or not found")


def run_server(runtime, options=None):
    options = options if options is not None else LaunchOptions()
    try:
        settings = runtime.store.load()
        _validate_paths(runtime, settings)
        if options.debug and not runtime.debugger_check():
            runtime.ui.error("Debug mode requires debugpy in the active Python environment.")
            runtime.ui.info("Install it with: " + shlex.join([
                sys.executable, "-m", "pip", "install", "debugpy",
            ]))
            return 1
        settings = resolve_version(runtime, settings)
        command = build_server_command(settings, options)
        if options.drop_database and options.test_tags is None:
            result = runtime.runner(["dropdb", settings.database_name], check=False)
            if result.returncode:
                runtime.ui.error(f"Could not drop database {settings.database_name}.")
                return result.returncode
            runtime.ui.info(f"Odoo database {settings.database_name} dropped successfully.")
        switch_extra_demo(runtime, settings)
        if options.test_tags is not None:
            runtime.ui.info(f"Running Odoo tests on port {settings.port} using installed modules")
        else:
            runtime.ui.info(f"Launching Odoo server on port {settings.port}")
        if options.debug:
            runtime.ui.info(
                f"Starting debugpy on 127.0.0.1:{options.debug_port} without waiting for VS Code"
            )
        return runtime.runner(command, check=False).returncode
    except (ConfigError, OSError) as error:
        runtime.ui.error(str(error))
        return 1
