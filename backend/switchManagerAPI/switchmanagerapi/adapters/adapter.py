from abc import abstractmethod
from datetime import datetime
from typing import List, Optional


class Adapter:
    def __init__(self):
        self.devices: List[dict] = []
        lastSync: Optional[datetime] = None

    def getDevices(self) -> List[dict]:
        """gets the devices from the adapter"""
        lastSync = datetime.now()
        return self.devices

    @abstractmethod
    def getDevicesNames(self):
        """gets the devices from the adapter"""
        pass
