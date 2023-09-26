"""Types of JSON responses
"""

from utils.json_helper_functions import pretty_json
from utils.Logger import logger
from utils.configuration import get_config

class JSONColectionResponse:
    """nesseccary Data and functions so create a response containing JSON of a collection
    """

    def __init__(self, route: str, collection: list, offset: int = 0, limit: int = 20) -> None:
        self.count = len(collection)
        self.offset = offset if offset >= 0 else 0 # set to default if not greater 0
        self.limit = limit if limit > 0 else 20 # set to default if negative
        self.url = f'http://{get_config("server", "IPv4")}:{get_config("server", "port")}{route}'
        self.collection = collection
        self.prev_offset = (offset - limit) if (offset - limit) > 0 else None
        self.next_offset = (offset + limit) if (offset + limit) <= self.count else None
        self.items = self.get_items()

    def get_items(self) -> list|None:
        if self.collection is None:
            return []
        if self.offset >= self.count:
            self.prev_offset = self.count - self.limit if self.count - self.limit > 0 else None
            return []
        else:
            item_count = self.offset+self.limit if self.offset + self.limit <= self.count else self.count
            return self.collection[self.offset:(item_count)]
        
    def get_json(self):
        response_object = {
            'count': self.count,
            'offset': self.offset,
            'limit': self.limit,
            'previous': f'{self.url}?offset={self.prev_offset}&limit={self.limit}' if self.prev_offset is not None else None,
            'next': f'{self.url}?offset={self.next_offset}&limit={self.limit}' if self.next_offset is not None else None,
            'results': self.items
        }
        response = pretty_json(response_object)
        logger.debug(f'{JSONColectionResponse.get_json.__qualname__} returned: \n{response_object}')
        return response
        
        