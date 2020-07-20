import pytest
from pybizfly.utils.validators import __in_list, validate_str_list
from pybizfly.utils.exceptions import ExcludeValueException

HAYSTACK = ['item1', 'item2', 'item3', 'item4']


@pytest.mark.parametrize('needle, haystack, message', [
    (None, HAYSTACK, 'None must not in list'),
    ('item5', HAYSTACK, 'item5 must not in list'),
])
def test_not_in_list(needle, haystack: list, message: str):
    try:
        __in_list(item=needle, haystack=haystack, name_to_call='')
        assert False, message
    except ExcludeValueException:
        assert True


@pytest.mark.parametrize('needle, haystack, message', [
    ('item4', HAYSTACK, 'item4 must in list')
])
def test_in_list(needle, haystack: list, message: str):
    try:
        __in_list(item=needle, haystack=haystack, name_to_call='')
        assert True
    except ExcludeValueException:
        assert False, message


@pytest.mark.parametrize('haystack, expected_haystack, message', [
    (['str1', 'str2', 'str3'], ['str1', 'str2', 'str3'], 'All items must be left untouched'),
])
def test_validate_str_list(haystack: list, expected_haystack: list, message):
    validated_result = validate_str_list(haystack)
    not_error = True
    for item in validated_result:
        if item not in expected_haystack:
            not_error = False
            break

    if not_error:
        message = ''
    assert not_error, message
