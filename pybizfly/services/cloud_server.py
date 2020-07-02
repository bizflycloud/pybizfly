from services.service import Service
from constants.api import ENDPOINTS
from utils.validators import validate_str_list


class CloudServer(Service):
    def post(self, name: str, flavor: str, ssh_key: str,
             os_type: str, os_id: str,
             server_type: str = 'premium',
             root_disk_size: int = 20, root_disk_type: str = 'HDD',
             data_disk_size: int = 50, data_disk_type: str = 'SSD',
             password: bool = True, availability_zone: str = 'HN1') -> Service:
        self._request_body = {
            "flavor": flavor,
            "name": name,
            "os": {
                "id": os_id,
                "type": os_type
            },
            "rootdisk": {
                "size": root_disk_size,
                "type": root_disk_type
            },
            "datadisks": [
                {
                    "size": data_disk_size,
                    "type": data_disk_type
                }
            ],
            "sshkey": ssh_key,
            "password": password,
            "type": server_type,
            "availability_zone": availability_zone
        }

        return super(CloudServer, self).post()

    def rebuild(self, server_id: str, image_id: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'rebuild',
            'image': image_id
        }
        return super(CloudServer, self).post()

    def resize(self, server_id: str, flavor_name: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'reseize',
            'flavor_name': flavor_name
        }
        return super(CloudServer, self).post()

    def get_vnc(self, server_id: str, vnc_type: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'get_vnc',
            'type': vnc_type
        }
        return super(CloudServer, self).post()

    def add_firewall(self, server_id: str, firewall_id: str) -> Service:
        self._add_sub_endpoint(server_id)
        self._add_sub_endpoint('action')

        self._request_body = {
            'action': 'add_firewall',
            'firewall_ids': firewall_id
        }
        return super(CloudServer, self).post()

    def change_type(self, server_id: str, new_type: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'add_firewall',
            'new_type': new_type
        }
        return super(CloudServer, self).post()

    def reset_password(self, server_id: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'reset_password',
        }
        return super(CloudServer, self).post()

    def hard_reboot(self, server_id: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'hard_reboot',
        }
        return super(CloudServer, self).post()

    def soft_reboot(self, server_id: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'soft_reboot',
        }
        return super(CloudServer, self).post()

    def start(self, server_id: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'start',
        }
        return super(CloudServer, self).post()

    def stop(self, server_id: str) -> Service:
        self.__decorate_action(server_id)
        self._request_body = {
            'action': 'stop',
        }
        return super(CloudServer, self).post()

    def delete(self, _id: str, delete_volumes: list = None, *args, **kwargs) -> 'Service':
        if delete_volumes:
            delete_volumes = validate_str_list(delete_volumes)
            self._request_body = {
                "delete_volume": delete_volumes
            }
        return super(CloudServer, self).delete(_id)

    def __decorate_action(self, server_id: str):
        self._add_sub_endpoint(server_id)
        self._add_sub_endpoint('action')

    def _create_endpoint(self) -> str:
        return ENDPOINTS['CLOUD_SERVER']
