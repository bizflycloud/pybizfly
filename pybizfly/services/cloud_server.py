from pybizfly.constants.api import RESOURCE_ENDPOINTS
from pybizfly.constants.services import (REBUILD, RESIZE, GET_VNC, ADD_FIREWALL, CHANGE_TYPE, RESET_PASSWORD,
                                         HARD_REBOOT, SOFT_REBOOT, STOP, START, OS_IMAGE_TYPE, OS_VOLUME_TYPE,
                                         OS_SNAPSHOT_TYPE, SSD,
                                         PREMIUM, HN1, DEFAULT_FLAVOR)
from pybizfly.services.segregations import Listable, Gettable, Creatable, Deletable
from pybizfly.utils.authenticator import Authenticator
from pybizfly.utils.validators import (validate_str_list, validate_server_type, validate_disk_type,
                                       validate_availability_zone,
                                       validate_os_type, validate_data_disks)


class CloudServer(Listable, Gettable, Creatable, Deletable):
    """
    Cloud server resource service
    Allowing list all servers, get individual server, create new server and delete individual server base on auth token
    """

    def __init__(self, auth_token: str, email: str, authenticator: Authenticator = None):
        super(CloudServer, self).__init__(auth_token, email, authenticator)
        self._post_request_body = []

    def get(self, server_id: str, *args, **kwargs) -> dict:
        """
        Get cloud server by server_id
        :param server_id: Cloud server id
        :param args:
        :param kwargs:
        :return:
        """
        return super(CloudServer, self).get(server_id, *args, **kwargs)

    def create(self, name: str, os_type: str, os_id: str,
               flavor_name: str = DEFAULT_FLAVOR, ssh_key_name: str = None,
               server_type: str = PREMIUM,
               root_disk_size: int = 20, root_disk_type: str = SSD,
               addition_data_disks: list = None,
               password: bool = True, availability_zone: str = HN1) -> dict:
        """
        Create an cloud server.
        Stack create methods to create equivalent amount of cloud servers.
        :param name: Cloud server name
        :param os_type: Cloud server os type, must be in (image, snapshot, volume)
        :param os_id: image_id or snapshot_id or volume_id to create cloud server
        :param flavor_name:
        :param ssh_key_name: Optional ssh key adding to new cloud server
        :param server_type: Cloud server type, must be in (basic, premium, enterprise)
        :param root_disk_size: Cloud server root disk size
        :param root_disk_type: Cloud server root disk type, must be in (SSD, HDD)
        :param addition_data_disks: List of additional data disks, each item must includes (type and size)
        :param password: Create cloud server with password
        :param availability_zone: Cloud server availability zones, must be in (HN1, HN2)
        :return:
        """
        validate_os_type(os_type)
        validate_disk_type(root_disk_size)
        validate_server_type(server_type)
        validate_availability_zone(availability_zone)
        if addition_data_disks:
            validate_data_disks(addition_data_disks)

        self._post_request_body.append(self.__generate_create_cs_request_body(**locals()))
        self._request_body = self._post_request_body
        return super(CloudServer, self).create()

    def create_from_image(self, name, image_id: str,
                          flavor_name: str = DEFAULT_FLAVOR, ssh_key_name: str = None,
                          server_type: str = PREMIUM,
                          root_disk_size: int = 20, root_disk_type: str = SSD,
                          addition_data_disks: list = None,
                          password: bool = True, availability_zone: str = HN1) -> dict:
        """
        Create cloud server based on an image
        Stack create methods to create equivalent amount of cloud servers.
        :param name: Cloud server name
        :param image_id: image_id to create cloud server
        :param flavor_name:
        :param ssh_key_name: Optional ssh key adding to new cloud server
        :param server_type: Cloud server type, must be in (basic, premium, enterprise)
        :param root_disk_size: Cloud server root disk size
        :param root_disk_type: Cloud server root disk type, must be in (SSD, HDD)
        :param addition_data_disks: List of additional data disks, each item must includes (type and size)
        :param password: Create cloud server with password
        :param availability_zone: Cloud server availability zones, must be in (HN1, HN2)
        :return:
        """
        return self.create(os_id=image_id, os_type=OS_IMAGE_TYPE, **self.__get_local(**locals()))

    def create_from_volume(self, name, volume_id: str,
                           flavor_name: str = DEFAULT_FLAVOR, ssh_key_name: str = None,
                           server_type: str = PREMIUM,
                           root_disk_size: int = 20, root_disk_type: str = SSD,
                           addition_data_disks: list = None,
                           password: bool = True, availability_zone: str = HN1) -> dict:
        """
        Create cloud server based on a volume
        Stack create methods to create equivalent amount of cloud servers.
        :param name: Cloud server name
        :param volume_id: volume_id to create cloud server
        :param flavor_name:
        :param ssh_key_name: Optional ssh key adding to new cloud server
        :param server_type: Cloud server type, must be in (basic, premium, enterprise)
        :param root_disk_size: Cloud server root disk size
        :param root_disk_type: Cloud server root disk type, must be in (SSD, HDD)
        :param addition_data_disks: List of additional data disks, each item must includes (type and size)
        :param password: Create cloud server with password
        :param availability_zone: Cloud server availability zones, must be in (HN1, HN2)
        :return:
        """
        return self.create(os_id=volume_id, os_type=OS_VOLUME_TYPE, **self.__get_local(**locals()))

    def create_from_snapshot(self, name, snapshot_id: str,
                             flavor_name: str = DEFAULT_FLAVOR, ssh_key_name: str = None,
                             server_type: str = PREMIUM,
                             root_disk_size: int = 20, root_disk_type: str = SSD,
                             addition_data_disks: list = None,
                             password: bool = True, availability_zone: str = HN1) -> dict:
        """
        Create cloud server based on a snapshot
        Stack create methods to create equivalent amount of cloud servers.
        :param name: Cloud server name
        :param snapshot_id: snapshot_id to create cloud server
        :param flavor_name:
        :param ssh_key_name: Optional ssh key adding to new cloud server
        :param server_type: Cloud server type, must be in (basic, premium, enterprise)
        :param root_disk_size: Cloud server root disk size
        :param root_disk_type: Cloud server root disk type, must be in (SSD, HDD)
        :param addition_data_disks: List of additional data disks, each item must includes (type and size)
        :param password: Create cloud server with password
        :param availability_zone: Cloud server availability zones, must be in (HN1, HN2)
        :return:
        """
        return self.create(os_id=snapshot_id, os_type=OS_SNAPSHOT_TYPE, **self.__get_local(**locals()))

    def delete(self, server_id: str, delete_volumes: list = None, *args, **kwargs) -> dict:
        """
        Delete a cloud server
        :param server_id: Cloud server id
        :param delete_volumes: List of volume to delete along
        :param args:
        :param kwargs:
        :return:
        """
        if delete_volumes:
            delete_volumes = validate_str_list(delete_volumes)
            self._request_body = {
                "delete_volume": delete_volumes
            }
        return super(CloudServer, self).delete(server_id)

    def action(self, server_id: str, request_body: dict = None) -> dict:
        """
        Send action to an individual cloud server
        :param server_id: Cloud server id
        :param request_body:
        :return:
        """
        # Generate /servers/<server_id>/action endpoint
        self._add_sub_endpoint(server_id)
        self._add_sub_endpoint('action')

        if request_body:
            self._request_body = request_body
        return super(CloudServer, self).create()

    def rebuild(self, server_id: str, image_id: str) -> dict:
        """
        Rebuild a cloud server based on an image
        :param server_id: Cloud server id
        :param image_id: Image id
        :return:
        """
        self._request_body = {
            'action': REBUILD,
            'image': image_id
        }
        return self.action(server_id)

    def resize(self, server_id: str, flavor_name: str) -> dict:
        """
        Resize a cloud server based on flavor
        :param server_id: Cloud server id
        :param flavor_name: Flavor name
        :return:
        """
        self._request_body = {
            'action': RESIZE,
            'flavor_name': flavor_name
        }
        return self.action(server_id)

    def get_vnc(self, server_id: str, vnc_type: str) -> dict:
        """
        Get cloud server vnd
        :param server_id:
        :param vnc_type:
        :return:
        """
        self._request_body = {
            'action': GET_VNC,
            'type': vnc_type
        }
        return self.action(server_id)

    def add_firewall(self, server_id: str, firewall_id: str) -> dict:
        """
        Add a firewall to cloud server
        :param server_id: Cloud server id
        :param firewall_id: Firewall id
        :return:
        """
        self._request_body = {
            'action': ADD_FIREWALL,
            'firewall_ids': firewall_id
        }
        return self.action(server_id)

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

    def reset_password(self, server_id: str) -> dict:
        """
        Reset cloud server password
        :param server_id: Cloud server id
        :return:
        """
        self._request_body = {
            'action': RESET_PASSWORD,
        }
        return self.action(server_id)

    def hard_reboot(self, server_id: str) -> dict:
        """
        Hard reboot cloud server
        :param server_id: Cloud server id
        :return:
        """
        self._request_body = {
            'action': HARD_REBOOT,
        }
        return self.action(server_id)

    def soft_reboot(self, server_id: str) -> dict:
        """
        Soft reboot cloud server
        :param server_id: Cloud server id
        :return:
        """
        self._request_body = {
            'action': SOFT_REBOOT,
        }
        return self.action(server_id)

    def start(self, server_id: str) -> dict:
        """
        Start cloud server
        :param server_id: Cloud server id
        :return:
        """
        self._request_body = {
            'action': START,
        }
        return self.action(server_id)

    def stop(self, server_id: str) -> dict:
        """
        Stop cloud server
        :param server_id: Cloud server id
        :return:
        """
        self._request_body = {
            'action': STOP,
        }
        return self.action(server_id)

    @staticmethod
    def __generate_create_cs_request_body(**kwargs):
        """
        Generate request body for sending create cloud server request
        :param kwargs:
        :return:
        """
        base_data = {
            "flavor": kwargs['flavor_name'],
            "name": kwargs['name'],
            'os': {
                "id": kwargs['os_id'],
                "type": kwargs['os_type']
            },
            "rootdisk": {
                "size": kwargs['root_disk_size'],
                "type": kwargs['root_disk_type']
            },

            "password": kwargs['password'],
            "type": kwargs['server_type'],
            "availability_zone": kwargs['availability_zone']
        }
        # add ssh key if exist
        ssh_key = kwargs.get('ssh_key_name')
        if ssh_key:
            base_data["sshkey"] = ssh_key

        # add data_disks if exist
        addition_data_disks = kwargs.get('addition_data_disks')
        if addition_data_disks:
            base_data['datadisks'] = addition_data_disks

        return base_data

    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['CLOUD_SERVER']

    @staticmethod
    def __get_local(**kwargs):
        """
        Get specific key-value pairs in local()
        :param kwargs:
        :return:
        """
        desired_keys = ['flavor_name', 'ssh_key_name', 'server_type', 'root_disk_size', 'root_disk_type',
                        'data_disk_size', 'data_disk_type', 'password', 'availability_zone', 'name',
                        'addition_data_disks']

        new_kwargs = {}
        for key in kwargs:
            if key in desired_keys:
                new_kwargs[key] = kwargs[key]

        return new_kwargs
