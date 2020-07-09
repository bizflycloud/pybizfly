from pybizfly.constants.services import (CLOUD_SERVER_DISK_TYPES, AVAILABILITY_ZONES, CLOUD_SERVER_SERVER_TYPES,
                                         CLOUD_SERVER_OS_TYPES, CLOUD_SERVER_ACTIONS)
from pybizfly.constants.methods import METHODS
from pybizfly.utils.exceptions import ExcludeValueException, InvalidTypeException, InvalidDictException


def validate_str_list(str_list: list) -> list:
    """
    Validate list with string instance items
    :param str_list:
    :return:
    """
    validate_list = []
    for item in str_list:
        try:
            item = str(item)
            validate_list.append(item)
        except ValueError:
            continue
    return validate_list


def validate_dict_list(dict_list: list) -> list:
    """
    Validate list with dict  instance items
    :param dict_list:
    :return:
    """
    validate_list = [] = list()
    for item in dict_list:
        if isinstance(item, dict):
            validate_list.append(item)
    return validate_list


def validate_method(method: str):
    """
    Restrict allowed method
    :param method:
    :return:
    """
    if method not in METHODS:
        raise ExcludeValueException('method', METHODS)


def __in_list(item, haystack: list, name_to_call: str):
    if item not in haystack:
        raise ExcludeValueException(name_to_call, haystack)


def validate_disk_type(disk_type, name_to_call: str = 'disk_type'):
    """
    Validate disk type, must be in (SSD, HDD)
    :param disk_type:
    :param name_to_call: Name to call on raising exception
    :return:
    """
    __in_list(disk_type, CLOUD_SERVER_DISK_TYPES, name_to_call)


def validate_server_type(server_type):
    """
    Validate server type. Must be in (basic, premium, enterprise)
    :param server_type:
    :return:
    """
    __in_list(server_type, CLOUD_SERVER_SERVER_TYPES, 'server_type')


def validate_availability_zone(availability_zone):
    """
    Validate availability zone. must be in (HN1, HN2)
    :param availability_zone:
    :return:
    """
    __in_list(availability_zone, AVAILABILITY_ZONES, 'availability_zone')


def validate_os_type(os_type):
    """
    Validate os type, must be in (image, snapshot, volume)
    :param os_type:
    :return:
    """
    __in_list(os_type, CLOUD_SERVER_OS_TYPES, 'os_type')


def validate_data_disks(data_disks):
    """
    Validate list of addition data disks. Each item must include (type, size)
    :param data_disks:
    :return:
    """
    count = 0
    for data_disk in data_disks:
        try:
            if not isinstance(data_disk, dict):
                raise InvalidTypeException('data_disks[{}]'.format(count), dict)
            validate_disk_type(data_disk['type'])
            if not isinstance(data_disk['size'], int):
                raise InvalidTypeException('data_disks[{}][size]'.format(count), int)
            count += 1
        except KeyError:
            raise InvalidDictException('data_disks', ['type', 'size'])


def validate_firewall_bounds(bounds_rules, name_to_call: str = None):
    """
    Validate list of firewall rules. Each item must include (type, protocol, port_range, cidr)
    :param bounds_rules:
    :param name_to_call:
    :return:
    """
    count = 0
    if not name_to_call:
        name_to_call = 'bound_rules'
    insisted = ['type', 'protocol', 'port_range', 'cidr']
    for bound in bounds_rules:
        try:
            if not isinstance(bound, dict):
                raise InvalidTypeException('{}[{}]'.format(name_to_call, count), dict)
            for key in insisted:
                if key not in bound.keys():
                    raise KeyError()
        except KeyError:
            raise InvalidDictException(name_to_call, insisted)
