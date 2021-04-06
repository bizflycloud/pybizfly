from pybizfly.constants.api import RESOURCE_ENDPOINTS
from pybizfly.services.segregations import Listable, Gettable, Creatable, Deletable
from pybizfly.utils.validators import (validate_str_list, validate_server_type, validate_disk_type,
                                       validate_availability_zone, validate_os_type, validate_data_disks,
                                       validate_cloud_server_action)


class DNS(Listable, Gettable, Creatable, Deletable):
    """
    DNS server resource service

    Allowing list all dns, get individual dns, create new dns and delete individual dns base on auth token
    """

    def __init__(self, auth_token: str, email: str, region: str = 'hn', region_service_map: dict = {}, service_name: str = "DNS", client=None):
        super(DNS, self).__init__(auth_token, email, region, region_service_map, service_name, client)
        self._post_request_body = []

    def get(self, zone_id: str, *args, **kwargs) -> dict:
        """
        Get cloud server by server_id
        :param zone_id: dns zone id
        """

        return super(DNS, self).get(zone_id, *args, **kwargs)

    def create(self, name: str) -> dict:
        self._request_body = self.__generate_create_dns_request_body(**locals())
        return super(DNS, self).create()


    def delete(self, zone_id: str, *args, **kwargs) -> dict:
        """
        Delete a dns zone

        :param server_id: Cloud server id
        """
        return super(DNS, self).delete(zone_id)

    def action(self, zone_id: str, request_body: dict = None) -> dict:
        """
        Send action to an individual cloud server

        :param server_id: Cloud server id
        :param request_body:
        :return:
        """
        # Generate /servers/<server_id>/action endpoint
        self._add_sub_endpoint(zone_id)
        self._add_sub_endpoint('action')

        if request_body:
            validate_cloud_server_action(request_body.get('action'))
            self._request_body = request_body
        return super(CloudServer, self).create()


    def change_type(self, server_id: str, new_type: str) -> dict:
        """
        Change cloud server type

        :param server_id: Cloud server id
        :param new_type: Cloud server new type, must be in (basic, premium, enterprise)
        :return:
        """
        validate_server_type(new_type)
        self._request_body = {
            'action': CHANGE_TYPE,
            'new_type': new_type
        }
        return self.action(server_id)

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
