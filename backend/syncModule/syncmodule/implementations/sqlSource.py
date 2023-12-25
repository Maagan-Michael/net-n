from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict
import logging
from .interface import ConnectionDataType, CustomerDataType, ISyncModule, DBConfig, TargetDataType
from sqlalchemy import create_engine, text


class ColMapping(BaseModel):
    """ColMaps is the mapping of the source column to the target column"""
    id: str
    firstname: Optional[str] = None
    lastname: str
    type: Optional[str] = None
    address: str
    flat: str
    toggled: str


class SQLSyncModuleConfig(BaseModel):
    """
        SyncModuleConfig is the configuration for the SyncModule
        source: DBConfig is the source database configuration
        destination: DBConfig is the destination database configuration
        mapping.id is the source column name for customer id

        if firstname is None, then the lastname will be split into firstname and lastname
        mapping.firstname is the source column name for customer firstname
        mapping.lastname is the source column name for customer lastname

        mapping.type is the source column name for customer type
        mapping.address is the source column name for customer address
        mapping.toggled is the source column name for connection toggled
    """
    model_config = ConfigDict(from_attributes=True)

    source: DBConfig
    destination: DBConfig
    api_url: str

    mapping: ColMapping


class SQLSyncModule(ISyncModule):
    """SyncModule is the module that syncs the data from the source database to the target database"""

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
            [self.config.mapping.id]
            + [
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
            for x in results:
                length = len(x)
                fn, lsn = "", ""
                if splitName and x[4] is not None:
                    _values = x[4].split(" ")
                    fn = _values[0]
                    lsn = " ".join(_values[1:len(_values)])
                else:
                    fn = x[4] if x[4] is not None else ""
                    lsn = x[5] if x[5] is not None else ""
                value = TargetDataType(
                    customer=CustomerDataType(
                        id=x[0],
                        firstname=fn,
                        lastname=lsn,
                    ),
                    connection=ConnectionDataType(
                        flat=x[1],
                        address=x[2],
                        toggled=bool(x[3]),
                        autoUpdate=True,
                    )
                )
                if hasType:
                    value["customer"]["type"] = x[length - 1]
                parsedValues.append(value)
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Error could retrieve data from source database")
        return parsedValues
