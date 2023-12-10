import os
import yaml


def get_config() -> dict:
    """get the configuration"""
    assert "CONFIG_PATH" in os.environ, "CONFIG_PATH is not defined"
    with open(os.environ["CONFIG_PATH"], "r") as f:
        return yaml.safe_load(f)


AppConfig = get_config()
