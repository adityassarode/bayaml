from dataclasses import dataclass


@dataclass
class DriftReport:
    score: float


class DriftDetector:
    def detect(self, reference_mean: float, current_mean: float) -> DriftReport:
        return DriftReport(score=abs(reference_mean - current_mean))
