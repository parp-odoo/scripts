import os

ALL_VERSIONS = ["master", "19.0", "18.0", "saas-19.2", "saas-19.1", "saas-18.4", "saas-18.3", "saas-18.2"]

DB_NAME = "testdb"
EXTRA_DEMO_MODULE_PATH = "/home/odoo/odoo/x/addons/"
DEMO_TAG_INCOMPATIBLE_VERSIONS = ["16.0", "17.0", "18.0", "saas-18.1", "saas-18.2"]
WEB_SHELL_PATH = "/home/odoo/odoo/shell"

# Need to make attention to the file location instead of user one.
CACHE_PATH = f"{os.path.dirname(__file__)}/../../.cache"
CACHE_FILE_NAME = "odoo-cli.json"
