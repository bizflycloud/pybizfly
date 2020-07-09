from pybizfly.constants.api import RESOURCE_ENDPOINTS
from pybizfly.services.segregations import Service, Listable, Creatable, Deletable


class KeyPair(Listable, Creatable, Deletable):
    """
    Ssh key resource query
    Allow list all account ssh keys, create new ssh key and delete ssh key with specific name.
    """
    def create(self, name: str, key_value: str = None, *args, **kwargs) -> 'Service':
        """
        Create new ssh key
        :param name: Ssh key name
        :param key_value: Ssh key value
        :param args:
        :param kwargs:
        :return:
        """
        self._request_body = self.__generate_create_key_pair_request_body(**locals())
        return super(KeyPair, self).create()

    def delete(self, name: str, *args, **kwargs) -> 'Service':
        """
        Delete a ssh key based on its name
        :param name: Ssh key
        :param args:
        :param kwargs:
        :return:
        """
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
