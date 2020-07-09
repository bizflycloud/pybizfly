from pybizfly.constants.api import RESOURCE_ENDPOINTS
from pybizfly.constants.services import (RESTORE_VOLUME, DETACH, ATTACH, EXTEND, HN1, SSD)
from pybizfly.services.segregations import Service, Gettable, Creatable, Listable, Deletable
from pybizfly.utils.exceptions import BizFlyClientException
from pybizfly.utils.validators import validate_disk_type, validate_availability_zone


class Volume(Listable, Gettable, Creatable, Deletable):
    """
    Volume resource service
    Allow: list all volumes, get an individual volume, create new volume and delete existed volume
    """
    def list(self, bootable: bool = False, *args, **kwargs) -> list:
        """
        List all volumes
        :param bootable: If this is true, list all volumes that able to create cloud server
        :param args:
        :param kwargs:
        :return:
        """
        if bootable:
            self._add_parameter(key='bootable', value='true')
        return super(Volume, self).list()

    def get(self, volume_id: str, *args, **kwargs) -> dict:
        """
        Get volume
        :param volume_id: Volume id
        :param args:
        :param kwargs:
        :return:
        """
        return super(Volume, self).get(volume_id)

    def create(self, name: str, volume_size: int = 20, snapshot_id: str = None,
               volume_type: str = SSD, availability_zone: str = HN1,
               *args, **kwargs) -> dict:
        """
        Create new volume
        :param name: Volume name
        :param volume_size: Volume disk size
        :param snapshot_id:
        :param volume_type: Volume disk type, must be in (SSD, HDD)
        :param availability_zone: Volume availability zone, must be in (HN1, HN2)
        :param args:
        :param kwargs:
        :return:
        """
        validate_disk_type(volume_type, 'volume_type')
        validate_availability_zone(availability_zone)

        self._request_body = self.__generate_create_volume_request_body(**locals())
        return super(Volume, self).create()

    def delete(self, volume_id: str, *args, **kwargs) -> dict:
        """
        Delete existed volume
        :param volume_id: Volume id
        :param args:
        :param kwargs:
        :return:
        """
        return super(Volume, self).delete(volume_id)

    def action(self, volume_id: str, request_body: dict = None) -> dict:
        """
        Request action to an individual volume
        :param volume_id: Volume id
        :param request_body:
        :return:
        """
        # Generate /volumes/<volume_id>/action endpoint
        self._add_sub_endpoint(volume_id)
        self._add_sub_endpoint('action')

        if request_body:
            self._request_body = request_body
        return super(Volume, self).create()

    def restore_volume(self, volume_id: str, snapshot_id: str) -> dict:
        """
        Restore an volume based on a snapshot
        :param volume_id:  Volume id
        :param snapshot_id:  Snapshot id
        :return:
        """
        self._request_body = {
            'type': RESTORE_VOLUME,
            'snapshot_id': snapshot_id
        }
        return self.action(volume_id)

    def detach(self, volume_id: str) -> dict:
        """
        Detach an volume
        :param volume_id: Volume id
        :return:
        """
        self._request_body = {
            'type': DETACH
        }
        return self.action(volume_id)

    def attach(self, volume_id: str, instance_uuid: str) -> dict:
        """
        Attach an volume
        :param volume_id: Volume id
        :param instance_uuid:
        :return:
        """
        self._request_body = {
            'type': ATTACH,
            'instance_uuid': instance_uuid
        }
        return self.action(volume_id)

    def extend(self, volume_id: str, new_size: int) -> dict:
        """
        Extend volume size with addition size in multiple of 10.
        :param volume_id: Volume id
        :param new_size: Extended size
        :return:
        """
        # check new size mod 10
        if not self.__check_extend_size(new_size):
            raise BizFlyClientException('Invalid new_size. Must be multiples of 10')
        self._request_body = {
            'type': EXTEND,
            'new_size': new_size
        }
        return self.action(volume_id)

    @staticmethod
    def __check_extend_size(size) -> bool:
        return size % 10 == 0

    @staticmethod
    def __generate_create_volume_request_body(**kwargs) -> dict:
        """
        Create request body for create volume request
        :param kwargs:
        :return:
        """
        return {
            "name": kwargs['name'],
            "size": kwargs['volume_size'],
            "volume_type": kwargs['volume_type'],
            "availability_zone": kwargs['availability_zone']
        }

    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['VOLUME']
