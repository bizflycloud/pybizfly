from constants.api import RESOURCE_ENDPOINTS
from services.segregations import Listable


class Image(Listable):
    """
    Image resource listable service
    Allow list all os images that are able to create cloud server
    """
    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['OS_IMAGE']
