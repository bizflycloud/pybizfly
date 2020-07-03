from constants.api import ENDPOINTS
from services.segregations import Listable


class Flavor(Listable):
    # Only list flavors allow
    def _create_endpoint(self) -> str:
        return ENDPOINTS['FLAVORS']
