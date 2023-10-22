import datetime
from faker import Faker
from ..models.connection import ConnectionOutput
from ..models.switch import Switch
from ..models.customer import Customer
import random

fake = Faker()


def createMockCustomer() -> Customer:
    return Customer(
        id=fake.ean(length=8),
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
    )


def createMockConnection() -> ConnectionOutput:
    fake.seed(random.randint(0, 1000))
    return ConnectionOutput(
        ppp="NR12",
        id=fake.uuid4(),
        port=fake.port_number(),
        toggleDate=random.choice([None, fake.date_time_between(
            start_date=datetime.now(), end_date="+1y")]),
        address=fake.address(),
        type=random.choice(["copper", "fiber"]),
        isUp=bool(random.getrandbits(1)),
        toggled=bool(random.getrandbits(1)),
        adapter="snmp",
        switch=createMockSwitch(),
        customer=createMockCustomer(),
    )
