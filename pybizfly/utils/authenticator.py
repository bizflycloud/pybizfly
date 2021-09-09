from urllib.parse import urljoin

from pybizfly.constants.api import TOKEN_ENDPOINT, DEFAULT_HOST_URI
from pybizfly.constants.methods import CREATE
from pybizfly.utils.exceptions import AuthenticationException
from pybizfly.utils.https import HttpRequest


class Authenticator(object):
    def __init__(self, email: str, password: str, host: str = None):
        self.token = ''
        self.request_status = None
        self.new_token_arrived = False
        self.__email = email
        self.__password = password
        self.__host = host or DEFAULT_HOST_URI


    def request(self) -> str:
        token_uri = urljoin(self.__host, TOKEN_ENDPOINT)
        http_request = HttpRequest(url=token_uri,
                                   method=CREATE,
                                   headers={'content-type': 'application/json'},
                                   body=self.__create_request_body())

        self.request_status, resp_content = http_request.execute(5)
        if self.request_status == 401:
            raise AuthenticationException()
        self.new_token_arrived = True
        self.token = resp_content.get('token')
        return self.token

    def reset(self):
        self.new_token_arrived = False

    def __create_request_body(self) -> dict:
        return {
            'username': self.__email,
            'password': self.__password,
            'auth_method': 'password'
        }
