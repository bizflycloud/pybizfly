from constants.api import ENDPOINTS
from services.segregations import Service, Listable, Creatable, Deletable


class KeyPair(Listable, Creatable, Deletable):
    def create(self, name: str, public_key: str = None, *args, **kwargs) -> 'Service':
        self._request_body = self.__generate_create_key_pair_request_body(**locals())
        return super(KeyPair, self).create()

    def delete(self, name: str, *args, **kwargs) -> 'Service':
        return super(KeyPair, self).delete(name)

    @staticmethod
    def __generate_create_key_pair_request_body(**kwargs):
        key_name = kwargs.get('name')
        public_key = kwargs.get('public_key')
        if not public_key:
            return {
                "name": key_name
            }
        return {
            "name": key_name,
            "public_key": public_key
        }

    def _create_endpoint(self) -> str:
        return ENDPOINTS['KEYPAIR']
