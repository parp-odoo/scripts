"""Atomic JSON configuration persistence."""

import json
import os
import tempfile
from dataclasses import asdict
from pathlib import Path

from .defaults import CONFIG_PATH
from .settings import ConfigError, Settings


class ConfigStore:
    def __init__(self, path=CONFIG_PATH):
        self.path = Path(path)

    def _read(self):
        try:
            data = json.loads(self.path.read_text(encoding="utf-8") or "{}")
        except (OSError, ValueError) as error:
            raise ConfigError(f"Cannot read configuration at {self.path}: {error}") from error
        if not isinstance(data, dict):
            raise ConfigError("The CLI configuration must contain a JSON object.")
        return data

    def load(self):
        return Settings.from_mapping(self._read())

    def load_or_default(self):
        """Allow first-time setup without concealing a damaged existing file."""
        return self.load() if self.path.exists() else Settings()

    def save(self, settings):
        # Retain settings added by users or other versions of the CLI.
        data = self._read() if self.path.exists() else {}
        data.update(asdict(settings))
        if "configuration_file_path" in data:
            data["configuration_file_path"] = settings.config_path
        Settings.from_mapping(data)
        temporary_path = None
        try:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                mode="w", encoding="utf-8", dir=self.path.parent, delete=False,
            ) as temporary:
                temporary_path = Path(temporary.name)
                json.dump(data, temporary, indent=2)
                temporary.write("\n")
            os.replace(temporary_path, self.path)
        except OSError as error:
            raise ConfigError(f"Cannot save configuration at {self.path}: {error}") from error
        finally:
            if temporary_path is not None:
                temporary_path.unlink(missing_ok=True)
