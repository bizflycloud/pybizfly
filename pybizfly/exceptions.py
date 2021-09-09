class HTTPException(Exception):
    """
    The base exception class for all HTTP exceptions in this library raises
    """

    def __init__(self, http_status: int, message: str = None, request_id: str = None):
        self.http_status = http_status
        self.message = message or getattr(self.__class__, 'message', None)
        self.request_id = request_id

    def __str__(self):
        formatted_str = f"{self.message} (HTTP {self.http_status} (Request-ID: {self.request_id})"
        return formatted_str


class BadRequest(HTTPException):
    """
    HTTP 400 - Bad request: you sent some malformed data.
    """
    http_status = 400
    message = "Bad request"


class Unauthorized(HTTPException):
    """
    HTTP 401 - Unauthorized: bad credentials.
    """
    http_status = 401
    message = "Unauthorized"


class PaymentRequired(HTTPException):
    """
    HTTP 402 - Payment Required
    """
    http_status = 402
    message = "Payment required"


class Forbidden(HTTPException):
    """
    HTTP 403 - Forbidden: your credentials don't give you access to this
    resource.
    """
    http_status = 403
    message = "Forbidden"


class NotFound(HTTPException):
    """
    HTTP 404 - Not found
    """
    http_status = 404
    message = "Not found"


class MethodNotAllowed(HTTPException):
    """
    HTTP 405 - Method Not Allowed
    """
    http_status = 405
    message = "Method Not Allowed"


class NotAcceptable(HTTPException):
    """
    HTTP 406 - Not Acceptable
    """
    http_status = 406
    message = "Not Acceptable"


class RequestTimeout(HTTPException):
    """
    HTTP 408 - Request Timeout
    """
    http_status = 408
    message = "Request Timeout"


class Conflict(HTTPException):
    """
    HTTP 409 - Conflict
    """
    http_status = 409
    message = "Conflict"


class InternalServerError(HTTPException):
    """
    HTTP 500 - Internal Server Error
    """
    http_status = 500
    message = "Internal Server Error"


class HTTPNotImplemented(HTTPException):
    """
    HTTP 501 - Not Implemented
    """
    http_status = 501
    message = "Not Implemented"


class BadGateway(HTTPException):
    """
    HTTP 502 - Bad Gateway
    """
    http_status = 502
    message = "Bad Gateway"


class ServiceUnavailable(HTTPException):
    """
    HTTP 503 - Service Unavailable
    """
    http_status = 503
    message = "Service Unavailable"


class GatewayTimeout(HTTPException):
    """
    HTTP 504 - Gateway Timeout
    """
    http_status = 504
    message = "Gateway Timeout"


_code_map = {c.http_status: c
             for c in [BadRequest, Unauthorized, PaymentRequired,
                       Forbidden, NotFound, MethodNotAllowed, NotAcceptable,
                       RequestTimeout, Conflict, InternalServerError, HTTPNotImplemented,
                       BadGateway, ServiceUnavailable, GatewayTimeout]}


def from_response(response, body):
    """
    Return an instance of a HTTPException
    Usage:

        resp, body = requests.request(...)
        if resp.status_code != 200:
            raise exceptions.from_response(resp, resp.text)
    """
    cls = _code_map.get(response.status_code, HTTPException)
    request_id = None
    if response.headers:
        for k, v in response.headers.items():
            if 'request-id' in k.lower():
                request_id = v
                break
    message = body.get('message', 'Unknown')
    return cls(http_status=response.status_code, request_id=request_id,
               message=message)
