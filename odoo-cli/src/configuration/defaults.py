"""Defaults shared by the CLI commands and services."""

from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parents[2] / ".cache" / "odoo-cli.json"
ALL_VERSIONS = (
    "master", "19.0", "18.0", "saas-19.2", "saas-19.1", "saas-18.4",
    "saas-18.3", "saas-18.2",
)
DEMO_TAG_INCOMPATIBLE_VERSIONS = frozenset({
    "16.0", "17.0", "18.0", "saas-18.1", "saas-18.2",
})
DEFAULT_EXTRA_DEMO_PATH = "/home/odoo/odoo/x/"
DEFAULT_DEBUG_PORT = 5678
DEFAULT_TEST_PORT = 8021
DEFAULT_TEST_DEBUG_PORT = 5679
