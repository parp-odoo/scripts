import typer
import os

from rich import print
from git import Repo
from .cache_utils import read_json_configuration, write_json_configuration, set_version, get_version


CACHE_PATH = f"{os.path.dirname(__file__)}/../../.cache"
CACHE_FILE_NAME = "odoo-cli.json"

DB_NAME = "testdb"

VERSION_WITHOUT_DEMO_TAG = ["17.0", "18.0", "saas-18.1", "saas-18.2"]

EXTRA_DEMO_MODULE_PATH = "/home/odoo/odoo/x/"


def choices():
    print("[bold yellow]Welcome to Odoo CLI, what do you want to do?")
    print("[bold]1. Run Odoo server")
    print("[bold]2. Initialize configuration")
    print("[bold]3. Change version")
    option = typer.prompt("Select an option")

    if option == "1":
        chnage_cache_version()
        run()
    elif option == "2":
        init()
    elif option == "3":
        version()


def chnage_cache_version():
    configuration = read_json_configuration(CACHE_FILE_NAME)
    version = configuration.get("version")
    target_version = typer.prompt("Which version to run odoo server?", version)
    set_version(CACHE_FILE_NAME, target_version)


def init():
    print("[bold yellow]We will initialize the configuration file")
    print("[bold yellow]Please provide the following information:")

    configuration = read_json_configuration(CACHE_FILE_NAME) or {}
    enterprise_path = typer.prompt("Odoo enterprise path?", configuration.get("enterprise_path") or "", type=str)
    community_path = typer.prompt("Odoo community path?", configuration.get("community_path") or "", type=str)
    port = typer.prompt("Port to run Odoo server?", configuration.get("port") or 8069, type=int)
    configuration_file_path = typer.prompt("Where is the odoo.conf file?", configuration.get("configuration_file_path") or "", type=str)

    result = write_json_configuration(CACHE_FILE_NAME, {
        "enterprise_path": enterprise_path,
        "community_path": community_path,
        "port": port,
        "configuration_file_path": configuration_file_path,
        "version": ""
    })

    if not result:
        print("[bold red]Error creating configuration file")
        return False

    print("[bold green]Configuration file created successfully")


def version():
    print("[bold yellow]We will change the Odoo version and drop the database")
    print("[bold yellow]Please provide the following information:")

    configuration = read_json_configuration(CACHE_FILE_NAME)
    target_version = typer.prompt("Target Odoo version?", configuration.get("target_version") or "", type=str)

    enterprise_repo = Repo(configuration.get("enterprise_path"))
    community_repo = Repo(configuration.get("community_path"))

    try:
        print("[bold green]Enterprise repository:")
        enterprise_repo.git.checkout(target_version)
        print(f"[bold green]  ✓ Version changed to {target_version}")
        enterprise_repo.remotes[0].pull()
        print("[bold green]  ✓ Repository updated successfully")

        print("[bold green]Community repository:")
        community_repo.git.checkout(target_version)
        print(f"[bold green]  ✓ Version changed to {target_version}")
        community_repo.remotes[0].pull()
        print("[bold green]  ✓ Repository updated successfully")

        print("[bold green]Odoo version updated successfully")
        set_version(CACHE_FILE_NAME, target_version)

        should_run = typer.prompt(f"Run the Odoo server on {target_version}? (y/n)", "y", type=str)
        if should_run == "y":
            run()
    except:
        print("[bold red]Error updating versions")
        return False


def run():
    """Run the Odoo server"""

    # Load configuration
    configuration = read_json_configuration(CACHE_FILE_NAME)
    if not configuration:
        print("[bold red]Error reading configuration file[/bold red]")
        return False

    community_path = configuration.get("community_path")
    enterprise_path = configuration.get("enterprise_path")
    extra_path = configuration.get("extra_path")
    port = configuration.get("port")
    configuration_file_path = configuration.get("configuration_file_path")
    version = configuration.get("version")

    try:
        # Verify enterprise path exists (optional)
        enterprise_path_check = os.path.exists(enterprise_path)
        if not enterprise_path_check:
            print(f"[bold yellow]Enterprise path not provided[/bold yellow]")

        # Verify community path exists
        community_path_check = os.path.exists(community_path)
        if not community_path_check:
            print(f"[bold red]Community path not found ({community_path})[/bold red]")
            return False

        # Verify Odoo configuration file exists
        configuration_file_path_check = os.path.exists(configuration_file_path)
        if not configuration_file_path_check:
            print(f"[bold red]Odoo configuration file not found ({configuration_file_path})[/bold red]")
            return False

        # Verify odoo-bin binary exists
        odoo_bin = os.path.isfile(f"{community_path}/odoo-bin")
        if not odoo_bin:
            print(f"[bold red]odoo-bin binary not found[/bold red]")
            return False

        # Verify odoo-bin binary is executable
        odoo_bin = os.access(f"{community_path}/odoo-bin", os.X_OK)
        if not odoo_bin:
            print(f"[bold red]odoo-bin binary is not executable[/bold red]")
            return False
    except:
        print("[bold red]Error verifying paths[/bold red]")
        print(f"[bold yellow]   Community path: {community_path}[/bold yellow]")
        print(f"[bold yellow]   Enterprise path: {enterprise_path}[/bold yellow]")
        print(f"[bold yellow]   Configuration file path: {configuration_file_path}[/bold yellow]")

        update_config_file = typer.prompt("Do you want to update the configuration file? (yes/no)")
        if update_config_file == "yes":
            init()

        return False

    # Launch Odoo server
    # Verify if cache db exist:
    args = "-u pos_restaurant"

    # DropDB old DB
    drop_db = typer.prompt(f"Want to drop the Odoo database - {DB_NAME}? (y/n)", "y")
    if drop_db == "y":
        os.system(f"dropdb {DB_NAME}")
        print(f"[bold green]✓ Odoo database - {DB_NAME} drop successfully.")
        args = "-i pos_restaurant"

    extra_addons = []

    with_demo_data = typer.prompt("Demo data? (y/n)", "y")
    if with_demo_data == "y" and version not in VERSION_WITHOUT_DEMO_TAG:
        args += " --with-demo"
    elif with_demo_data != "y" and version in VERSION_WITHOUT_DEMO_TAG:
        args += " --without-demo"

    if with_demo_data == "y":
        print("[bold green]✓ db will Initialize with Extra Demo Data.")
        extra_addons += [EXTRA_DEMO_MODULE_PATH]

    # with_exta = typer.prompt("Extra modules? (y/n)", "n")
    with_exta = "n"
    if with_exta != "n":
        print("[bold green]✓ db will Initialize with Extra Modules.")
        extra_addons += [extra_path]

    extra_addons_path = ""
    if len(extra_addons):
        for ex_path in extra_addons:
            extra_addons_path += "," + ex_path

    print(f"[bold green]✓ Launching Odoo server on port {port} {'With' if with_demo_data == 'y' else 'without'} Demo Data")
    os.system(f"{community_path}/odoo-bin --addons-path={community_path}/addons,{community_path}/odoo/addons,{enterprise_path}{extra_addons_path} -d {DB_NAME} -p {port} {args} --dev=all")
