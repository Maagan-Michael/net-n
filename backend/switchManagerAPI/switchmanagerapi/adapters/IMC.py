from pyhpeimc.auth import *
from pyhpeimc.plat.device import *


class IMCAdapter:
    def __init__(self, https: bool = False, host: str = None, port: int = 80, user: str = None, password: str = None):
        self.auth = IMCAuth("https://" if https else "http://",
                            host, port, user, password)
        self.devices: list[dict] = []

    def getDevices(self):
        self.devices = get_all_devs(self.auth)
