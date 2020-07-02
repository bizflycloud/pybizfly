import json


def should_retry() -> bool:
    pass


def retry_request():
    pass


def json_serialize(json_content) -> dict:
    try:
        return json.loads(json_content)
    except json.JSONDecodeError:
        return {}
