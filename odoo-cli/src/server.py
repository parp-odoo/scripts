import importlib.util
import os
import shlex
import subprocess
import sys

import typer
from config import init_config
from rich import print as richPrint
from utils.const import DB_NAME, DEMO_TAG_INCOMPATIBLE_VERSIONS, EXTRA_DEMO_MODULE_PATH
from utils.json_config import read_config, write_config
from utils.version import (
    change_extra_demo_version,
    chnage_cache_version,
    get_and_set_current_version,
)


def drop_and_run_server():
    return run(True)


def run_server(debug=True, debug_port=5678):
    return run(debug=debug, debug_port=debug_port)


def run_tests(test_tags=None):
    """Run selected tests, remembering the selector for the next invocation."""
    configuration = read_config()
    if not configuration:
        richPrint("[bold red]Initialize the CLI configuration before running tests.[/bold red]")
        return False

    if test_tags is None:
        test_tags = configuration.get("test_tags") or typer.prompt("Test tags")
    test_tags = test_tags.strip()
    if not test_tags:
        richPrint("[bold red]Test tags cannot be empty.[/bold red]")
        return False

    configuration["test_tags"] = test_tags
    if not write_config(configuration):
        richPrint("[bold red]Could not save test tags to the CLI configuration.[/bold red]")
        return False

    richPrint("[bold cyan]Running tests with tags:[/bold cyan]", test_tags)
    return run(test_tags=test_tags, debug=True)


def run(dropdb=False, debug=True, debug_port=5678, test_tags=None):
    """Run the Odoo server"""

    if debug and importlib.util.find_spec("debugpy") is None:
        richPrint("[bold red]Debug mode requires debugpy in the active Python environment.[/bold red]")
        richPrint("Install it with: " + shlex.join([sys.executable, "-m", "pip", "install", "debugpy"]))
        return False

    if not get_and_set_current_version():
        chnage_cache_version()

    # Load configuration
    configuration = read_config()
    if not configuration:
        richPrint("[bold red]Error reading configuration file[/bold red]")
        return False

    community_path = configuration.get("community_path")
    enterprise_path = configuration.get("enterprise_path")
    port = configuration.get("port")
    configuration_file_path = configuration.get("configuration_file_path") or configuration.get("config_path")
    version = configuration.get("version")

    try:
        # Verify enterprise path exists
        enterprise_path_check = os.path.exists(enterprise_path)
        if not enterprise_path_check:
            richPrint("[bold yellow]Enterprise path not provided[/bold yellow]")

        # Verify community path exists
        community_path_check = os.path.exists(community_path)
        if not community_path_check:
            richPrint(f"[bold red]Community path not found ({community_path})[/bold red]")
            return False

        # Verify Odoo configuration file exists
        configuration_file_path_check = os.path.exists(configuration_file_path)
        if not configuration_file_path_check:
            richPrint(f"[bold red]Odoo configuration file not found ({configuration_file_path})[/bold red]")
            return False

        # Verify odoo-bin binary exists
        odoo_bin = os.path.isfile(f"{community_path}/odoo-bin")
        if not odoo_bin:
            richPrint("[bold red]odoo-bin binary not found[/bold red]")
            return False

        # Verify odoo-bin binary is executable
        odoo_bin = os.access(f"{community_path}/odoo-bin", os.X_OK)
        if not odoo_bin:
            richPrint("[bold red]odoo-bin binary is not executable[/bold red]")
            return False
    except:
        richPrint("[bold red]Error verifying paths[/bold red]")
        richPrint(f"[bold yellow]   Community path: {community_path}[/bold yellow]")
        richPrint(f"[bold yellow]   Enterprise path: {enterprise_path}[/bold yellow]")
        richPrint(f"[bold yellow]   Configuration file path: {configuration_file_path}[/bold yellow]")

        update_config_file = typer.prompt("Do you want to update the configuration file? (yes/no)")
        if update_config_file == "yes":
            init_config()

        return False

    args = []
    if test_tags is not None:
        args.extend([
            "-c", configuration_file_path,
            "--test-enable",
            f"--test-tags={test_tags}",
            "--stop-after-init",
        ])
    else:
        args.extend(["-u", "pos_restaurant"])
    db_name = DB_NAME + "-" + version
    if dropdb and test_tags is None:
        os.system(f"dropdb {db_name}")
        richPrint(f"[bold green]✓ Odoo database - {db_name} drop successfully.")
        args = ["-i", "pos_restaurant"]

    if test_tags is None:
        if version not in DEMO_TAG_INCOMPATIBLE_VERSIONS:
            args.append("--with-demo")

        if version in ("master"):
            args.append("--with-test-data")

    change_extra_demo_version(version)

    addons_path = ",".join([
        f"{community_path}/addons",
        f"{community_path}/odoo/addons",
        enterprise_path,
        # WEB_SHELL_PATH,
        EXTRA_DEMO_MODULE_PATH,
        # "/home/odoo/odoo/workspace/my",
    ])
    if test_tags is not None:
        richPrint(f"[bold green]✓ Running Odoo tests on port {port} using installed modules")
    else:
        richPrint(f"[bold green]✓ Launching Odoo server on port {port} With Demo Data")
    command = [
        f"{community_path}/odoo-bin",
        f"--addons-path={addons_path}",
        "-d", db_name,
        "-p", str(port),
        *args,
        "--http-interface=0.0.0.0",
        "--limit-time-real=6969696969",
    ]
    if test_tags is None:
        command.append("--dev=xml,qweb" if debug else "--dev=all")
    if debug or test_tags is not None:
        command.append("--workers=0")
    if debug:
        # Keep breakpoints in one process and avoid the Python autoreloader.
        command = [
            sys.executable, "-m", "debugpy",
            "--listen", f"127.0.0.1:{debug_port}",
            *command,
        ]
        richPrint(f"[bold cyan]Starting debugpy on 127.0.0.1:{debug_port} without waiting for VS Code[/bold cyan]")

    result = subprocess.run(command, check=False)
    if debug or test_tags is not None:
        return result.returncode
    return None
