from abc import ABC, abstractmethod

import requests

from constants.api import DASHBOARD_URI
from constants.methods import *
from utils.https import serialize_json, build_uri


class Service(ABC):
    def __init__(self, auth_token: str, email: str):
        self.auth_token = auth_token
        self.email = email
        self._request_method = None
        self._request_body = {}
        self._request_response = {}
        self.__sub_endpoints = []
        self.__parameters = []

    @abstractmethod
    def _create_endpoint(self) -> str:
        pass

    def execute(self, method: str = None) -> dict:
        url = self.__build_uri()
        headers = self._create_headers()

        if method and method in METHODS:
            self._request_method = method

        common_request_kwargs = {
            'method': self._request_method,
            'url': url,
            'headers': headers
        }

        if self._request_method != GET:
            json_body = self._request_body
            response = requests.request(**common_request_kwargs, json=json_body)
        else:
            response = requests.request(**common_request_kwargs)

        if response.status_code == 200:
            self._request_response = serialize_json(response.content)
        return self._request_response

    def _add_sub_endpoint(self, sub_endpoint: str):
        self.__sub_endpoints.append(sub_endpoint)

    def _add_parameter(self, key: str, value):
        self.__parameters.append({key: value})

    def _create_headers(self):
        return {
            'X-Auth-Token': self.auth_token,
            'X-Tenant-Name': self.email,
            'Content-Type': 'application/json'
        }

    def __build_uri(self):
        base_uri = DASHBOARD_URI.format(self._create_endpoint())
        return build_uri(base_uri, sub_endpoints=self.__sub_endpoints, parameters=self.__parameters)


# Interface segregation
class Gettable(Service, ABC):
    def get(self, _id: str, *args, **kwargs) -> Service:
        self._request_method = GET
        self._add_sub_endpoint(_id)
        return self


class Creatable(Service, ABC):
    def create(self, *args, **kwargs) -> Service:
        self._request_method = CREATE
        return self


class Patchable(Service, ABC):
    def update(self, _id: str, *args, **kwargs) -> Service:
        self._add_sub_endpoint(_id)
        self._request_method = UPDATE
        return self


class Listable(Service, ABC):
    def list(self, *args, **kwargs) -> Service:
        self._request_method = GET
        return self


class Putable(Service, ABC):
    def put(self, *args, **kwargs) -> Service:
        self._request_method = PUT
        return self


class Deletable(Service, ABC):
    def delete(self, _id: str, *args, **kwargs) -> Service:
        self._add_sub_endpoint(_id)
        self._request_method = DELETE
        return self
