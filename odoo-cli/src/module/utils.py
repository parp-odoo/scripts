import re
from git import Repo, GitCommandError


def parse_branch(branch_name: str):
    # Remove optional 'odoo-dev:' prefix
    clean_branch = branch_name.split(":", 1)[-1]

    # Pattern: master, saas-X.Y, or X.Y at start
    match = re.match(r"^(master|saas-\d+\.\d+|\d+\.\d+)", clean_branch)
    if not match:
        raise ValueError(f"Could not extract version from branch: {branch_name}")

    version = match.group(1)
    return version, clean_branch


def chnage_repo_version(repo: Repo, input_branch):
    target_version, branch = parse_branch(input_branch)

    for remote in repo.remotes:
        remote.fetch()
        print(f"[bold green]  ✓ Remote fetched {remote.name}")

    # Check if branch exists on remote
    branch_exists_remote = False
    remote_branch_name = f"origin/{branch}"

    try:
        remote_refs = [ref.name for ref in repo.refs]
        if remote_branch_name in remote_refs:
            branch_exists_remote = True
    except GitCommandError as e:
        print(f"[bold red] ✗ Error checking branches: {e}")

    # Checkout based on existence
    if branch_exists_remote:
        repo.git.checkout(branch)
        print(f"[bold green]  ✓ Checked out to branch {branch}")
    else:
        repo.git.checkout(target_version)
        print(f"[bold yellow]  ⚠ Branch '{branch}' not found. Checked out to version {target_version}")

    # If branch and target_version are same, pull
    if target_version == branch:
        repo.git.pull('--rebase')
        print("[bold green]  ✓ Repository updated with rebase")
