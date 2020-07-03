from constants.api import ENDPOINTS
from services.segregations import Service, Gettable, Creatable, Listable, Deletable, Putable


class Backup(Listable, Gettable, Creatable, Deletable, Putable):
    def get(self, backup_id: str, *args, **kwargs) -> 'Service':
        return super(Backup, self).get(backup_id)

    def create(self, resource_id: str,
               backup_at_time: int = 16, backup_frequency: int = 1440, backup_quantity: int = 2,
               *args, **kwargs) -> 'Service':
        self._request_body = self.__generate_create_backup_request_body(**locals())
        return super(Backup, self).create()

    def delete(self, backup_id: str, *args, **kwargs) -> 'Service':
        return super(Backup, self).delete(backup_id)

    def put(self, *args, **kwargs) -> Service:
        return super(Backup, self).put()

    @staticmethod
    def __generate_create_backup_request_body(**kwargs):
        return {
            "resource_id": kwargs['resource_id'],
            "hour": kwargs['backup_at_time'],
            "frequency": kwargs['backup_frequency'],
            "size": kwargs['backup_quantity']
        }

    def _create_endpoint(self) -> str:
        return ENDPOINTS['BACKUP_CALENDAR']
