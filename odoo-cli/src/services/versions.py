"""Version resolution and optional demo synchronization shared by commands."""

from dataclasses import replace

from configuration.settings import ConfigError

from .repositories import RepositoryError


def resolve_version(runtime, settings):
    try:
        version = runtime.repositories.current_version(settings.community_path)
    except RepositoryError as error:
        runtime.ui.warning(str(error))
        version = runtime.ui.prompt("Which version to run odoo server?", settings.version or None)
    version = version.strip()
    if not version:
        raise ConfigError("An Odoo version is required.")
    if version != settings.version:
        settings = replace(settings, version=version)
        runtime.store.save(settings)
    return settings


def switch_extra_demo(runtime, settings):
    try:
        runtime.repositories.switch_extra_demo(settings.extra_demo_path, settings.version)
    except RepositoryError as error:
        runtime.ui.warning(str(error))
