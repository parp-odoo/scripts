from rich import print as richPrint
from typer import prompt

from utils.json_config import read_config, write_config


def init_config():
    richPrint("[bold yellow]We will initialize the configuration file")
    richPrint("[bold yellow]Please provide the following information:")

    configuration = read_config()
    enterprise_path = prompt("Odoo enterprise path?", configuration.get("enterprise_path"), type=str)
    community_path = prompt("Odoo community path?", configuration.get("community_path"), type=str)
    port = prompt("Port to run Odoo server?", configuration.get("port", 8069), type=int)
    config_path = prompt("Where is the odoo.conf file?", configuration.get("config_path"), type=str)

    result = write_config({
        "enterprise_path": enterprise_path,
        "community_path": community_path,
        "port": port,
        "config_path": config_path,
        "version": "",
        "with_extra": "n",
    })

    if not result:
        richPrint("[bold red]Error creating configuration file")
        return False

    richPrint("[bold green]Configuration file created successfully")
