import requests

from constants.api import DASHBOARD_URI, TOKEN_ENDPOINTS
from utils.https import serialize_json


class Authenticator(object):
    def __init__(self, email: str, password: str):
        self.__email = email
        self.__password = password

    def request(self) -> str:
        token_uri = DASHBOARD_URI.format(TOKEN_ENDPOINTS)
        response = requests.post(url=token_uri,
                                 headers={'content-type': 'application/json'},
                                 json=self.__create_request_body())
        if response.status_code == 201:
            return serialize_json(response.content).get('token')
        return ''

    def __create_request_body(self) -> dict:
        return {
            'username': self.__email,
            'password': self.__password
        }


# k = KeystoneAuthenticator(email='dungpq@vccloud.vn', password='k`g`4Ib2N$Y6')
# print(k.request())
