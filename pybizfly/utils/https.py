import json
import time

import requests

from pybizfly.constants.methods import GET, METHODS
from pybizfly.constants.response_codes import TOO_MANY_REQUEST
from pybizfly.utils.validators import validate_str_list, validate_dict_list, validate_method


def _should_retry(response_status: int) -> bool:
    """
    Determine that request with specific response status should be continued to be retried
    :param response_status: HTTP request response status
    :return:
    """
    # Retry on 5xx
    if response_status >= 500:
        return True

    # Retry on 429
    if response_status == TOO_MANY_REQUEST:
        return True

    return False


def _retry_request(num_retry: int, uri: str, method: str, **kwargs):
    """
    Retry HTTP request in number of times.
    :param num_retry:
    :param uri:
    :param method:
    :param kwargs:
    :return:
    """
    response = None
    response_status = None
    response_content = None

    validate_method(method)
    for retry_num in range(num_retry + 1):
        if retry_num > 0:
            # sleep 1 sec for each retry
            time.sleep(1)
        try:
            exception = None
            response = requests.request(method=method, url=uri, **kwargs)
        except requests.exceptions.RequestException as re:
            exception = re

        if retry_num == num_retry:
            if exception:
                raise exception
            else:
                continue

        response_status = response.status_code
        response_content = serialize_json(response.content)
        if not _should_retry(response_status):
            break

    return response_status, response_content


def serialize_json(json_content) -> dict:
    """
    Serialize json data to dict
    :param json_content:
    :return:
    """
    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        # raise error
        return {"messsage": str(json_content)}


def build_uri(uri: str, sub_endpoints: list, parameters: list):
    """
    Build uri with sub endpoints and URL parameters
    :param uri:
    :param sub_endpoints:
    :param parameters:
    :return:
    """
    parameters = validate_dict_list(parameters)
    sub_endpoints = validate_str_list(sub_endpoints)
    for sub_endpoint in sub_endpoints:
        sub_endpoint = str(sub_endpoint)
        uri += '/{}'.format(sub_endpoint)

    if len(parameters) > 0:
        first_parameter = parameters.pop()
        uri += '?{}={}'.format(*first_parameter.item())

    for parameter in parameters:
        uri += '&{}={}'.format(*parameter.items())

    return uri


class HttpRequest(object):
    def __init__(self, url: str, method: str = GET, body=None, headers=None):
        self.url = url
        if method not in METHODS:
            method = GET
        self.method = method
        self.body = body
        self.headers = headers or {}

    def execute(self, num_retry: int = 0, url: str = '', method: str = None, body=None, headers=None):
        if self.method == GET:
            self.body = None

        url = url or self.url
        method = method or self.method
        body = body or self.body
        headers = headers or self.headers

        validate_method(method)
        return _retry_request(num_retry,
                              uri=url,
                              method=method,
                              json=body,
                              headers=headers)
