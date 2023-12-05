from abc import abstractmethod
import os
import yaml

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update, select, bindparam
from sqlalchemy import exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from ..db.context import SQLALCHEMY_DATABASE_URL
from ..db.schemas import DBConnection, DBSwitch

from .adapter import Adapter
from .IMC import IMCAdapter

from ..logger import get_logger

logger = get_logger("SyncAdapter")


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
        self.update()
        self.check()
        self.insert()


class ConnectionSyncModule(ModelsSyncModule):
    def __init__(self, adapter: Adapter, session):
        super().__init__(adapter, session)

    def insert(self):
        switches = self.session.scalars(
            select(DBSwitch)
            .where(DBSwitch.notReachable == False)
        ).all()
        for switch in switches:
            _dict = switch.__dict__
            logger.info(
                f"syncronizing switch {_dict['name']}({_dict['ip']}) interfaces")
            try:
                interfaces = self.adapter.getSwitchInterfaces(_dict["ip"])
                for interface in interfaces:
                    values = {
                        "name": interface["ifAlias"],
                        "switchId": _dict["id"],
                        "port": int(interface["ifIndex"]),
                        "strPort": interface["ifIndex"],
                        "toggled": interface["operationStatus"] == "1",
                        "isUp": interface["operationStatus"] == "1",
                        "adapter": "imc"
                    }
                    self.session.execute(
                        insert(DBConnection)
                        .values(values)
                        .on_conflict_do_update(
                            constraint="switch_port_unique", set_=values)
                    )
            except Exception as e:
                logger.error(
                    f"error syncing switch {_dict['name']}({_dict['ip']}) interfaces")
                logger.error(e)
            logger.info(
                f"syncronizing switch {_dict['name']}({_dict['ip']}) interfaces done")

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
        if (len(inserts) > 0):
            logger.info(
                f"adding new switches detected on the network ({len(inserts)})")
            self.session.execute(
                insert(DBSwitch)
                .values({
                    "name": bindparam("name"),
                    "ip": bindparam("ip"),
                    "notReachable": False
                }),
                inserts
            )
            logger.info("adding new switches detected on the network done")

    def update(self):
        updates = [{
            "name": e["label"],
            "ip": e["ip"],
            "notReachable": False
        } for e in self.adapter.switches]
        for e in updates:
            logger.info(f"syncing switch {e['name']}")
            self.session.execute(
                update(DBSwitch)
                .where(DBSwitch.name == e["name"])
                .values({
                    "ip": e["ip"],
                    "notReachable": False
                })
            )
            logger.info(f"syncing switch {e['name']} done")

    def check(self):
        names = [e['label'] for e in self.adapter.switches]
        self.session.execute(
            update(DBSwitch)
            .where(DBSwitch.name.not_in(names))
            .values({
                "notReachable": True
            })
        )
        unreachables = self.session.scalars(
            select(DBSwitch)
            .where(DBSwitch.notReachable == True)
        ).all()
        for e in unreachables:
            logger.info(f"switch {e['name']} is unreachable")


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

    def _sync_all(self, session):
        switches = SwitchesSyncModule(self.adapter, session)
        switches.sync()
        connections = ConnectionSyncModule(self.adapter, session)
        connections.sync()

    def sync(self):
        """get database session"""
        engine = create_engine(
            SQLALCHEMY_DATABASE_URL.replace("asyncpg", "psycopg2"))
        factory = sessionmaker(engine)
        with factory() as session:
            try:
                self._sync_all(session)
                session.commit()
            except exc.SQLAlchemyError as e:
                session.rollback()
                raise e
            finally:
                session.close()
