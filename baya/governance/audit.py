class AuditLog:
    def __init__(self) -> None:
        self.events = []

    def record(self, event: str) -> None:
        self.events.append(event)
