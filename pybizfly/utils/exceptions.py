class BizFlyClientException(Exception):
    pass


class BadRequestException(BizFlyClientException):
    pass


class MethodNotAllowException(BizFlyClientException):
    pass


class NotAcceptableException(BizFlyClientException):
    pass


class ResourceException(BizFlyClientException):
    pass


class InvalidIdentityException(BizFlyClientException):
    pass


class ForbiddenException(BizFlyClientException):
    pass
