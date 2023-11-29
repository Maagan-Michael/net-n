from datetime import datetime
from faker import Faker
from ..models.connection import Connection
from ..models.switch import Switch
from ..models.customer import InternalCustomer
from ..db import create_db, drop_db, get_context_db_session
from ..db.schemas import DBConnection, DBSwitch, DBCustomer
from sqlalchemy import insert
import random

fake = Faker()
Faker.seed(random.randint(0, 1000))


def createMockCustomer() -> InternalCustomer:
    id = fake.ean(length=8)
    return InternalCustomer(
        id=id,
        idstr=str(id),
        firstname=fake.first_name(),
        lastname=fake.last_name(),
        type=random.choice(["haverim", fake.company()]),
        address=fake.address(),
    )


def createMockSwitch() -> Switch:
    return Switch(
        id=fake.uuid4(),
        name=f"switch {fake.word()}",
        ip=fake.ipv4(),
        description=fake.text(),
        gpsLat=random.choice([None, fake.latitude()]),
        gpsLong=random.choice([None, fake.longitude()]),
        restricted=bool(random.getrandbits(1)),
        notReachable=bool(random.getrandbits(1))
    )


def createMockConnection(switchId: str, customerId: str) -> Connection:
    port = fake.port_number()
    try:
        return Connection(
            id=fake.uuid4(),
            name=f"{fake.word()[0:3].upper()}{fake.ean(length=8)[0:3]}",
            port=port,
            strPort=f"{port}",
            toggleDate=random.choice([None, fake.date_time_between(
                start_date=datetime.now(), end_date="+1y")]),
            type=random.choice(["copper", "fiber"]),
            isUp=bool(random.getrandbits(1)),
            toggled=bool(random.getrandbits(1)),
            adapter="snmp",
            switchId=switchId,
            customerId=customerId,
            autoUpdate=bool(random.getrandbits(1)),
        )
    except Exception as e:
        print(e)


async def generateMockupDB():
    await drop_db()
    await create_db()
    customers = [createMockCustomer().model_dump() for x in range(0, 50)]
    switches = [createMockSwitch().model_dump() for x in range(0, 10)]
    connections = [
        createMockConnection(switches[random.randint(0, 9)]["id"], customers[x]["id"]).model_dump() for x in range(0, 50)]
    async with get_context_db_session() as session:
        await session.execute(insert(DBCustomer).values(customers))
        await session.execute(insert(DBSwitch).values(switches))
        await session.execute(insert(DBConnection).values(connections))
