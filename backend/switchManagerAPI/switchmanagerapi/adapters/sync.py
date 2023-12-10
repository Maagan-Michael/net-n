from abc import abstractmethod
import datetime

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import update, select, bindparam
from sqlalchemy.orm import contains_eager
from ..db.schemas import DBConnection, DBSwitch
from ..config import AppConfig
from ..db.context import get_context_db_session

from .adapter import Adapter
from .IMC import IMCAdapter

from ..logger import get_logger

logger = get_logger("SyncAdapter")


class ModelsSyncModule:
    def __init__(self, adapter: Adapter, session):
        self.adapter = adapter
        self.session = session

    @abstractmethod
    async def insert(self):
        pass

    @abstractmethod
    async def update(self):
        pass

    @abstractmethod
    async def check(self):
        pass

    async def sync(self):
        self.adapter.getSwitches()
        await self.update()
        await self.check()
        await self.insert()


class ConnectionSyncModule(ModelsSyncModule):
    def __init__(self, adapter: Adapter, session):
        super().__init__(adapter, session)

    async def insert(self):
        switches = await (self.session.scalars(
            select(DBSwitch)
            .where(DBSwitch.notReachable == False)
        )).all()
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
                    await self.session.execute(
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

    async def update(self):
        pass

    async def check(self):
        pass

    async def toggleConnections(self):
        cons = (await self.session.scalars(
            select(DBConnection.id, DBConnection.toggled,
                   DBConnection.port, DBSwitch.ip)
            .join(DBConnection.switch)
            .where(DBConnection.toggleDate <= datetime.datetime.now())
            .options(contains_eager(DBConnection.switch))
        )).all()
        for con in cons:
            if (con["toggled"]):
                logger.info(
                    f"disabling connection {con['id']} on switch {con['ip']} port {con['port']}")
                self.adapter.togglePort(con["ip"], con["port"], False)
                await self.session.execute(
                    update(DBConnection)
                    .where(DBConnection.id == con["id"])
                    .values({
                        "toggled": False,
                        "toggleDate": None
                    })
                )
            else:
                logger.info(
                    f"enabling connection {con['id']} on switch {con['ip']} port {con['port']}")
                await self.session.execute(
                    update(DBConnection)
                    .where(DBConnection.id == con["id"])
                    .values({
                        "toggled": True,
                        "toggleDate": None
                    })
                )

    async def sync(self):
        await super().sync()
        await self.toggleConnections()


class SwitchesSyncModule(ModelsSyncModule):
    def __init__(self, adapter: Adapter, session):
        super().__init__(adapter, session)

    async def insert(self):
        inserts = [{
            "name": e["label"],
            "ip": e["ip"],
            "notReachable": False
        } for e in self.adapter.switches]
        names = [e["name"] for e in inserts]
        exists = await self.session.execute(
            select(DBSwitch.name).where(DBSwitch.name.in_(names))
        )
        exists = [e[0] for e in exists]
        inserts = [e for e in inserts if e["name"] not in exists]
        if (len(inserts) > 0):
            logger.info(
                f"adding new switches detected on the network ({len(inserts)})")
            await self.session.execute(
                insert(DBSwitch)
                .values({
                    "name": bindparam("name"),
                    "ip": bindparam("ip"),
                    "notReachable": False
                }),
                inserts
            )
            logger.info("adding new switches detected on the network done")

    async def update(self):
        updates = [{
            "name": e["label"],
            "ip": e["ip"],
            "notReachable": False
        } for e in self.adapter.switches]
        for e in updates:
            logger.info(f"syncing switch {e['name']}")
            await self.session.execute(
                update(DBSwitch)
                .where(DBSwitch.name == e["name"])
                .values({
                    "ip": e["ip"],
                    "notReachable": False
                })
            )
            logger.info(f"syncing switch {e['name']} done")

    async def check(self):
        names = [e['label'] for e in self.adapter.switches]
        await self.session.execute(
            update(DBSwitch)
            .where(DBSwitch.name.not_in(names))
            .values({
                "notReachable": True
            })
        )
        unreachables = (await self.session.scalars(
            select(DBSwitch)
            .where(DBSwitch.notReachable == True)
        )).all()
        for e in unreachables:
            logger.info(f"switch {e['name']} is unreachable")


class AdapterSyncModule:
    def __init__(self) -> None:
        self.adapter = None
        if (AppConfig.get("imc")):
            self.adapter = IMCAdapter(
                https=AppConfig["imc"]["https"],
                host=AppConfig["imc"]["host"],
                user=AppConfig["imc"]["user"],
                password=AppConfig["imc"]["password"],
                port=AppConfig["imc"]["port"]
            )
        else:
            logger.error(
                "unknown network adapter, please provide a configuration file for [imc]")
            self.adapter = Adapter()

    async def _sync_all(self, session):
        switches = SwitchesSyncModule(self.adapter, session)
        await switches.sync()
        connections = ConnectionSyncModule(self.adapter, session)
        await connections.sync()

    async def sync(self):
        """get database session"""
        async with get_context_db_session() as session:
            await self._sync_all(session)


AppAdapter = AdapterSyncModule()
