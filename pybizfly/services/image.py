from constants.api import RESOURCE_ENDPOINTS
from services.segregations import Listable


class Image(Listable):
    # only list images
    def _create_endpoint(self) -> str:
        return RESOURCE_ENDPOINTS['OS_IMAGE']
