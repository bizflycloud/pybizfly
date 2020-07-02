import requests

from constants.api import DASHBOARD_URI, TOKEN_ENDPOINTS


class KeystoneAuthenticator(object):
    def __init__(self, email: str, password: str):
        self.__email = email
        self.__password = password

    def request(self) -> str:
        token_uri = DASHBOARD_URI.format(TOKEN_ENDPOINTS)
        response = requests.post(url=token_uri,
                                 headers={'content-type': 'application/json'},
                                 json=self.__create_request_body())
        if response.status_code == 201:
            return response.headers['x-subject-token']
        return ''

    def __create_request_body(self) -> dict:
        return {
            'username': self.__email,
            'password': self.__password
        }

# from setting import KEYSTONE_AUTHTOKEN
#
# k = KeystoneAuthenticator(KEYSTONE_AUTHTOKEN)
# print(k.request())
