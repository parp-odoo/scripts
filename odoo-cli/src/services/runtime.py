"""Compose the shared dependencies supplied to command handlers."""

import importlib.util
import subprocess
from dataclasses import dataclass, field
from typing import Callable

from configuration.store import ConfigStore
from terminal.ui import TerminalUI

from .repositories import RepositoryManager


def debugger_available():
    return importlib.util.find_spec("debugpy") is not None


@dataclass
class Runtime:
    store: ConfigStore = field(default_factory=ConfigStore)
    repositories: RepositoryManager = field(default_factory=RepositoryManager)
    ui: TerminalUI = field(default_factory=TerminalUI)
    runner: Callable = subprocess.run
    debugger_check: Callable = debugger_available
