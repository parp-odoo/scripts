"""Typed CLI settings and configuration validation."""

from dataclasses import dataclass, fields

from .defaults import DEFAULT_EXTRA_DEMO_PATH, DEFAULT_TEST_PORT


class ConfigError(ValueError):
    """Configuration is missing, malformed, or cannot be persisted."""


@dataclass(frozen=True)
class Settings:
    community_path: str = ""
    enterprise_path: str = ""
    config_path: str = ""
    port: int = 8069
    test_port: int = DEFAULT_TEST_PORT
    version: str = ""
    test_tags: str = ""
    extra_demo_path: str = DEFAULT_EXTRA_DEMO_PATH
    database_prefix: str = "testdb"
    update_module: str = "pos_restaurant"

    @classmethod
    def from_mapping(cls, data):
        values = {field.name: data[field.name] for field in fields(cls) if field.name in data}
        # Older installations use this key; keep its existing precedence.
        values["config_path"] = data.get("configuration_file_path") or data.get("config_path", "")
        for name, default, label in (
            ("port", 8069, "HTTP"),
            ("test_port", DEFAULT_TEST_PORT, "test HTTP"),
        ):
            try:
                values[name] = int(data.get(name, default))
            except (TypeError, ValueError) as error:
                raise ConfigError(f"The {label} port must be an integer.") from error
            if not 1 <= values[name] <= 65535:
                raise ConfigError(f"The {label} port must be between 1 and 65535.")
        for name, value in values.items():
            if name not in ("port", "test_port") and not isinstance(value, str):
                raise ConfigError(f"Configuration setting '{name}' must be a string.")
        return cls(**values)

    @property
    def database_name(self):
        if not self.version:
            raise ConfigError("Select an Odoo version before starting the server.")
        return f"{self.database_prefix}-{self.version}"
