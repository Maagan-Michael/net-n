from abc import abstractmethod
from typing import Dict, List
from pydantic import BaseModel
import requests

from sqlalchemy import create_engine

SourceDataType = Dict[
    "customer": Dict[
        "id": int,
        "firstname": str,
        "lastname": str,
        "type": str,
        "address": str
    ],
    "connection": Dict[
        "toggled": bool,
    ]
]

TargetDataType = Dict[
    "customer": Dict[
        "id": int,
        "firstname": str,
        "lastname": str,
        "type": str,
        "address": str
    ],
    "connection": Dict[
        "id": int,
        "toggled": bool,
        "autoUpdate": bool
    ]
]


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


class ISyncModule:
    """ISyncModule is the interface for the SyncModule"""

    def __init__(self, destination: DBConfig, apiUrl: str):
        self.destination = destination
        self.apiUrl = apiUrl

    @abstractmethod
    def getSourceData(self) -> List[SourceDataType]:
        """
        gets the data from the source
        this method should be implemented by the child class
        this method should return a list of SourceDataType
        """
        pass

    def getTargetData(self) -> List[TargetDataType]:
        """gets the data from the target database"""
        url = self.destination.generateUrl()
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
                    "id": x[6],
                    "toggled": x[5],
                    "autoUpdate": x[7]
                }
            }
        with engine.connect() as conn:
            result = conn.execute(
                f"""
                SELECT {columns} FROM {self.destination.table}
                FROM customers
                LEFT JOIN connections ON = connections.customer_id
                """
            )
        engine.dispose()
        return result

    def splitData(self) -> Dict[
        "updates": Dict[
            "customers": List[Dict],
            "connections": List[Dict]
        ],
        "removes": Dict[
            "customers": List[Dict],
            "connections": List[Dict]
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

    async def apiUpdates(self, data: Dict):
        if (len(data["updates"]["customers"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/customers/upsert", json=data)
        if (len(data["updates"]["connections"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/connections/upsert", json=data)

    async def apiRemoves(self, data: Dict):
        if (len(data["removes"]["customers"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/customers/delete", json=data)
        if (len(data["removes"]["connections"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/connections/delete", json=data)

    async def sync(self):
        """syncs the data from the source database to the target database"""
        data = self.splitData()
