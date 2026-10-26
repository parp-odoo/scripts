"""Shared Git operations and branch naming rules, without prompts or config I/O."""

import re
from concurrent.futures import ThreadPoolExecutor

from git import Repo
from git.exc import GitError


class RepositoryError(RuntimeError):
    """A repository could not be inspected or switched."""


def version_from_branch(branch):
    clean_branch = branch.split(":", 1)[-1]
    match = re.match(r"^(master|saas-\d+\.\d+|\d+\.\d+)", clean_branch)
    return match.group(1) if match else clean_branch


class RepositoryManager:
    def __init__(self, repo_factory=Repo):
        self.repo_factory = repo_factory

    def current_version(self, path):
        try:
            repo = self.repo_factory(path)
            branch = repo.git.rev_parse("--abbrev-ref", "HEAD")
            if branch == "HEAD":
                raise RepositoryError("The Community repository has a detached HEAD.")
            return version_from_branch(branch)
        except (GitError, OSError) as error:
            raise RepositoryError(f"Cannot determine the version in {path}: {error}") from error

    def switch(self, path, version):
        try:
            repo = self.repo_factory(path)
            for remote in repo.remotes:
                remote.fetch()
            repo.git.checkout(version)
            repo.git.pull("--rebase")
        except (GitError, OSError) as error:
            raise RepositoryError(f"Cannot update repository at {path}: {error}") from error

    def switch_all(self, paths, version):
        paths = list(dict.fromkeys(path for path in paths if path))
        if not paths:
            return
        with ThreadPoolExecutor(max_workers=len(paths)) as executor:
            # Consume every result so failures reach the caller before saving a version.
            list(executor.map(lambda path: self.switch(path, version), paths))

    def switch_extra_demo(self, path, version):
        if not path:
            return
        try:
            repo = self.repo_factory(path)
            if repo.git.rev_parse("--abbrev-ref", "HEAD") != version:
                repo.git.checkout(version)
        except (GitError, OSError) as error:
            raise RepositoryError(f"Cannot switch extra demo at {path}: {error}") from error
