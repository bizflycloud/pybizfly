from constants.api import ENDPOINTS
from services.segregations import Listable


class Image(Listable):
    # only list images
    def _create_endpoint(self) -> str:
        return ENDPOINTS['OS_IMAGE']
