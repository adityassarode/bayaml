from dataclasses import dataclass
import numpy as np


@dataclass(frozen=True)
class PredictionDistribution:
    mean: float
    std: float
    min: float
    max: float


def summarize(preds: np.ndarray) -> PredictionDistribution:
    return PredictionDistribution(
        mean=float(np.mean(preds)),
        std=float(np.std(preds)),
        min=float(np.min(preds)),
        max=float(np.max(preds)),
    )