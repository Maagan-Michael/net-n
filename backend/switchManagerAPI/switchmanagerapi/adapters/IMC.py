from pyhpeimc.auth import *
from pyhpeimc.plat.device import *
from .adapter import Adapter


class IMCAdapter(Adapter):
    """
        IMCAdapter is an adapter for the HP IMC API.
    """

    def __init__(self, https: bool = False, host: str = None, port: int = 80, user: str = None, password: str = None):
        super().__init__()
        self.auth = IMCAuth("https://" if https else "http://",
                            host, port, user, password)

    def getSwitches(self):
        self.switches = get_all_devs(auth=self.auth.creds, url=self.auth.url)
        return self.switches

    def getSwitchInterfaces(self, ip: str):
        res = get_all_interface_details(
            auth=self.auth.creds,
            url=self.auth.url,
            devip=ip
        )
        res = [i for i in res if i["ifType"] == "53"]  # virtual
        return res

    def getSwitchInterface(self, ip: str, port: int) -> dict:
        inter = get_interface_details(
            ifindex=str(port),
            auth=self.auth.creds,
            url=self.auth.url,
            devip=ip,
        )
        if (inter["ifType"] == "53"):
            return inter
        return None

    def togglePort(self, ip: str, port: int, state: bool):
        """sets the interface up / down"""
        interfaces = self.getSwitchInterfaces(ip)
        assert len(interfaces) > 0
        interfaces = [
            i for i in interfaces if (
                # virtual connections only need to check wanted behavior; physical connections == "6" need to check both
                i["ifType"] == "53"
                and i["ifIndex"] == str(port)
            )
        ]
        assert len(interfaces) > 0
        if (state):
            set_interface_up(port, self.auth.creds, self.auth.url, devip=ip)
        else:
            set_interface_down(port, self.auth.creds, self.auth.url, devip=ip)
