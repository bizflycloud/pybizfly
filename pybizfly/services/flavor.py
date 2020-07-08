from pybizfly.constants.api import RESOURCE_ENDPOINTS
from pybizfly.services.segregations import Listable


class Flavor(Listable):
    """
    Flavor resource listable service
    Allow list all flavors
    """
    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['FLAVOR']
