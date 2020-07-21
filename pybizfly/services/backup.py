from pybizfly.constants.api import RESOURCE_ENDPOINTS
from pybizfly.services.segregations import Gettable, Creatable, Listable, Deletable, Puttable


class Backup(Listable, Gettable, Creatable, Deletable, Puttable):
    """
    Backup resource service
    Allow list all backups, get backup, create new backup, remove existed backup and overwrite a backup
    """

    def get(self, backup_id: str, *args, **kwargs) -> dict:
        """
        Get backup.

        :param backup_id: Backup id
        :param args:
        :param kwargs:
        :return:
        """
        return super(Backup, self).get(backup_id)

    def create(self, resource_id: str,
               backup_at_time: int = 16, backup_frequency: int = 1440, backup_quantity: int = 2,
               *args, **kwargs) -> dict:
        """
        Create backup

        :param resource_id:
        :param backup_at_time: Create backup at specific hour every day
        :param backup_frequency: Backup frequency
        :param backup_quantity: Determine how many identical backup will be created
        :param args:
        :param kwargs:
        :return:
        """
        self._request_body = self.__generate_create_backup_request_body(**locals())
        return super(Backup, self).create()

    def delete(self, backup_id: str, *args, **kwargs) -> dict:
        """
        Delete backup

        :param backup_id: Backup id
        :param args:
        :param kwargs:
        :return:
        """
        return super(Backup, self).delete(backup_id)

    def put(self, backup_id: str,
            backup_at_time: int = 16, backup_frequency: int = 1440, backup_quantity: int = 2,
            *args, **kwargs) -> dict:
        """
        Overwrite of create an backup

        :param backup_id: Backup id
        :param backup_at_time: Create backup at specific hour every day
        :param backup_frequency: Backup frequency
        :param backup_quantity: Determine how many identical backup will be created
        :param args:
        :param kwargs:
        :return:
        """
        self._request_body = {
            "hour": backup_at_time,
            "frequency": backup_frequency,
            "size": backup_quantity
        }
        return super(Backup, self).put(backup_id)

    @staticmethod
    def __generate_create_backup_request_body(**kwargs):
        return {
            "resource_id": kwargs['resource_id'],
            "hour": kwargs['backup_at_time'],
            "frequency": kwargs['backup_frequency'],
            "size": kwargs['backup_quantity']
        }

    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['BACKUP_CALENDAR']
