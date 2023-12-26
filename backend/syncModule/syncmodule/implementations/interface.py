from abc import abstractmethod
from typing import List, Optional

from .types import DBConfig, SourceDataType, ConnectionDataType, CustomerDataType, SplitDataType, UpdatesDataType, RemovesDataType
from sqlalchemy import create_engine, text
import requests


class ISyncModule:
    """
        ISyncModule is the interface for the SyncModule
        this class should be inherited by the child class
        this class should not be instantiated
        only getSourceData should be implemented by the child class
    """

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
            gets full list of connections from the switchManager database
        """
        results = []
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
            queryResult = conn.execute(
                text(f"SELECT {columns} FROM public.connections")
            ).all()
            for x in queryResult:
                results.append(ConnectionDataType.model_construct(
                    id=x[0],
                    address=x[1],
                    flat=x[2],
                    toggled=x[3],
                    autoUpdate=x[4],
                    customerId=x[5],
                ))
            engine.dispose()
        return results

    def getCurrentCustomers(self) -> List[CustomerDataType]:
        """
            gets full list of customers from the switchManager database
        """
        results = []
        url = self.destination.generateUrl()
        engine = create_engine(url)
        columns = ", ".join([
            "id",
            "firstname",
            "lastname",
            "type",
        ])
        with engine.connect() as conn:
            queryResult = conn.execute(
                text(f"SELECT {columns} FROM public.customers")
            ).all()
            for x in queryResult:
                results.append(CustomerDataType.model_construct(
                    id=x[0],
                    firstname=x[1],
                    lastname=x[2],
                    type=x[3],
                ))
            engine.dispose()
        return results

    def splitData(self) -> SplitDataType:
        """
            get the data from the source and the target
            splits the data into updateables and removeables objects

        """
        sourceData = self.getSourceData()
        connections = self.getCurrentConnections()
        customers = self.getCurrentCustomers()
        res = SplitDataType.model_construct(
            updates=UpdatesDataType.model_construct(
                customers=[],
                connections=[]
            ),
            removes=RemovesDataType.model_construct(
                customers=[]
            )
        )
        # getting customers and connections to update
        for x in sourceData:
            for (idx, y) in enumerate(connections):
                # upsert customer
                res.updates.customers.append(x.customer)

                # match connection based on address and flat
                if (
                    (x.connection.address == y.address) and
                    (x.connection.flat == y.flat)
                ):
                    # check if has budget, close the port otherwise
                    # also set the customerId in case customer changed
                    if (
                        y.autoUpdate and
                        (
                            x.connection.toggled != y.toggled or
                            x.connection.customerId != y.customerId
                        )
                    ):
                        res.updates.connections.append(
                            ConnectionDataType.model_construct(
                                id=y.id,
                                toggled=x.connection.toggled,
                                customerId=x.customer.id
                            ))
                    # remove from list
                    del connections[idx]
                    break

        # getting customers to remove
        customersToDelete = [
            x.id for x in customers if (
                x.id not in [y.customer.id
                             for y in sourceData]
            )]
        res.removes.customers = customersToDelete
        return res

    async def apiUpdates(self, data: SplitDataType):
        """updates the data using the syncManager API"""
        if (len(data.updates.customers) > 0):
            await requests.post(f"{self.apiUrl}/v1/customers/upsert", json=data)
        if (len(data.updates.connections) > 0):
            await requests.post(f"{self.apiUrl}/v1/connections/upsert", json=data)

    async def apiRemoves(self, data: SplitDataType):
        """
            removes the data using the syncManager API
            only customers are removed
            connections are not removed because they are statically generated based on hardware information, thus they must not be removed
        """
        if (len(data.removes.customers) > 0):
            await requests.post(f"{self.apiUrl}/v1/customers/delete", json=data)

    async def sync(self):
        """syncs the data from the source database to the API"""
        data = self.splitData()
        await self.apiUpdates(data)
        await self.apiRemoves(data)
