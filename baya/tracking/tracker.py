from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict
import uuid

from .storage import Storage


class Tracker:
    def __init__(self, root: Path) -> None:
        self.run_id = str(uuid.uuid4())
        self._storage = Storage(root / self.run_id)
        self._params: Dict[str, Any] = {}
        self._metrics: Dict[str, float] = {}

    def log_param(self, key: str, value: Any) -> None:
        self._params[key] = value

    def log_metric(self, key: str, value: float) -> None:
        self._metrics[key] = float(value)

    def log_metrics(self, metrics: Dict[str, float]) -> None:
        for k, v in metrics.items():
            self.log_metric(k, v)

    def finalize(self) -> Path:
        return self._storage.save_json(
            "run",
            {
                "run_id": self.run_id,
                "params": self._params,
                "metrics": self._metrics,
                "completed_at": datetime.now(timezone.utc).isoformat(),
            },
        )
