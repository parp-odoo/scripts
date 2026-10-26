"""Build process arguments without running commands or reading configuration."""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from configuration.defaults import (
    DEFAULT_DEBUG_PORT,
    DEFAULT_TEST_DEBUG_PORT,
    DEMO_TAG_INCOMPATIBLE_VERSIONS,
)
from configuration.settings import ConfigError


@dataclass(frozen=True)
class LaunchOptions:
    drop_database: bool = False
    debug: bool = True
    debug_port: Optional[int] = None
    test_tags: Optional[str] = None

    @property
    def debugger_port(self):
        if self.debug_port is not None:
            return self.debug_port
        return DEFAULT_TEST_DEBUG_PORT if self.test_tags is not None else DEFAULT_DEBUG_PORT

    def http_port(self, settings):
        if self.test_tags is not None:
            if settings.test_port == settings.port:
                raise ConfigError(
                    "The test HTTP port must differ from the server HTTP port. "
                    "Choose a different test port in Initialize configuration."
                )
            if self.debug and settings.test_port == DEFAULT_DEBUG_PORT:
                raise ConfigError("The test HTTP port must differ from the server debugger port (5678).")
            port = settings.test_port
        else:
            port = settings.port
        if self.debug and port == self.debugger_port:
            raise ConfigError("The HTTP port must differ from the debugger port.")
        if self.debug and self.test_tags is not None and self.debugger_port == settings.port:
            raise ConfigError("The test debugger port must differ from the server HTTP port.")
        return port


def build_server_command(settings, options, python_executable=None):
    """Return argv for regular, database initialization, or installed-module tests."""
    community = Path(settings.community_path)
    addons = [str(community / "addons"), str(community / "odoo" / "addons")]
    if settings.enterprise_path:
        addons.append(settings.enterprise_path)
    if settings.extra_demo_path:
        addons.append(str(Path(settings.extra_demo_path) / "addons") + "/")
    command = [
        str(community / "odoo-bin"),
        f"--addons-path={','.join(addons)}",
        "-d", settings.database_name,
        "-p", str(options.http_port(settings)),
    ]
    if options.test_tags is not None:
        command.extend([
            "-c", settings.config_path,
            "--test-enable", f"--test-tags={options.test_tags}", "--stop-after-init",
            "--max-cron-threads=0",
        ])
    else:
        command.extend(["-i" if options.drop_database else "-u", settings.update_module])
        if settings.version not in DEMO_TAG_INCOMPATIBLE_VERSIONS:
            command.append("--with-demo")
        if settings.version == "master":
            command.append("--with-test-data")
    command.extend(["--http-interface=0.0.0.0", "--limit-time-real=6969696969"])
    if options.test_tags is None:
        command.append("--dev=all")
    if options.debug or options.test_tags is not None:
        command.append("--workers=0")
    if options.debug:
        command = [
            python_executable or sys.executable, "-m", "debugpy",
            "--listen", f"127.0.0.1:{options.debugger_port}", *command,
        ]
    return command
