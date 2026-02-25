from typing import Dict, List
from baya.tracking.tracker import Tracker


class PerformanceTracker:
    def __init__(self, tracker: Tracker) -> None:
        self._tracker = tracker

    def latest(self, metric: str) -> float:
        history: List[float] = self._tracker.metric_history(metric)
        return history[-1]

    def degraded(self, metric: str, tolerance: float) -> bool:
        history = self._tracker.metric_history(metric)
        if len(history) < 2:
            return False
        return history[-1] < (history[-2] - tolerance)