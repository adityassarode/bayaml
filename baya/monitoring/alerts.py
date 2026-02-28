class AlertManager:
    def should_alert(self, value: float, threshold: float) -> bool:
        return value > threshold
