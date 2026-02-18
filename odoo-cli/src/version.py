from concurrent.futures import ThreadPoolExecutor, as_completed

from git import Repo
from rich import print as richPrint

from server import run

from utils.json_config import read_config
from utils.terminal_menu import get_selection
from utils.version import set_version, change_extra_demo_version
from utils.const import ALL_VERSIONS
from itertools import starmap


def run_threading_repo_version_change(repo_tasks):
    results = []
    with ThreadPoolExecutor(max_workers=len(repo_tasks)) as executor:
        # futures = list(starmap(executor.submit, repo_tasks))
        futures = [
            executor.submit(chnage_repo_version, repo, version, color)
            for repo, version, color in repo_tasks
        ]
        for future in as_completed(futures):
            result = future.result()
            results.append(result)
    return results


def change_version():
    richPrint("[bold yellow]We will change the Odoo version and drop the database")
    richPrint("[bold yellow]Please provide the following information:")

    configuration = read_config()
    target_version = _select_version()
    if not target_version:
        return
    richPrint("[bold Green]Selected version : ", target_version)

    should_run = get_selection(
        ["Yes", "No"],
        f"Run the Odoo server on {target_version}?",
        clear_screen=False,
    )
    if should_run is None:
        return

    enterprise_repo = Repo(configuration.get("enterprise_path"))
    community_repo = Repo(configuration.get("community_path"))

    try:
        # richPrint("[bold deep_pink4]Enterprise repository:")
        # chnage_repo_version(enterprise_repo, target_version, "deep_pink4")
        # richPrint("[bold dark_orange3]Community repository:")
        # chnage_repo_version(community_repo, target_version, "dark_orange3")

        run_threading_repo_version_change([
            (community_repo, target_version, "dark_orange3"),
            (enterprise_repo, target_version, "deep_pink4"),
        ])

        change_extra_demo_version(target_version)
        set_version(target_version)

        if should_run == 0:
            run(True)
    except Exception as err:
        richPrint("[bold red]Error updating versions", err)
        return False


def chnage_repo_version(repo, target_version, color="purple3"):
    for remote in repo.remotes:
        remote.fetch()
        richPrint(f"[bold {color}]  ✓ Remote fetched", remote.name)

    repo.git.checkout(target_version)
    richPrint(f"[bold {color}]  ✓ Version changed to {target_version}")

    repo.git.pull('--rebase')
    richPrint(f"[bold {color}]  ✓ Repository updated with rebase")


def _select_version():
    selected_menu = get_selection(
        ALL_VERSIONS,
        "Target Version",
        clear_screen=False,
    )
    if selected_menu is None:
        return False
    return ALL_VERSIONS[selected_menu]
