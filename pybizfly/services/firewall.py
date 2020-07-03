from constants.api import ENDPOINTS
from services.segregations import Service, Listable, Gettable, Creatable, Patchable, Deletable


class Firewall(Listable, Gettable, Creatable, Patchable, Deletable):
    def create(self, name: str,
               inbound: list,
               outbound: list,
               on_services: list,
               *args, **kwargs) -> 'Service':
        return super(Firewall, self).create()

    def update(self, firewall_id: str, *args, **kwargs) -> Service:
        return super(Firewall, self).update(firewall_id)

    @staticmethod
    def __generate_create_firewall_request_body() -> dict:
        return {
            "name": "bizflycloud-firewall",
            "inbound": [
                {"type": "SSH",
                 "protocol": "TCP",
                 "port_range": "22",
                 "cidr": "0.0.0.0/0"
                 },
                {"type": "HTTP",
                 "protocol": "TCP",
                 "port_range": "80",
                 "cidr": "192.168.17.5"
                 },
                {"type": "SSH",
                 "protocol": "TCP",
                 "port_range": "22",
                 "cidr": "2001:0db8:85a3:0000:0000:8a2e:0370:7334/128"
                 }
            ],
            "outbound": [
                {"type": "PING",
                 "protocol": "ICMP",
                 "cidr": "::/0"
                 },
                {"type": "CUSTOM",
                 "protocol": "TCP",
                 "port_range": "1-255",
                 "cidr": "192.168.0.0/28"
                 }

            ],
            "targets": ["26b5cb61-95bb-417e-a1a3-2ea51f40d6ee"]
        }

    def _create_endpoint(self) -> str:
        return ENDPOINTS['FIREWALL']
