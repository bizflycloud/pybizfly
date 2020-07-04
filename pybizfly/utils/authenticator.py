from constants.api import DASHBOARD_URI, TOKEN_ENDPOINTS
from constants.methods import CREATE
from utils.exceptions import InvalidIdentityException
from utils.https import HttpRequest


class Authenticator(object):
    def __init__(self, email: str, password: str):
        self.__email = email
        self.__password = password

    def request(self) -> str:
        token_uri = DASHBOARD_URI.format(TOKEN_ENDPOINTS)
        http_request = HttpRequest(url=token_uri,
                                   method=CREATE,
                                   headers={'content-type': 'application/json'},
                                   body=self.__create_request_body())

        resp_code, resp_content = http_request.execute(5)
        return resp_content.get('token')

    def __create_request_body(self) -> dict:
        return {
            'username': self.__email,
            'password': self.__password
        }
