from abc import abstractmethod
import os
from net-n.backend.switchManagerAPI.switchmanagerapi.db.schemas.connections import DBConnection
import yaml
from .adapter import Adapter
from sqlalchemy import update, delete, insert, select, bindparam
from ..db.schemas.switches import DBSwitch
from .IMC import IMCAdapter

from ..db.context import SQLALCHEMY_DATABASE_URL
from sqlalchemy import exc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


class ModelsSyncModule:
    def __init__(self, adapter: Adapter, session):
        self.adapter = adapter
        self.session = session

    @abstractmethod
    def insert(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def check(self):
        pass

    def sync(self):
        self.adapter.getSwitches()
        self.insert()
        self.update()
        self.check()

class ConnectionSyncModule(ModelsSyncModule):
    def __init__(self, adapter: Adapter, session):
        super().__init__(adapter, session)

    def insert(self):
        switches = self.session.execute(
            select(DBSwitch)
            .where(DBSwitch.notReachable == False)
        )
        for switch in switches:
            interfaces = self.adapter.getSwitchInterfaces(switch["ip"])
            for interface in interfaces:
                self.session.execute(
                    insert(DBConnection)
                    .values({
                        "switchId": switch["id"],
                        "port": int(interface["ifIndex"]),
                        "isUp": interface["showStatus"] == "1"
                    })
                    .on_conflict_do_update(
                        constraint="switch_port_unique", set_={
                        "isUp": interface["showStatus"] == "1"
                    })
                )

    def update(self):
        pass

    def check(self):
        pass

class SwitchesSyncModule(ModelsSyncModule):
    def __init__(self, adapter: Adapter, session):
        super().__init__(adapter, session)

    def insert(self):
        inserts = [{
            "name": e["label"],
            "ip": e["ip"],
            "notReachable": False
        } for e in self.adapter.switches]
        names = [e["name"] for e in inserts]
        exists = self.session.execute(
            select(DBSwitch.name).where(DBSwitch.name.in_(names))
        )
        exists = [e[0] for e in exists]
        inserts = [e for e in inserts if e["name"] not in exists]
        self.session.execute(
            insert(DBSwitch)
            .values({
                "name": bindparam("name"),
                "ip": bindparam("ip"),
                "notReachable": False
            }),
            inserts
        )

    def update(self):
        updates = [{
            "name": e["label"],
            "ip": e["ip"],
            "notReachable": False
        } for e in self.adapter.switches]
        self.session.execute(
            update(DBSwitch)
            .where(DBSwitch.name == bindparam("label"))
            .values({
                "ip": bindparam("ip"),
                "notReachable": False
            }),
            updates
        )

    def check(self):
        names = [e['label'] for e in self.adapter.switches]
        self.session.execute(
            update(DBSwitch)
            .where(DBSwitch.name.not_in(names))
            .values({
                "notReachable": True
            })
        )


class AdapterSyncModule:
    def get_config(self) -> dict:
        """get the configuration"""
        with open(os.environ["SM_CONF"], "r") as f:
            return yaml.safe_load(f)

    def __init__(self) -> None:
        config = self.get_config()
        self.adapter = None
        if (config["imc"]):
            self.adapter = IMCAdapter(
                https=config["imc"]["https"],
                host=config["imc"]["host"],
                user=config["imc"]["user"],
                password=config["imc"]["password"],
                port=config["imc"]["port"]
            )
        else:
            raise Exception(
                "unknown network adapter, please provide a configuration file for [imc]")

