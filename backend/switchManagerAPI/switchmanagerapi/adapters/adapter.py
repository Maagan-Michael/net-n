from abc import abstractmethod
from typing import List


class Adapter:
    def __init__(self):
        self.devices: List[dict] = []

    @abstractmethod
    def getDevices(self) -> List[dict]:
        """gets the devices from the adapter"""
        pass

    @abstractmethod
    def getDevicesNames(self):
        """gets the devices from the adapter"""
        pass

    @abstractmethod
    def togglePort(self, ip: str, port: int, state: bool):
        """sets the interface for a specific device up / down"""
        pass
