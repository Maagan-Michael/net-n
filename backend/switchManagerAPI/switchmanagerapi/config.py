import os
import yaml


def get_config() -> dict:
    """get the configuration"""
    with open(os.environ["SM_CONF"], "r") as f:
        return yaml.safe_load(f)


AppConfig = get_config()
