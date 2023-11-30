from pyhpeimc.auth import *
from pyhpeimc.plat.device import *
from .adapter import Adapter


class IMCAdapter(Adapter):
    def __init__(self, https: bool = False, host: str = None, port: int = 80, user: str = None, password: str = None):
        super().__init__()
        self.auth = IMCAuth("https://" if https else "http://",
                            host, port, user, password)

    def getDevices(self):
        self.devices = get_all_devs(auth=self.auth.creds, url=self.auth.url)

        print(self.devices)
        return self.devices

    def getDevicesNames(self):
        return [device['name'] for device in self.devices]

    def togglePort(self, ip: str, port: int, state: bool):
        """sets the interface up / down"""
        interfaces = get_all_interface_details(
            auth=self.auth.creds,
            url=self.auth.url,
            devip=ip
        )
        assert len(interfaces) > 0
        interface = [
            i for i in interfaces if (
                i["ifType"] == "6"  # or i["ifTypeDesc"] == "ETHERNETCSMACD"
                and i["ifIndex"] == str(port)
            )
        ]
        assert len(interface) > 0
        if (state):
            set_interface_up(port, self.auth.creds, self.auth.url, devip=ip)
        else:
            set_interface_down(port, self.auth.creds, self.auth.url, devip=ip)
