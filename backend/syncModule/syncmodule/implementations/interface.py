from abc import abstractmethod
from typing import TypedDict, List, Optional
from pydantic import BaseModel, model_validator
import requests

from sqlalchemy import create_engine


class CustomerDataType(TypedDict):
    """CustomerDataType is the type of the data from the customer"""
    id: int
    firstname: str
    lastname: str
    type: str
    address: str


class ConnectionDataType(TypedDict):
    """ConnectionDataType is the type of the data from the connection"""
    id: Optional[int]
    toggled: bool
    autoUpdate: bool


class SourceDataType(TypedDict):
    """SourceDataType is the type of the data from the source"""
    customer: CustomerDataType
    connection: ConnectionDataType


class TargetDataType(TypedDict):
    """TargetDataType is the type of the data from the target"""
    customer: CustomerDataType
    connection: ConnectionDataType


class UpdatesDataType(TypedDict):
    """UpdatesDataType is the type of the data to be updated"""
    customers: List[CustomerDataType]
    connections: List[ConnectionDataType]


class RemovesDataType(TypedDict):
    """RemovesDataType is the type of the data to be removed"""
    customers: List[int]
    connections: List[int]


class SplitDataType(TypedDict):
    """SplitDataType is the type of the data to be split"""
    updates: UpdatesDataType
    removes: RemovesDataType


class DBConfig(BaseModel):
    """DBConfig is the configuration for the database"""
    driver: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None
    user: Optional[str] = None
    password: Optional[str] = None
    database: Optional[str] = None
    table: Optional[str] = None
    url: Optional[str] = None

    @model_validator(mode="after")
    def validateUrl(self):
        if (self.url):
            return self
        if (not self.driver):
            raise ValueError("driver is required")
        if (not self.host):
            raise ValueError("host is required")
        if (not self.port):
            raise ValueError("port is required")
        if (not self.user):
            raise ValueError("user is required")
        if (not self.password):
            raise ValueError("password is required")
        if (not self.database):
            raise ValueError("database is required")
        if (not self.table):
            raise ValueError("table is required")
        return self

    def generateUrl(self) -> str:
        if (self.url):
            return self.url
        return f"{self.driver}://{self.user}:{self.password}@{self.host}/{self.database}"


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
                LEFT JOIN connections ON = connections.customer_id
                """
            )
        engine.dispose()
        return result

    def splitData(self) -> SplitDataType:
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
                res["removes"]["customers"].append(x["customer"]["id"])
                res["removes"]["connections"].append(x["connection"]["id"])

    async def apiUpdates(self, data: SplitDataType):
        """updates the data to the API"""
        if (len(data["updates"]["customers"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/customers/upsert", json=data)
        if (len(data["updates"]["connections"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/connections/upsert", json=data)

    async def apiRemoves(self, data: SplitDataType):
        """removes the data from the API"""
        if (len(data["removes"]["customers"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/customers/delete", json=data)
        if (len(data["removes"]["connections"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/connections/delete", json=data)

    async def sync(self):
        """syncs the data from the source database to the API"""
        data = self.splitData()
        await self.apiUpdates(data)
        await self.apiRemoves(data)
