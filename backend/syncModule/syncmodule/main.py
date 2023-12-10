import os
import yaml
from .implementations.sqlSource import SQLSyncModule, SyncModuleConfig


def getConfig(path: str) -> SyncModuleConfig:
    assert os.path.exists(path), "config file does not exist"
    assert os.path.isfile(path), "only files are supported"
    assert path.endswith(".yaml"), "only yaml files are supported"
    with open(path, 'r') as f:
        return SyncModuleConfig(**yaml.load(f))


def main():
    assert "CONFIG_PATH" in os.environ, "CONFIG_PATH is not defined"
    config = getConfig(os.environ["CONFIG_PATH"])
    assert config.sync is not None, "config.sync is not defined"
    assert config.sync.type is not None, "config.sync.type is not defined"
    assert config.sync.type in [
        "sql"], f"type {config.sync.type} is not supported, accepted types [sql]"
    if (config.sync.type == "sql"):
        syncModule = SQLSyncModule(config)
        print(syncModule.getSourceData())
    else:
        print("to be implemented")
    pass
