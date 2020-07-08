from services import *
from services.segregations import Service
from utils.authenticator import Authenticator


class BizFlyClient(object):
    def __init__(self, email: str, password: str, access_token: str = None):
        self.__email = email
        self.__password = password
        self.__authenticator = Authenticator(email, password)

        if not access_token:
            self.__authorization()
        else:
            self.__token = access_token

        self.subscribers = []

    def cloud_server(self) -> CloudServer:
        """
        Create a new cloud server service instance
        :return:
        """
        cs = CloudServer(self.__token, self.__email, self.__authenticator)
        self._add_subscriber(cs)
        return cs

    def backup(self) -> Backup:
        """
        Create a new backup service instance
        :return:
        """
        ba = Backup(self.__token, self.__email, self.__authenticator)
        self._add_subscriber(ba)
        return ba

    def firewall(self) -> Firewall:
        """
        Create a new firewall service instance
        :return:
        """
        fw = Firewall(self.__token, self.__email, self.__authenticator)
        self._add_subscriber(fw)
        return fw

    def flavor(self) -> Flavor:
        """
        Create a new flavor service instance
        :return:
        """
        fv = Flavor(self.__token, self.__email, self.__authenticator)
        self._add_subscriber(fv)
        return fv

    def image(self) -> Image:
        """
        Create a new image service instance
        :return:
        """
        im = Image(self.__token, self.__email, self.__authenticator)
        self._add_subscriber(im)
        return im

    def key_pair(self) -> KeyPair:
        """
        Create a new key pair service instance
        :return:
        """
        kp = KeyPair(self.__token, self.__email, self.__authenticator)
        self._add_subscriber(kp)
        return kp

    def snapshot(self) -> Snapshot:
        """
        Create a new snapshot service instance
        :return:
        """
        ss = Snapshot(self.__token, self.__email, self.__authenticator)
        self._add_subscriber(ss)
        return ss

    def volume(self) -> Volume:
        """
        Create a new volume service instance
        :return:
        """
        vl = Volume(self.__token, self.__email, self.__authenticator)
        self._add_subscriber(vl)
        return vl

    def _add_subscriber(self, service: Service):
        """
        Subscribe resource service to client.
        Each of services that subscribe to this client get auth token updated when old one expired
        :param service:
        :return:
        """
        self.subscribers.append(service)
        update_auth_token = self.__authenticator.new_token_arrived
        if update_auth_token:
            for subscriber in self.subscribers:
                subscriber.set_auth_token(self.__authenticator.token)
            self.__authenticator.reset()

    def __authorization(self):
        self.__token = self.__authenticator.request()
        self.__authenticator.reset()
