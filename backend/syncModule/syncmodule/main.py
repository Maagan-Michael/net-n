import os
import yaml
from .implementations.sqlSource import SQLSyncModule, SQLSyncModuleConfig


def getConfig(path: str) -> SQLSyncModuleConfig:
    """
        getConfig gets the config from the given path
        path is the path to the config file
        return the parsed config
    """
    assert os.path.exists(path), "config file does not exist"
    assert os.path.isfile(path), "only files are supported"
    assert path.endswith(".yaml"), "only yaml files are supported"
    with open(path, 'r') as f:
        config = yaml.safe_load(f)
        assert config["sync"] is not None, "config.sync is not defined"
        assert config["sync"]["type"] is not None, "config.sync.type is not defined"
        if (config["sync"]["type"] == "sql"):
            return SQLSyncModuleConfig.model_validate(config["sync"])
        else:
            raise NotImplementedError(
                f"type {config['sync']['type']} is not supported, accepted types [sql]")


def main():
    """
        main is the entry point of the sync module
        it gets the config from the CONFIG_PATH environment variable
        it creates the sync module based on the config
        it syncs the data
    """
    assert "CONFIG_PATH" in os.environ, "CONFIG_PATH is not defined"
    config = getConfig(os.environ["CONFIG_PATH"])
    if type(config) is SQLSyncModuleConfig:
        syncModule = SQLSyncModule(config)
    else:
        raise NotImplementedError("the requested sync module is not supported")

    # testing puposes
    # print(syncModule.getCurrentConnections())
    # print(syncModule.getCurrentCustomers())
    # print(syncModule.getSourceData())
    # print(syncModule.splitData())

    syncModule.sync()
