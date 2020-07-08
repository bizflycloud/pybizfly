from constants.api import RESOURCE_ENDPOINTS
from services.segregations import Service, Gettable, Listable, Creatable, Deletable


class Snapshot(Listable, Gettable, Creatable, Deletable):
    """
    Snapshot resource service
    Allow list snapshots, get individual snapshot, create new snapshot and delete existed snapshot
    """
    def list(self, bootable: bool = False, *args, **kwargs) -> 'Service':
        """
        List all snapshots base on auth token
        :param bootable: If this is true, list all snapshots that able to create cloud server
        :param args:
        :param kwargs:
        :return:
        """
        if bootable:
            self._add_parameter(key='bootable', value='true')

        return super(Snapshot, self).list()

    def get(self, snapshot_id: str, *args, **kwargs) -> 'Service':
        """
        Get individual snapshot
        :param snapshot_id: Snapshot id
        :param args:
        :param kwargs:
        :return:
        """
        return super(Snapshot, self).get(snapshot_id)

    def create(self, name: str, volume_id: str, force: bool = True, *args, **kwargs) -> 'Service':
        """
        Create snapshot based on an image
        :param name: Snapshot name
        :param volume_id: Volume id
        :param force:
        :param args:
        :param kwargs:
        :return:
        """
        self._request_body = self.__generate_create_snapshot_request_body(**locals())
        return super(Snapshot, self).create()

    def delete(self, snapshot_id: str, *args, **kwargs) -> 'Service':
        """
        Delete a snapshot
        :param snapshot_id: Snapshot id
        :param args:
        :param kwargs:
        :return:
        """
        return super(Snapshot, self).delete(snapshot_id)

    @staticmethod
    def __generate_create_snapshot_request_body(**kwargs):
        return {
            "name": kwargs['name'],
            "volume_id": kwargs['volume_id'],
            "force": kwargs['force']
        }

    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['SNAPSHOT']
