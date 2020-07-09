from pybizfly.constants.api import RESOURCE_ENDPOINTS
from pybizfly.services.segregations import Service, Listable, Gettable, Creatable, Patchable, Deletable
from pybizfly.utils.validators import validate_str_list, validate_firewall_bounds


class Firewall(Listable, Gettable, Creatable, Patchable, Deletable):
    """
    Firewall resource service
    Allow list all firewalls, get firewall, create new firewall, update firewall and delete existed firewall
    """

    def get(self, firewall_id: str, *args, **kwargs) -> dict:
        """
        Get firewall
        :param firewall_id: Firewall id
        :param args:
        :param kwargs:
        :return:
        """
        return super(Firewall, self).get(firewall_id)

    def create(self, name: str,
               inbound_rules: list, outbound_rules: list,
               on_servers: list, *args, **kwargs) -> dict:
        """
        Create new firewall
        :param name: Firewall name
        :param inbound_rules: List of firewall inbound rules.
        Each item must include (type, protocol, port_range, cidr)
        :param outbound_rules: List of firewall outbound rules.
        Each item must include (type, protocol, port_range, cidr)
        :param on_servers: Set firewall on listed servers
        :param args:
        :param kwargs:
        :return:
        """
        validate_firewall_bounds(inbound_rules, 'inbound_rules')
        validate_firewall_bounds(outbound_rules, 'outbound_rules')
        validate_str_list(on_servers)
        self._request_body = self.__generate_create_firewall_request_body(**locals())
        return super(Firewall, self).create()

    def update(self, firewall_id: str,
               inbound_rules: list = None, outbound_rules: list = None,
               on_servers: list = None, *args, **kwargs) -> dict:
        """
        Update firewall
        :param firewall_id: Firewall id
        :param inbound_rules: List of firewall inbound rules.
        Each item must include (type, protocol, port_range, 'cidr)
        :param outbound_rules: List of firewall inbound rules.
        Each item must include (type, protocol, port_range, cidr)
        :param on_servers: Set firewall on listed servers
        :param args:
        :param kwargs:
        :return:
        """
        if inbound_rules:
            validate_firewall_bounds(inbound_rules)
        if outbound_rules:
            validate_firewall_bounds(outbound_rules)
        if on_servers:
            validate_str_list(on_servers)
        self._request_body = self.__generate_update_firewall_request_body(**locals())
        return super(Firewall, self).update(firewall_id)

    def delete(self, firewall_id: str, *args, **kwargs) -> dict:
        """
        Delete firewall
        :param firewall_id: Firewall id
        :param args:
        :param kwargs:
        :return:
        """
        return super(Firewall, self).delete(firewall_id)

    def delete_across_servers(self, firewall_id: str, servers: list) -> dict:
        """
        Remove firewall on listed servers
        :param firewall_id: Firewall id
        :param servers: Servers to remove firewall from
        :return:
        """
        self._add_sub_endpoint('servers')

        servers = validate_str_list(servers)
        self._request_body = {
            'servers': servers
        }
        return super(Firewall, self).delete(firewall_id)

    @staticmethod
    def __generate_create_firewall_request_body(**kwargs) -> dict:
        return {
            "name": kwargs['name'],
            "inbound": kwargs['inbound_rules'],
            "outbound": kwargs['outbound_rules'],
            "targets": kwargs['on_servers']
        }

    @staticmethod
    def __generate_update_firewall_request_body(**kwargs) -> dict:
        patch_data = {}

        on_servers = kwargs.get('on_servers')
        if on_servers:
            patch_data['targets'] = on_servers

        inbound_rules = kwargs.get('inbound_rules')
        if inbound_rules:
            patch_data['inbound'] = inbound_rules

        outbound_rules = kwargs.get('outbound_rules')
        if outbound_rules:
            patch_data['outbound'] = outbound_rules

        return patch_data

    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['FIREWALL']
