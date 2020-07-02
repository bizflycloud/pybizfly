from services.service import Service
from constants.api import ENDPOINTS


class CloudServerService(Service):
    def _deserialize(self) -> dict:
        return {
            "flavor": self.attributes['flavor'],
            "name": self.attributes['name'],
            "os": {
                "id": "9a0f31e3-c43d-4fc2-ae1c-cc6ebde571fa",
                "type": "image"
            },
            "rootdisk": {
                "size": 20,
                "type": "HDD"
            },
            "datadisks": [{
                "size": 50,
                "type": "SSD"
            }
            ]
            ,
            "sshkey": "bizflycloud",
            "password": true,
            "type": "premium",
            "availability_zone": "HN1"
        }

    def _create_endpoint(self) -> str:
        return ENDPOINTS['CLOUD_SERVER']
