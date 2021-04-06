from abc import ABC, abstractmethod

from pybizfly.constants.api import DASHBOARD_URI, CATALOG_URI, RESOURCE_SERVICES
from pybizfly.constants.methods import GET, CREATE, UPDATE, DELETE, PUT, METHODS
from pybizfly.utils.authenticator import Authenticator
from pybizfly.utils.https import build_uri, HttpRequest
import requests


class Service(ABC):
    def __init__(self, auth_token: str, email: str, region, region_service_map, client=None):
        self.response_content = {}
        self.response_code = None

        # for update auth token
        self.__client = client
        self.__authenticator = None
        self.__prepare_service()

        self._request_method = GET
        self._request_body = {}
        self.__sub_endpoints = []
        self.__parameters = []
        self.__auth_token = auth_token
        self.__email = email
        self.__region = region
        self.__region_service_map = region_service_map

    @abstractmethod
    def _create_endpoint(self) -> str:
        pass

    def set_auth_token(self, auth_token: str):
        self.__auth_token = auth_token

    def _execute(self, method: str = None):
        url = self.__build_uri()
        headers = self._create_headers()

        if method and method in METHODS:
            self._request_method = method

        # request 5 times maximum to server
        http_request = HttpRequest(method=self._request_method, url=url, headers=headers, body=self._request_body)
        self.response_code, self.response_content = http_request.execute(5)

        # If token expires, request a new one and send request again.
        if self.response_code == 401 and isinstance(self.__authenticator, Authenticator):
            self.__auth_token = self.__authenticator.request()
            # trigger client update token
            self.__client.update_token()

            headers = self._create_headers()
            self.response_code, self.response_content = http_request.execute(5, headers=headers)

        # flush request data
        self.__flush_request_data()

        return self.response_content

    def _add_sub_endpoint(self, sub_endpoint: str):
        self.__sub_endpoints.append(sub_endpoint)

    def _add_parameter(self, key: str, value):
        self.__parameters.append({key: value})

    def _create_headers(self):
        return {
            'X-Auth-Token': self.__auth_token,
            'X-Tenant-Name': self.__email,
            'Content-Type': 'application/json'
        }

    def __build_uri(self):
        base_uri = self.__region_service_map[self.__region.upper()][RESOURCE_SERVICES['CLOUD_SERVER']] + '/' + self._create_endpoint()
        return build_uri(base_uri, sub_endpoints=self.__sub_endpoints, parameters=self.__parameters)

    def __flush_request_data(self) -> bool:
        self._request_body = {}
        self.__sub_endpoints = []
        self.__parameters = []
        return True

    def __prepare_service(self):
        # import client to trigger update token to other services that subscribe to client
        from pybizfly.client import BizFlyClient
        if isinstance(self.__client, BizFlyClient):
            self.__authenticator = self.__client.get_authenticator()
        else:
            self.__authenticator = None

        # connect client and service if client has not subscribed to client
        if self not in self.__client.subscribers:
            self.__client.add_subscriber(self)


# Interface segregation
class Gettable(Service, ABC):
    def get(self, _id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint(_id)
        return self._execute(method=GET)


class Creatable(Service, ABC):
    def create(self, *args, **kwargs) -> dict:
        return self._execute(method=CREATE)


class Patchable(Service, ABC):
    def update(self, _id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint(_id)
        return self._execute(method=UPDATE)


class Listable(Service, ABC):
    def list(self, *args, **kwargs) -> list:
        return self._execute(method=GET)


class Puttable(Service, ABC):
    def put(self, _id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint(_id)
        return self._execute(method=PUT)


class Deletable(Service, ABC):
    def delete(self, _id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint(_id)
        return self._execute(method=DELETE)
