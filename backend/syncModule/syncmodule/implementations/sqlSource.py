from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict
import logging
from .interface import ISyncModule, DBConfig, TargetDataType
from sqlalchemy import create_engine


class SQLSyncModuleConfig(BaseModel):
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
    model_config = ConfigDict(from_attributes=True)

    source: DBConfig
    destination: DBConfig
    api_url: str

    col_name_customer_id: str
    col_name_customer_firstname: Optional[str] = None
    col_name_customer_lastname: str
    col_name_customer_type: str
    col_name_customer_address: str
    col_name_connection_toggled: Optional[str]
    split_name: bool = False


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
        columns = ','.join(
            [self.config.col_name_customer_id]
            + ([self.config.col_name_customer_lastname] if self.config.split_name
               else [
                self.config.col_name_customer_firstname,
                self.config.col_name_customer_lastname
            ]) + [
                self.config.col_name_customer_type,
                self.config.col_name_customer_address,
            ] + [self.config.col_name_connection_toggled] if self.config.col_name_connection_toggled else []
        )
        results = []
        with engine.connect() as conn:
            results = conn.scalars(
                f"SELECT {columns} FROM {self.config.source.table}").all()
            engine.dispose()
        for x in results:
            [firstname, lastname] = x[2].split(" ") if self.config.split_name else [
                x[1], x[2]]
            x = {
                "customer": {
                    "id": x[0],
                    "firstname": firstname,
                    "lastname": lastname,
                    "type": x[3],
                },
                "connection": {
                    "address": x[4],
                    "toggled": bool(x[5])
                }
            }
        return results
