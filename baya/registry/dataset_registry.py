class DatasetRegistry:
    def __init__(self) -> None:
        self._items = {}

    def register(self, name: str, uri: str) -> None:
        self._items[name] = uri
