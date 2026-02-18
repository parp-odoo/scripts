import json
import os

from utils.const import CACHE_PATH, CACHE_FILE_NAME


def read_config():
    try:
        config = open(f"{CACHE_PATH}/{CACHE_FILE_NAME}", "r")

        return json.loads(config.read() or "{}")
    except Exception as e:
        print(f"[bold red]Error while reading configuration: {e}")
        return False


def write_config(data):
    try:
        if not os.path.exists(CACHE_PATH):
            os.makedirs(CACHE_PATH)

        config = open(f"{CACHE_PATH}/{CACHE_FILE_NAME}", "w")
        config.write(json.dumps(data))
        config.close()

        return True
    except:
        return False


def validate_new_config_data(data):
    return True
