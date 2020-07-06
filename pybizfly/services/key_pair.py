from constants.api import RESOURCE_ENDPOINTS
from services.segregations import Service, Listable, Creatable, Deletable


class KeyPair(Listable, Creatable, Deletable):
    def create(self, name: str, key_value: str = None, *args, **kwargs) -> 'Service':
        self._request_body = self.__generate_create_key_pair_request_body(**locals())
        return super(KeyPair, self).create()

    def delete(self, name: str, *args, **kwargs) -> 'Service':
        return super(KeyPair, self).delete(name)

    @staticmethod
    def __generate_create_key_pair_request_body(**kwargs):
        key_name = kwargs.get('name')
        key_value = kwargs.get('key_value')
        if not key_value:
            return {
                "name": key_name
            }
        return {
            "name": key_name,
            "public_key": key_value
        }

    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['KEYPAIR']
