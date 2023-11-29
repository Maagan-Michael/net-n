from abc import abstractmethod


class Adapter:
    @abstractmethod
    def getDevices(self):
        """gets the devices from the adapter"""
        pass

    @abstractmethod
    def getDevicesNames(self):
        """gets the devices from the adapter"""
        pass
