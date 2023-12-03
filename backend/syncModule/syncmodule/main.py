import sys
import json
import yaml
from .implementations.sqlSource import SQLSyncModule, SyncModuleConfig


def getConfig(path: str) -> SyncModuleConfig:
    with open(path, 'r') as f:
        if (path.endswith(".yaml")):
            return SyncModuleConfig(**yaml.load(f))
        elif (path.endswith(".json")):
            return SyncModuleConfig(**json.load(f))
        else:
            raise Exception("unknown file type")


def __main__():
    config = getConfig(sys.argv[1])
    print("to be implemented")
    pass
