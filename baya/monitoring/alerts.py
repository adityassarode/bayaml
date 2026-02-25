from dataclasses import dataclass


@dataclass(frozen=True)
class Alert:
    name: str
    triggered: bool
    message: str


class AlertManager:
    def drift(self, drifted: bool) -> Alert:
        return Alert(
            name="data_drift",
            triggered=drifted,
            message="Data drift detected" if drifted else "OK",
        )

    def performance(self, degraded: bool) -> Alert:
        return Alert(
            name="performance_drop",
            triggered=degraded,
            message="Model performance degraded" if degraded else "OK",
        )