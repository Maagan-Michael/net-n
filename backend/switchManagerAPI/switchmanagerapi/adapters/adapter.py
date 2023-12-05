from abc import abstractmethod
from typing import List


class Adapter:
    def __init__(self):
        self.switches: List[dict] = []

    @abstractmethod
    def getSwitches(self) -> List[dict]:
        """gets the devices from the adapter"""
        pass

    @abstractmethod
    def getSwitchInterfaces(self, ip: str) -> List[dict]:
        """gets the interfaces from the adapter"""
        pass

    @abstractmethod
    def getSwitchInterface(self, ip: str, port: int) -> dict:
        """gets the interface for a specific device"""
        pass

    @abstractmethod
    def togglePort(self, ip: str, port: int, state: bool):
        """sets the interface for a specific device up / down"""
        pass
