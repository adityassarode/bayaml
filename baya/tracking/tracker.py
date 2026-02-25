from __future__ import annotations

from typing import Dict, Any
from pathlib import Path
from datetime import datetime

from baya.reproducibility.run_manifest import RunManifest
from .storage import Storage


class Tracker:
    def __init__(self, manifest: RunManifest, root: Path) -> None:
        self.manifest = manifest
        self.storage = Storage(root / manifest.run_id)

        self._metrics: Dict[str, Any] = {}
        self._params: Dict[str, Any] = {}
        self._artifacts: Dict[str, Any] = {}

    # -------------------------------------
    # Logging
    # -------------------------------------

    def log_param(self, key: str, value: Any) -> None:
        self._params[key] = value

    def log_metric(self, key: str, value: Any) -> None:
        self._metrics[key] = value

    def log_artifact(self, name: str, metadata: Dict[str, Any]) -> None:
        self._artifacts[name] = metadata

    # -------------------------------------
    # Finalization
    # -------------------------------------

    def finalize(self) -> None:
        payload = {
            "manifest": self.manifest.__dict__,
            "params": self._params,
            "metrics": self._metrics,
            "artifacts": self._artifacts,
            "completed_at": datetime.utcnow().isoformat(),
        }

        self.storage.save_json("run", payload)