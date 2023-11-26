from typing import Any, List
from pydantic import BaseModel
import logging

from sqlalchemy import create_engine


class DBConfig(BaseModel):
    """DBConfig is the configuration for the database"""
    host: str
    port: int
    user: str
    password: str
    database: str
    table: str

    def generateUrl(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}/{self.database}"


class SyncModuleConfig(BaseModel):
    """
        SyncModuleConfig is the configuration for the SyncModule
        source: DBConfig is the source database configuration
        destination: DBConfig is the destination database configuration
        col_name_customer_id is the source column name for customer id
        col_name_customer_firstname is the source column name for customer firstname
        col_name_customer_lastname is the source column name for customer lastname
        col_name_customer_type is the source column name for customer type
        col_name_customer_address is the source column name for customer address
        col_name_connection_toggled is the source column name for connection toggled
    """
    source: DBConfig
    destination: DBConfig

    col_name_customer_id: str
    col_name_customer_firstname: str
    col_name_customer_lastname: str
    col_name_customer_type: str
    col_name_customer_address: str
    col_name_connection_toggled: str


class SyncModule:
    """SyncModule is the module that syncs the data from the source database to the target database"""

    def __init__(self, config: SyncModuleConfig):
        self.config = config
        self.logger = logging.getLogger('syncmodule')
        self.logger.info('SyncModule init')

    def getSourceData(self) -> List[dict]:
        """gets the data from the source database"""
        url = self.config.source.generateUrl()
        engine = create_engine(url)
        columns = ",".join([
            self.config.source.col_name_customer_id,
            self.config.source.col_name_customer_firstname,
            self.config.source.col_name_customer_lastname,
            self.config.source.col_name_customer_type,
            self.config.source.col_name_customer_address,
            self.config.source.col_name_connection_toggled
        ])
        for x in columns:
            x = {
                "customer": {
                    "id": x[0],
                    "firstname": x[1],
                    "lastname": x[2],
                    "type": x[3],
                    "address": x[4],
                },
                "connection": {
                    "toggled": x[5]
                }
            }
        with engine.connect() as conn:
            result = conn.execute(
                f"SELECT {columns} FROM {self.config.source.table}")
        engine.dispose()
        return result

    def getTargetData(self) -> List[dict]:
        """gets the data from the target database"""
        url = self.config.destination.generateUrl()
        engine = create_engine(url)
        columns = ",".join([
            "customers.id",
            "customers.firstname",
            "customers.lastname",
            "customers.type",
            "customers.address",
            "connections.toggled",
            "connections.id",
            "connections.autoUpdate"
        ])
        for x in columns:
            x = {
                "customer": {
                    "id": x[0],
                    "firstname": x[1],
                    "lastname": x[2],
                    "type": x[3],
                    "address": x[4],
                },
                "connection": {
                    "toggled": x[5],
                    "id": x[6],
                    "autoUpdate": x[7]
                }
            }
        with engine.connect() as conn:
            result = conn.execute(
                f"""
                SELECT {columns} FROM {self.config.destination.table}
                FROM customers
                LEFT JOIN connections ON = connections.customer_id
                """
            )
        engine.dispose()
        return result

    def splitData(self) -> dict[
        "updates": dict[
            "customers": List[dict],
            "connections": List[dict]
        ],
        "removes": dict[
            "customers": List[dict],
            "connections": List[dict]
        ]
    ]:
        """splits the data into updates and removes"""
        sourceData = self.getSourceData()
        targetData = self.getTargetData()
        res = {
            "updates": {
                "customers": [],
                "connections": []
            },
            "removes": {
                "customers": [],
                "connections": []
            }
        }
        # getting customers and connections to update
        for x in sourceData:
            for (y, idx) in enumerate(targetData):
                if x["customer"]["id"] == y["customer"]["id"]:
                    if (x["customer"] != y["customer"]):
                        res["updates"]["customers"].append(x)
                    if (x["connection"]["toggled"] != y["connection"]["toggled"] and y["connection"]["autoUpdate"]):
                        res["updates"]["connection"].append({
                            "id": y["connection"]["id"],
                            "toggled": x["connection"]["toggled"]
                        })
                    # remove from list
                    del targetData[idx]
                    break

        # all the targetData left is to be removed only if autoUpdate is true
        for (x, idx) in enumerate(targetData):
            if x["connection"]["autoUpdate"]:
                res["removes"]["customers"].append(x["customer"])
                res["removes"]["connections"].append(x["connection"])

    def sync(self):
        """syncs the data from the source database to the target database"""
        data = self.splitData()
