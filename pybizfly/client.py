from services import *
from utils.authenticator import Authenticator


class BizFlyClient(object):
    def __init__(self, email: str, password: str):
        self.__email = email
        self.__password = password
        self.__authenticator = Authenticator(email, password)
        self.__token = self.__authenticator.request()

    def cloud_server(self) -> CloudServer:
        return CloudServer(self.__token, self.__email)

    def backup(self) -> Backup:
        return Backup(self.__token, self.__email)

    def firewall(self) -> Firewall:
        return Firewall(self.__token, self.__email)

    def flavor(self) -> Flavor:
        return Flavor(self.__token, self.__email)

    def image(self) -> Image:
        return Image(self.__token, self.__email)

    def key_pair(self) -> KeyPair:
        return KeyPair(self.__token, self.__email)

    def snapshot(self) -> Snapshot:
        return Snapshot(self.__token, self.__email)

    def volume(self) -> Volume:
        return Volume(self.__token, self.__email)
