from constants.api import RESOURCE_ENDPOINTS
from services.segregations import Service, Listable, Gettable, Creatable, Patchable, Deletable
from utils.validators import validate_str_list, validate_firewall_bounds


class Firewall(Listable, Gettable, Creatable, Patchable, Deletable):
    def get(self, firewall_id: str, *args, **kwargs) -> Service:
        return super(Firewall, self).get(firewall_id)

    def create(self, name: str,
               inbound_rules: list, outbound_rules: list,
               on_servers: list, *args, **kwargs) -> Service:
        validate_firewall_bounds(inbound_rules, 'inbound_rules')
        validate_firewall_bounds(outbound_rules, 'outbound_rules')
        validate_str_list(on_servers)
        self._request_body = self.__generate_create_firewall_request_body(**locals())
        return super(Firewall, self).create()

    def update_rules(self, firewall_id: str,
                     inbound_rules: list = None, outbound_rules: list = None,
                     on_servers: list = None, *args, **kwargs) -> Service:
        if inbound_rules:
            validate_firewall_bounds(inbound_rules)
        if outbound_rules:
            validate_firewall_bounds(outbound_rules)
        if on_servers:
            validate_str_list(on_servers)
        self._request_body = self.__generate_update_firewall_request_body(**locals())
        return super(Firewall, self).update(firewall_id)

    def delete(self, firewall_id: str, *args, **kwargs) -> Service:
        return super(Firewall, self).delete(firewall_id)

    def delete_across_servers(self, firewall_id: str, servers: list) -> Service:
        service = super(Firewall, self).delete(firewall_id)
        self._add_sub_endpoint('servers')

        servers = validate_str_list(servers)
        self._request_body = {
            'servers': servers
        }
        return service

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
