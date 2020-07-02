import json

from utils.validators import validate_str_list, validate_dict_list


def should_retry() -> bool:
    pass


def retry_request():
    pass


def serialize_json(json_content) -> dict:
    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        # raise error
        return {}


def build_uri(uri: str, sub_endpoints: list, parameters: list):
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
