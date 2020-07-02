from abc import ABC, abstractmethod

import requests

from constants.api import DASHBOARD_URI
from constants.methods import *
from utils.https import json_serialize, should_retry, retry_request


class Service(ABC):
    def __init__(self, auth_token: str, email: str):
        self.auth_token = auth_token
        self.email = email
        self.attributes = {}
        self._method = GET
        self.__sub_endpoints = []

    def execute(self) -> dict:
        url = self.__build_uri()
        headers = self._create_headers()

        common_request_kwargs = {
            'method': self._method,
            'url': url,
            'headers': headers
        }

        if self._method != GET:
            json_body = self._deserialize()
            response = requests.request(**common_request_kwargs, json=json_body)
        else:
            response = requests.request(**common_request_kwargs)

        if response.status_code == 200:
            self.attributes = json_serialize(response.content)
        return self.attributes

    def list(self, *args, **kwargs) -> 'Service':
        self._method = GET
        return self

    def get(self, _id: str, *args, **kwargs) -> 'Service':
        self._method = GET
        self._add_sub_endpoint(_id)
        return self

    def create(self, *args, **kwargs) -> 'Service':
        self._method = CREATE
        return self

    def update(self, _id: str, *args, **kwargs) -> 'Service':
        self._add_sub_endpoint(_id)
        self._method = UPDATE
        return self

    def delete(self, _id: str, *args, **kwargs) -> 'Service':
        self._add_sub_endpoint(_id)
        self._method = DELETE
        return self

    def _add_sub_endpoint(self, sub_endpoint: str):
        self.__sub_endpoints.append(sub_endpoint)

    def _create_headers(self):
        return {
            'X-Auth-Token': self.auth_token,
            'X-Tenant-Name': self.email,
            'Content-Type': 'application/json'
        }

    def _validate(self, validating: dict) -> bool:
        for key, value in self.attributes:
            if key not in validating.keys():
                return False
        return True

    def __build_uri(self):
        base_uri = DASHBOARD_URI.format(self._create_endpoint())
        for sub_endpoint in self.__sub_endpoints:
            try:
                sub_endpoint = str(sub_endpoint)
                base_uri += '/{}'.format(sub_endpoint)
            except ValueError:
                continue
        return base_uri

    @abstractmethod
    def _deserialize(self) -> dict:
        pass

    @abstractmethod
    def _create_endpoint(self) -> str:
        pass
