from pydantic import BaseModel, model_validator
from typing import Optional


class CustomerDataType(BaseModel):
    """CustomerDataType is the type of the data from the customer"""
    id: int
    firstname: str
    lastname: str
    type: Optional[str]


class ConnectionDataType(BaseModel):
    """ConnectionDataType is the type of the data from the connection"""
    id: Optional[int]
    toggled: bool
    autoUpdate: bool
    address: str
    flat: str
    customerId: Optional[int]


class SourceDataType(BaseModel):
    """SourceDataType is the type of the data from the source"""
    customer: CustomerDataType
    connection: ConnectionDataType


class TargetDataType(BaseModel):
    """TargetDataType is the type of the data from the target"""
    customer: CustomerDataType
    connection: ConnectionDataType


class UpdatesDataType(BaseModel):
    """UpdatesDataType is the type of the data to be updated"""
    customers: list[CustomerDataType]
    connections: list[ConnectionDataType]


class RemovesDataType(BaseModel):
    """RemovesDataType is the type of the data to be removed"""
    customers: list[int]


class SplitDataType(BaseModel):
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
