from pybizfly.services import *
from pybizfly.constants.api import CATALOG_URI, RESOURCE_SERVICES
import requests
from pybizfly.services.segregations import Service
from pybizfly.utils.authenticator import Authenticator


class BizFlyClient(object):
    def __init__(self, email: str, password: str, access_token: str = None, region: str = 'hn', region_service_map: dict = {}, service_name: str = "Cloud Server"):
        def _raise_error(error, all_regions):
            all_regions_lower  = [ region.lower() for region in all_regions]
            raise error(f"Region must in {all_regions} or {all_regions_lower}")
        self.__email = email
        self.__password = password
        self.__service_name = service_name 
        self.__authenticator = Authenticator(email, password)
        services_catalog = requests.get(CATALOG_URI).json()['services']
        all_regions = set([service['region'] for service in services_catalog])
        self.__region = region if region.upper() in all_regions else _raise_error(ValueError, all_regions)
        service_names = [service['name'] for  service in services_catalog if service['region'].upper() == region.upper()]
        service_urls = [service['service_url'] for  service in services_catalog if service['region'].upper() == region.upper()]
        self.region_service_map = {
                region.upper(): {k:v for k,v in zip(service_names,service_urls)},
                }

        if not access_token:
            self.__authorization()
        else:
            self.__token = access_token

        self.subscribers = []
        
    def dns(self) -> DNS:
        self.__service_name = RESOURCE_SERVICES['DNS']
        dns = DNS(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(dns)
        return dns


    def cloud_server(self) -> CloudServer:
        """
        Create a new cloud server service instance
        :return:
        """
        cs = CloudServer(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(cs)
        return cs

    def backup(self) -> Backup:
        """
        Create a new backup service instance
        :return:
        """
        ba = Backup(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(ba)
        return ba

    def firewall(self) -> Firewall:
        """
        Create a new firewall service instance
        :return:
        """
        fw = Firewall(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(fw)
        return fw

    def flavor(self) -> Flavor:
        """
        Create a new flavor service instance
        :return:
        """
        fv = Flavor(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(fv)
        return fv

    def image(self) -> Image:
        """
        Create a new image service instance
        :return:
        """
        im = Image(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(im)
        return im

    def key_pair(self) -> KeyPair:
        """
        Create a new key pair service instance
        :return:
        """
        kp = KeyPair(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(kp)
        return kp

    def snapshot(self) -> Snapshot:
        """
        Create a new snapshot service instance
        :return:
        """
        ss = Snapshot(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(ss)
        return ss

    def volume(self) -> Volume:
        """
        Create a new volume service instance
        :return:
        """
        vl = Volume(self.__token, self.__email, self.__region, self.region_service_map, self.__service_name, self)
        self.add_subscriber(vl)
        return vl

    def update_token(self) -> bool:
        """
        Update token to all services that subscribe to this client
        :return:
        """
        update_auth_token = self.__authenticator.new_token_arrived
        if update_auth_token:
            self.__token = self.__authenticator.token
            for subscriber in self.subscribers:
                subscriber.set_auth_token(auth_token=self.__token)
            self.__authenticator.reset()

        return update_auth_token and len(self.subscribers) > 0

    def get_authenticator(self) -> Authenticator:
        return self.__authenticator

    def add_subscriber(self, service: Service):
        """
        Subscribe resource service to client.
        Each of services that subscribe to this client get auth token updated when old one expire
        :param service:
        :return:
        """
        self.subscribers.append(service)
        self.update_token()

    def __authorization(self):
        self.__token = self.__authenticator.request()
        self.__authenticator.reset()
