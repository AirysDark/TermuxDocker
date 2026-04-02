import os
import json

CONFIG_PATH = os.path.expanduser("~/.termuxdocker/config.json")

DEFAULT_CONFIG = {
    "images_path": os.path.expanduser("~/.termuxdocker/images"),
    "default_arch": "auto"
}

def load_config():
    if not os.path.exists(CONFIG_PATH):
        save_config(DEFAULT_CONFIG)
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)
