"""Build process arguments without running commands or reading configuration."""

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from configuration.defaults import DEFAULT_DEBUG_PORT, DEMO_TAG_INCOMPATIBLE_VERSIONS


@dataclass(frozen=True)
class LaunchOptions:
    drop_database: bool = False
    debug: bool = True
    debug_port: int = DEFAULT_DEBUG_PORT
    test_tags: Optional[str] = None


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
        "-p", str(settings.port),
    ]
    if options.test_tags is not None:
        command.extend([
            "-c", settings.config_path,
            "--test-enable", f"--test-tags={options.test_tags}", "--stop-after-init",
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
            "--listen", f"127.0.0.1:{options.debug_port}", *command,
        ]
    return command
