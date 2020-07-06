from constants.api import RESOURCE_ENDPOINTS
from services.segregations import Listable


class Flavor(Listable):
    # Only list flavors allow
    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['FLAVOR']
