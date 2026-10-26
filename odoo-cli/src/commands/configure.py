"""Initialize or update the CLI configuration."""

from dataclasses import replace

from configuration.settings import ConfigError


def initialize_configuration(runtime):
    try:
        settings = runtime.store.load_or_default()
        runtime.ui.info("We will initialize the configuration file")
        settings = replace(
            settings,
            enterprise_path=runtime.ui.prompt("Odoo enterprise path?", settings.enterprise_path or None),
            community_path=runtime.ui.prompt("Odoo community path?", settings.community_path or None),
            port=runtime.ui.prompt("Port to run Odoo server?", settings.port, type=int),
            test_port=runtime.ui.prompt("Port to run Odoo tests?", settings.test_port, type=int),
            config_path=runtime.ui.prompt("Where is the odoo.conf file?", settings.config_path or None),
        )
        runtime.store.save(settings)
        runtime.ui.info("Configuration file created successfully")
        return 0
    except ConfigError as error:
        runtime.ui.error(str(error))
        return 1
