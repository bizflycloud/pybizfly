from constants.api import ENDPOINTS
from constants.services import *
from services.segregations import *
from utils.validators import validate_str_list


class CloudServer(Listable, Gettable, Creatable, Deletable):
    def get(self, server_id: str, *args, **kwargs) -> Service:
        return super(CloudServer, self).get(server_id, *args, **kwargs)

    def create(self, name: str, flavor: str, ssh_key: str,
               os_type: str, os_id: str,
               server_type: str = 'premium',
               root_disk_size: int = 20, root_disk_type: str = 'HDD',
               data_disk_size: int = 50, data_disk_type: str = 'SSD',
               password: bool = True, availability_zone: str = 'HN1') -> Service:
        self._request_body = self.__generate_create_cs_request_body(**locals())
        return super(CloudServer, self).create()

    def delete(self, server_id: str, delete_volumes: list = None, *args, **kwargs) -> Service:
        if delete_volumes:
            delete_volumes = validate_str_list(delete_volumes)
            self._request_body = {
                "delete_volume": delete_volumes
            }
        return super(CloudServer, self).delete(server_id)

    def action(self, server_id: str, request_body: dict = None) -> Service:
        # Generate /servers/<server_id>/action endpoint
        self._add_sub_endpoint(server_id)
        self._add_sub_endpoint('action')

        if request_body:
            self._request_body = request_body
        return super(CloudServer, self).create()

    def rebuild(self, server_id: str, image_id: str) -> Service:
        self._request_body = {
            'action': REBUILD,
            'image': image_id
        }
        return self.action(server_id)

    def resize(self, server_id: str, flavor_name: str) -> Service:
        self._request_body = {
            'action': RESIZE,
            'flavor_name': flavor_name
        }
        return self.action(server_id)

    def get_vnc(self, server_id: str, vnc_type: str) -> Service:
        self._request_body = {
            'action': GET_VNC,
            'type': vnc_type
        }
        return self.action(server_id)

    def add_firewall(self, server_id: str, firewall_id: str) -> Service:
        self._request_body = {
            'action': ADD_FIREWALL,
            'firewall_ids': firewall_id
        }
        return self.action(server_id)

    def change_type(self, server_id: str, new_type: str) -> Service:
        self._request_body = {
            'action': CHANGE_TYPE,
            'new_type': new_type
        }
        return self.action(server_id)

    def reset_password(self, server_id: str) -> Service:
        self._request_body = {
            'action': RESET_PASSWORD,
        }
        return self.action(server_id)

    def hard_reboot(self, server_id: str) -> Service:
        self._request_body = {
            'action': HARD_REBOOT,
        }
        return self.action(server_id)

    def soft_reboot(self, server_id: str) -> Service:
        self._request_body = {
            'action': SOFT_REBOOT,
        }
        return self.action(server_id)

    def start(self, server_id: str) -> Service:
        self._request_body = {
            'action': START,
        }
        return self.action(server_id)

    def stop(self, server_id: str) -> Service:
        self._request_body = {
            'action': STOP,
        }
        return self.action(server_id)

    @staticmethod
    def __generate_create_cs_request_body(**kwargs):
        return {
            "flavor": kwargs['flavor'],
            "name": kwargs['name'],
            "os": {
                "id": kwargs['os_id'],
                "type": kwargs['os_type']
            },
            "rootdisk": {
                "size": kwargs['root_disk_size'],
                "type": kwargs['root_disk_type']
            },
            "datadisks": [
                {
                    "size": kwargs['data_disk_size'],
                    "type": kwargs['data_disk_type']
                }
            ],
            "sshkey": kwargs['ssh_key'],
            "password": kwargs['password'],
            "type": kwargs['server_type'],
            "availability_zone": kwargs['availability_zone']
        }

    def _create_endpoint(self) -> str:
        return ENDPOINTS['CLOUD_SERVER']
