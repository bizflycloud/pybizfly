from pybizfly.constants.api import DASHBOARD_URI, TOKEN_ENDPOINTS
from pybizfly.constants.methods import CREATE
from pybizfly.utils.exceptions import AuthenticationException
from pybizfly.utils.https import HttpRequest


class Authenticator(object):
    def __init__(self, email: str, password: str):
        self.token = ''
        self.request_status = None
        self.new_token_arrived = False
        self.__email = email
        self.__password = password

    def request(self) -> str:
        token_uri = DASHBOARD_URI.format(TOKEN_ENDPOINTS)
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
            'password': self.__password
        }
