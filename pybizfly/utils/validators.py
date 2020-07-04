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


def validate_firewall_rules() -> list:
    """
    pass
    :return:
    """
