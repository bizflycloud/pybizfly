class BizFlyClientException(Exception):
    pass


class AuthenticationException(BizFlyClientException):
    def __init__(self, message: str = None):
        if not message:
            message = 'Invalid authentication'
        super(AuthenticationException, self).__init__(message)


class ExcludeValueException(BizFlyClientException):
    def __init__(self, value: str, includes: list):
        message = "{} must be in {}".format(value, includes)
        super(ExcludeValueException, self).__init__(message)


class InvalidTypeException(BizFlyClientException):
    def __init__(self, value: str, _type: type):
        message = "{} must be instance of {}".format(value, _type)
        super(InvalidTypeException, self).__init__(message)


class InvalidDictException(BizFlyClientException):
    def __init__(self, value: str, includes: list):
        message = "{} items must include {}".format(value, includes)
        super(InvalidDictException, self).__init__(message)
