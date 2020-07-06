from constants.api import RESOURCE_ENDPOINTS
from constants.services import (RESTORE_VOLUME, DETACH, ATTACH, EXTEND, HN1, SSD)
from services.segregations import Service, Gettable, Creatable, Listable, Deletable
from utils.exceptions import BizFlyClientException
from utils.validators import validate_disk_type, validate_availability_zone


class Volume(Listable, Gettable, Creatable, Deletable):
    def list(self, bootable: bool = False, *args, **kwargs) -> 'Service':
        if bootable:
            self._add_parameter(key='bootable', value='true')
        return super(Volume, self).list()

    def get(self, volume_id: str, *args, **kwargs) -> 'Service':
        return super(Volume, self).get(volume_id)

    def create(self, name: str, volume_size: int = 20, snapshot_id: str = None,
               volume_type: str = SSD, availability_zone: str = HN1,
               *args, **kwargs) -> 'Service':

        validate_disk_type(volume_type, 'volume_type')
        validate_availability_zone(availability_zone)

        self._request_body = self.__generate_create_volume_request_body(**locals())
        return super(Volume, self).create()

    def delete(self, volume_id: str, *args, **kwargs) -> 'Service':
        return super(Volume, self).delete(volume_id)

    def action(self, volume_id: str, request_body: dict = None) -> Service:
        # Generate /volumes/<volume_id>/action endpoint
        self._add_sub_endpoint(volume_id)
        self._add_sub_endpoint('action')

        if request_body:
            self._request_body = request_body
        return super(Volume, self).create()

    def restore_volume(self, volume_id: str, snapshot_id: str) -> Service:
        self._request_body = {
            'type': RESTORE_VOLUME,
            'snapshot_id': snapshot_id
        }
        return self.action(volume_id)

    def detach(self, volume_id: str) -> Service:
        self._request_body = {
            'type': DETACH
        }
        return self.action(volume_id)

    def attach(self, volume_id: str, instance_uuid: str) -> Service:
        self._request_body = {
            'type': ATTACH,
            'instance_uuid': instance_uuid
        }
        return self.action(volume_id)

    def extend(self, volume_id: str, new_size: int) -> Service:
        # check new size mod 10
        if not self.__check_extend_size(new_size):
            raise BizFlyClientException('Invalid new_size. Must be multiples of 10')
        self._request_body = {
            'type': EXTEND,
            'new_size': new_size
        }
        return self.action(volume_id)

    @staticmethod
    def __check_extend_size(size):
        return size % 10 == 0

    @staticmethod
    def __generate_create_volume_request_body(**kwargs):
        return {
            "name": kwargs['name'],
            "size": kwargs['volume_size'],
            "volume_type": kwargs['volume_type'],
            "availability_zone": kwargs['availability_zone']
        }

    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['VOLUME']
