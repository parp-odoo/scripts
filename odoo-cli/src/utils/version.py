import re
import typer
from git import Repo
from rich import print as richPrint

from .json_config import read_config, write_config


def parse_branch(branch_name: str):
    # Remove optional 'odoo-dev:' prefix
    clean_branch = branch_name.split(":", 1)[-1]

    # Pattern: master, saas-X.Y, or X.Y at start
    match = re.match(r"^(master|saas-\d+\.\d+|\d+\.\d+)", clean_branch)
    if not match:
        raise ValueError(f"Could not extract version from branch: {branch_name}")

    version = match.group(1)
    return version, clean_branch


def change_extra_demo_version(target_version):
    configuration = read_config()
    extra_demo_path = configuration.get("extra_demo_path", "/home/odoo/odoo/x/")
    extra_demo_repo = Repo(extra_demo_path)
    try:
        current_version = extra_demo_repo.git.rev_parse("--abbrev-ref", "HEAD")
        if current_version == target_version:
            richPrint(f"[bold cyan]ℹ Extra demo is already on '{target_version}'")
            return True

        extra_demo_repo.git.checkout(target_version)
    except Exception as e:
        richPrint(f"[bold yellow]⚠ Failed to switch extra demo version: {e}")
        return False
    richPrint(f"[bold green]✓ Extra demo version switched to '{target_version}'")
    return True


def get_version_from_branch(branch):
    if branch == "master" or branch.startswith("master-"):
        return "master"
    saas_match = re.match(r"(saas-\d+\.\d+)", branch)
    if saas_match:
        return saas_match.group(1)
    version_match = re.match(r"(\d+\.0)", branch)
    if version_match:
        return version_match.group(1)
    return branch


def get_and_set_current_version():
    configuration = read_config()
    community_path = configuration.get("community_path")
    community_repo = Repo(community_path)
    try:
        current_branch = community_repo.git.rev_parse("--abbrev-ref", "HEAD")
        current_version = get_version_from_branch(current_branch)
        if current_version:
            set_version(current_version)
        return current_version
    except Exception as e:
        print(f"[bold yellow]⚠ Failed to get current version: {e}")
        return False


def chnage_cache_version():
    configuration = read_config()
    version = configuration.get("version")
    target_version = typer.prompt("Which version to run odoo server?", version)
    set_version(target_version)


def set_version(version):
    try:
        config = read_config()
        config["version"] = version
        write_config(config)
        return True
    except:
        return False


def get_version(file):
    try:
        config = read_config(file)
        return config.get("version", False)
    except:
        return False
