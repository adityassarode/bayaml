from dataclasses import dataclass
from typing import Dict
import numpy as np


@dataclass(frozen=True)
class DriftReport:
    feature_scores: Dict[str, float]
    drifted: bool


class DriftDetector:
    def __init__(self, threshold: float = 0.2) -> None:
        self._threshold = threshold

    def _psi(self, ref: np.ndarray, cur: np.ndarray, bins: int = 10) -> float:
        ref_hist, bin_edges = np.histogram(ref, bins=bins, density=True)
        cur_hist, _ = np.histogram(cur, bins=bin_edges, density=True)

        ref_hist = np.clip(ref_hist, 1e-6, None)
        cur_hist = np.clip(cur_hist, 1e-6, None)

        return float(np.sum((cur_hist - ref_hist) * np.log(cur_hist / ref_hist)))

    def compare(self, reference: Dict[str, np.ndarray], current: Dict[str, np.ndarray]) -> DriftReport:
        scores: Dict[str, float] = {}
        drifted = False

        for col in reference:
            score = self._psi(reference[col], current[col])
            scores[col] = score
            if score > self._threshold:
                drifted = True

        return DriftReport(scores, drifted)