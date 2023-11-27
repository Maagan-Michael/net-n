from typing import Any, Dict, List
from pydantic import BaseModel
import logging
from .interface import ISyncModule, DBConfig, TargetDataType
from sqlalchemy import create_engine


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
    apiUrl: str

    col_name_customer_id: str
    col_name_customer_firstname: str
    col_name_customer_lastname: str
    col_name_customer_type: str
    col_name_customer_address: str
    col_name_connection_toggled: str


class SyncModule(ISyncModule):
    """SyncModule is the module that syncs the data from the source database to the target database"""

    def __init__(self, config: SyncModuleConfig):
        super().__init__(config.destination, config.apiUrl)
        self.config = config
        self.logger = logging.getLogger('syncmodule')
        self.logger.info('SyncModule init')

    def getSourceData(self) -> List[TargetDataType]:
        """gets the data from the source database"""
        url = self.config.source.generateUrl()
        engine = create_engine(url)
        columns = ",".join([
            self.config.col_name_customer_id,
            self.config.col_name_customer_firstname,
            self.config.col_name_customer_lastname,
            self.config.col_name_customer_type,
            self.config.col_name_customer_address,
            self.config.col_name_connection_toggled
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
