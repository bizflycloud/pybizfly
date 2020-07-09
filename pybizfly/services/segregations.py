from abc import ABC, abstractmethod

from pybizfly.constants.api import DASHBOARD_URI
from pybizfly.constants.methods import *
from pybizfly.utils.authenticator import Authenticator
from pybizfly.utils.https import build_uri, HttpRequest


class Service(ABC):
    def __init__(self, auth_token: str, email: str, authenticator: Authenticator = None):
        self.response_content = {}
        self.response_code = None
        self.authenticator = authenticator
        self._request_method = None
        self._request_body = {}
        self.__sub_endpoints = []
        self.__parameters = []
        self.__auth_token = auth_token
        self.__email = email

    @abstractmethod
    def _create_endpoint(self) -> str:
        pass

    def set_auth_token(self, auth_token):
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
        if self.response_code == 401 and isinstance(self.authenticator, Authenticator):
            self.__auth_token = self.authenticator.request()

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
        base_uri = DASHBOARD_URI.format(self._create_endpoint())
        return build_uri(base_uri, sub_endpoints=self.__sub_endpoints, parameters=self.__parameters)

    def __flush_request_data(self) -> bool:
        self._request_body = {}
        self.__sub_endpoints = []
        self.__parameters = []
        return True


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
