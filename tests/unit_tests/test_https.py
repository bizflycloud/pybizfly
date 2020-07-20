import pytest

from pybizfly.utils.https import build_uri


@pytest.mark.parametrize('sub_endpoints, parameters, expected', [
    (
            ['users', '07e17zb3-6574-5ae1-b43f-6fb78c9bf164', 'action'],
            [{'with': 'server'}, {'vat': 'true'}],
            '/users/07e17zb3-6574-5ae1-b43f-6fb78c9bf164/action?vat=true&with=server'
    )
])
def test_build_uri(sub_endpoints: list, parameters: list, expected: str):
    built_uri = build_uri('', sub_endpoints, parameters)
    assert built_uri == expected
