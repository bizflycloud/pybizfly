from services import *
from services.segregations import Service
from utils.authenticator import Authenticator
from utils.exceptions import AuthenticationException


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
        cs = CloudServer(self.__token, self.__email)
        self.subscribers.append(cs)
        return cs

    def backup(self) -> Backup:
        ba = Backup(self.__token, self.__email)
        self.subscribers.append(ba)
        return ba

    def firewall(self) -> Firewall:
        fw = Firewall(self.__token, self.__email)
        self.subscribers.append(fw)
        return fw

    def flavor(self) -> Flavor:
        fv = Flavor(self.__token, self.__email)
        self.subscribers.append(fv)
        return fv

    def image(self) -> Image:
        im = Image(self.__token, self.__email)
        self.subscribers.append(im)
        return im

    def key_pair(self) -> KeyPair:
        kp = KeyPair(self.__token, self.__email)
        self.subscribers.append(kp)
        return kp

    def snapshot(self) -> Snapshot:
        ss = Snapshot(self.__token, self.__email)
        self.subscribers.append(ss)
        return ss

    def volume(self) -> Volume:
        vl = Volume(self.__token, self.__email)
        self.subscribers.append(vl)
        return vl

    def _add_subscriber(self, service: Service):
        self.subscribers.append(service)
        update_auth_token = self.__authenticator.new_token_arrived
        if update_auth_token:
            for subscriber in self.subscribers:
                subscriber.set_auth_token(self.__authenticator.token)
            self.__authenticator.reset()

    def __authorization(self):
        self.__token = self.__authenticator.request()
        self.__authenticator.reset()
        if self.__authenticator.request_status == 401:
            raise AuthenticationException()
