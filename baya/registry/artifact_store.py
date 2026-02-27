class ArtifactStore:
    def __init__(self) -> None:
        self._items = {}

    def put(self, key: str, value: str) -> None:
        self._items[key] = value
