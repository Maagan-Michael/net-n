from abc import abstractmethod
from typing import TypedDict, List, Optional
from pydantic import BaseModel, model_validator
import requests

from sqlalchemy import create_engine, text


class CustomerDataType(TypedDict):
    """CustomerDataType is the type of the data from the customer"""
    id: int
    firstname: str
    lastname: str
    type: Optional[str]


class ConnectionDataType(TypedDict):
    """ConnectionDataType is the type of the data from the connection"""
    id: Optional[int]
    toggled: bool
    autoUpdate: bool
    address: str
    flat: str
    customerId: Optional[int]


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

    def getCurrentConnections(self) -> List[ConnectionDataType]:
        """
            gets full list of connections from the target database
            customers are joined to the connections
        """
        url = self.destination.generateUrl()
        engine = create_engine(url)
        columns = ", ".join([
            "id",
            "address",
            "flat",
            "toggled",
            "'autoUpdate'",
            "'customerId'"
        ])
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT {columns} FROM public.connections")
            ).all()
            for x in result:
                x = ConnectionDataType(
                    id=x[0],
                    address=x[1],
                    flat=x[2],
                    toggled=x[3],
                    autoUpdate=x[4],
                    customerId=x[5],
                )
            engine.dispose()
        return result

    def getCurrentCustomers(self) -> List[CustomerDataType]:
        """
            gets full list of customers from the target database
        """
        url = self.destination.generateUrl()
        engine = create_engine(url)
        columns = ", ".join([
            "id",
            "firstname",
            "lastname",
            "type",
        ])
        with engine.connect() as conn:
            result = conn.execute(
                text(f"SELECT {columns} FROM public.customers")
            ).all()
            for x in result:
                x = CustomerDataType(
                    id=x[0],
                    firstname=x[1],
                    lastname=x[2],
                    type=x[3],
                )
            engine.dispose()
        return result

    def splitData(self) -> SplitDataType:
        """
            get the data from the source and the target
            splits the data into updates and removes objects ot be used with the API
        """
        sourceData = self.getSourceData()
        connections = self.getCurrentConnections()
        customers = self.getCurrentCustomers()
        res = SplitDataType(
            updates=UpdatesDataType(
                customers=[],
                connections=[]
            ),
            removes=RemovesDataType(
                customers=[]
            )
        )
        # getting customers and connections to update
        for x in sourceData:
            for (y, idx) in enumerate(connections):
                # upsert customer
                res.updates.customers.append(x.customer)
                res["updates"]["customers"].append(x["customer"])

                # match connection based on address and flat
                if (
                    (x["connection"]["address"] == y["connection"]["address"]) and
                    (x["connection"]["flat"] == y["connection"]["flat"])
                ):
                    # check if has budget, close the port otherwise
                    # also set the customerId in case customer changed
                    if (
                        y["connection"]["autoUpdate"] and
                        (
                            x["connection"]["toggled"] != y["connection"]["toggled"] or
                            x["connection"]["customerId"] != y["customer"]["id"]
                        )
                    ):
                        res["updates"]["connection"].append({
                            "id": y["connection"]["id"],
                            "toggled": x["connection"]["toggled"],
                            "customerId": x["customer"]["id"]
                        })
                    # remove from list
                    del connections[idx]
                    break

        # getting customers to remove
        customersToDelete = [
            x["customer"]["id"] for x in customers if (
                x["customer"]["id"] not in [y["customer"]["id"]
                                            for y in sourceData]
            )]
        res["removes"]["customers"] = customersToDelete
        return res

    async def apiUpdates(self, data: SplitDataType):
        """updates the data to the API"""
        if (len(data["updates"]["customers"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/customers/upsert", json=data)
        if (len(data["updates"]["connections"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/connections/upsert", json=data)

    async def apiRemoves(self, data: SplitDataType):
        """
            removes the data from the API
            only customers are removed
            connections are not removed because they are statically generated based on hardware information, thus they must not be removed
        """
        if (len(data["removes"]["customers"]) > 0):
            await requests.post(f"{self.apiUrl}/v1/customers/delete", json=data)

    async def sync(self):
        """syncs the data from the source database to the API"""
        data = self.splitData()
        await self.apiUpdates(data)
        await self.apiRemoves(data)
