from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field
import logging
from .interface import ISyncModule
from .types import ConnectionDataType, CustomerDataType, DBConfig, TargetDataType
from sqlalchemy import create_engine, text
from typing import List, Optional


class ColMapping(BaseModel):
    """
        ColMaps is the mapping of the source column to the target column
    """
    id: str = Field(descrition="customer id column name")
    firstname: Optional[str] = Field(
        default=None, descrition="customer firstname column name")
    lastname: str = Field(descrition="customer lastname column name")
    type: Optional[str] = Field(
        default=None, descrition="customer type column name")
    address: str = Field(descrition="customer address column name")
    flat: str = Field(descrition="customer flat column name")
    toggled: str = Field(
        descrition="weather the connection is toggled or not column name, will be automatically converted to bool")


class SQLSyncModuleConfig(BaseModel):
    """
        SyncModuleConfig is the configuration for the SyncModule
    """
    model_config = ConfigDict(from_attributes=True)

    source: DBConfig = Field(description="source database configuration")
    destination: DBConfig = Field(
        description="SwitchManager database configuration")
    api_url: str = Field(description="SwitchManager api url")

    mapping: ColMapping = Field(description="source column mapping")


class SQLSyncModule(ISyncModule):
    """
        SyncModule is the module that syncs the customers from an external database
        it implements the ISyncModule interface

        current supported drivers :
            - postgresql    : psycopg2
            - oracleDB      : cx_oracle

        to add extra support :
            - check the sqlalchemy documentation about drivers and dialects
            - add the driver to the dependencies through poetry
    """

    def __init__(self, config: SQLSyncModuleConfig):
        super().__init__(config.destination, config.api_url)
        self.config = config
        self.logger = logging.getLogger('syncmodule')
        self.logger.info('SyncModule init')

    def getSourceData(self) -> List[TargetDataType]:
        """gets the data from the source database"""
        url = self.config.source.generateUrl()
        engine = create_engine(url)

        hasType = self.config.mapping.type is not None
        splitName = self.config.mapping.firstname is None

        columns = ", ".join(
            [
                self.config.mapping.id,
                self.config.mapping.flat,
                self.config.mapping.address,
                self.config.mapping.toggled,
            ] +
            ([self.config.mapping.lastname] if splitName
             else [
                self.config.mapping.firstname,
                self.config.mapping.lastname
            ]) +
            ([self.config.mapping.type] if hasType else [])
        )
        results = []
        parsedValues = []
        try:
            with engine.connect() as conn:
                results = conn.execute(
                    text(f"SELECT {columns} FROM {self.config.source.table}")).all()
                engine.dispose()
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Error could retrieve data from source database")
        for x in results:
            try:
                length = len(x)
                fn, lsn = "", ""
                if splitName and x[4] is not None:
                    _v = x[4].split(" ")
                    lsn = _v[0]
                    fn = " ".join(_v[1:len(_v)]) if len(
                        _v) > 1 else ""
                else:
                    fn = x[4] if x[4] is not None else ""
                    lsn = x[5] if x[5] is not None else ""
                value = TargetDataType.model_construct(
                    customer=CustomerDataType.model_construct(
                        id=x[0],
                        firstname=fn,
                        lastname=lsn,
                    ),
                    connection=ConnectionDataType.model_construct(
                        customerId=x[0],
                        flat=x[1],
                        address=x[2],
                        toggled=bool(x[3]),
                        autoUpdate=True,
                    )
                )
                if hasType:
                    value.customer.type = x[length - 1]
                parsedValues.append(value)
            except Exception as e:
                self.logger.error(e)
                self.logger.error(
                    "Error could not parse element from sourceDB")
                self.logger.error(x)
        return parsedValues
