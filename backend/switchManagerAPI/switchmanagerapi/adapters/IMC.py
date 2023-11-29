from pyhpeimc.auth import *
from pyhpeimc.plat.device import *
from .adapter import Adapter


class IMCAdapter(Adapter):
    def __init__(self, https: bool = False, host: str = None, port: int = 80, user: str = None, password: str = None):
        super().__init__()
        self.auth = IMCAuth("https://" if https else "http://",
                            host, port, user, password)

    def getDevices(self):
        self.devices = get_all_devs(self.auth)
        return self.devices

    def getDevicesNames(self):
        return [device['name'] for device in self.devices]
