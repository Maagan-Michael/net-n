from .adapter import Adapter
from sqlalchemy import update, delete, insert, select, bindparam
from ..db.schemas.switches import DBSwitch
from ..db.context import get_context_db_session


class DeviceSyncModule:
    def __init__(self, adapter: Adapter):
        self.adapter = adapter

    async def sync(self):
        """sync the devices from the adapter to the database"""
        with get_context_db_session() as session:
            self.adapter.getDevices()
            names = self.adapter.getDevicesNames()

            updates = [
                {
                    "name": e["label"],
                    "ip": e["ip"],
                    "notReachable": False
                } for e in self.adapter.devices
            ]
            # override IP, notReachable
            await session.execute(
                update(DBSwitch)
                .where(DBSwitch.name == bindparam("label"))
                .values({
                    "ip": bindparam("ip"),
                    "notReachable": bindparam("notReachable")
                }),
                updates
            )

            # switches to add
            reachables = await session.scalars(
                select(DBSwitch).where(DBSwitch.name.in_(names))
            )
            reachablesNames = [e.name for e in reachables]
            # todo : check for differences and update
            toAdd = [e for e in self.adapter.devices.filter(
                lambda x: x['name'] not in reachablesNames
            )]
            # todo add new switches

            # switches to flag (ie: maintenance, hardware | network issue, removed)
            notReachable = await session.scalars(
                select(DBSwitch).where(DBSwitch.name.not_in(names))
            )
            notReachableIds = [e.id for e in notReachable]
            await session.execute(
                update(DBSwitch)
                .where(DBSwitch.id.in_(notReachableIds))
                .values(notReachable=True)
            )

            # switches to add
