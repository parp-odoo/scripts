import os
from rich import print as richPrint
import typer

from config import init_config

from utils.version import get_and_set_current_version, chnage_cache_version, change_extra_demo_version
from utils.json_config import read_config
from utils.const import DB_NAME, EXTRA_DEMO_MODULE_PATH, DEMO_TAG_INCOMPATIBLE_VERSIONS, WEB_SHELL_PATH


def drop_and_run_server():
    run(True)


def run_server():
    run()


def run(dropdb=False):
    """Run the Odoo server"""

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
    configuration_file_path = configuration.get("configuration_file_path")
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

    args = "-u pos_restaurant"
    db_name = DB_NAME + "-" + version
    if dropdb:
        os.system(f"dropdb {db_name}")
        richPrint(f"[bold green]✓ Odoo database - {db_name} drop successfully.")
        args = "-i pos_restaurant"

    if version not in DEMO_TAG_INCOMPATIBLE_VERSIONS:
        args += " --with-demo"

    change_extra_demo_version(version)

    addons_path = ",".join([
        f"{community_path}/addons",
        f"{community_path}/odoo/addons",
        enterprise_path,
        WEB_SHELL_PATH,
        EXTRA_DEMO_MODULE_PATH,
    ])
    richPrint(f"[bold green]✓ Launching Odoo server on port {port} With Demo Data")
    command = f"{community_path}/odoo-bin --addons-path={addons_path} -d {db_name} -p {port} {args} --dev=all"

    os.system(command)
