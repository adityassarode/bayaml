from __future__ import annotations

from pathlib import Path
from typing import Any, Dict

from .tracker import Tracker


class Experiment:
    def __init__(self, tracking_root: Path) -> None:
        self.tracker = Tracker(tracking_root)

    def run_summary(self) -> Dict[str, Any]:
        return {"run_id": self.tracker.run_id}
