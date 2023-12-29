import os
import yaml


def get_config() -> dict:
    """
        get the configuration
        TODO: parse and validate the configuration with a PydanticModel
        TODO: change all AppConfig["..."] to AppConfig.[key]
    """
    assert "CONFIG_PATH" in os.environ, "CONFIG_PATH is not defined"
    with open(os.environ["CONFIG_PATH"], "r") as f:
        return yaml.safe_load(f)


AppConfig = get_config()
