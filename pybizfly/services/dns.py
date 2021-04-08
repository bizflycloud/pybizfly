from pybizfly.constants.api import RESOURCE_ENDPOINTS
from pybizfly.services.segregations import Listable, Gettable, Creatable, Deletable


class DNS(Listable, Gettable, Creatable, Deletable):
    """
    DNS server resource service

    Allowing list all dns, get individual dns, create new dns and delete individual dns base on auth token
    """

    def __init__(self, auth_token: str, email: str, region: str = 'hn', region_service_map: dict = {}, service_name: str = "DNS", client=None):
        super(DNS, self).__init__(auth_token, email, region, region_service_map, service_name, client)
        self._post_request_body = []

    def get_zone(self, zone_id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint('zone')
        return super(DNS, self).get(zone_id, *args, **kwargs)

    def get_record(self, record_id: str, *args, **kwargs) -> dict:
        self._add_sub_endpoint('record')
        return super(DNS, self).get(record_id, *args, **kwargs)

    def list(self) -> dict:
        self._add_sub_endpoint('zones')
        return super(DNS, self).list()

    def add_zone(self, name:str) -> dict:
        self._request_body = self.__generate_create_dns_request_body(**locals())
        self._add_sub_endpoint('zones')
        return super(DNS, self).create()

    def delete_zone(self, zone_id) -> dict:
        self._add_sub_endpoint('zone')
        return super(DNS, self).delete(zone_id)

    def add_record(self, name:str,  zone_id: str, _type:str='A', request_body: dict = None, _ttl:int=300) -> dict:
        self._add_sub_endpoint('zone')
        self._add_sub_endpoint(zone_id)
        self._add_sub_endpoint('record')
        self._request_body = {
                "record":{
                    "name": name,
                    "ttl": _ttl,
                    "type": _type,
                    "data":[ "10.5.23.1", "20.1.1.1" ],
                    "routing_policy_data": {}}
                }
        return super(DNS, self).create()

    def delete_record(self, record_id: str) -> dict:
        self._add_sub_endpoint('record')
        return super(DNS, self).delete(record_id)

    @staticmethod
    def __generate_create_dns_request_body(**kwargs):
        """
        Generate request body for sending create cloud server request

        :param kwargs:
        :return:
        """
        base_data = {
                "zones": {
                    "name": kwargs['name']
                    }
                }

        return base_data

    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['DNS']

    @staticmethod
    def __get_local(**kwargs):
        """
        Get specific key-value pairs in local()

        :param kwargs:
        :return:
        """
        desired_keys = ['name']

        new_kwargs = {}
        for key in kwargs:
            if key in desired_keys:
                new_kwargs[key] = kwargs[key]

        return new_kwargs
