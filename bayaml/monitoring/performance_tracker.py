class PerformanceTracker:
    def __init__(self) -> None:
        self.values = {}

    def update(self, key: str, value: float) -> None:
        self.values[key] = float(value)
