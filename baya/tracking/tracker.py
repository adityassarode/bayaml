from __future__ import annotations

from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from dataclasses import asdict

from baya.reproducibility.run_manifest import RunManifest
from .storage import Storage


class Tracker:
    """
    Run lifecycle logger.

    Responsibilities:
        - Log params, metrics, artifacts
        - Persist run payload
        - Never mutate manifest
        - Deterministic JSON persistence
    """

    def __init__(self, manifest: RunManifest, root: Path) -> None:
        self._manifest = manifest
        self._storage = Storage(root / manifest.run_id)

        self._metrics: Dict[str, Any] = {}
        self._params: Dict[str, Any] = {}
        self._artifacts: Dict[str, Any] = {}

        self._finalized: bool = False

    # =====================================================
    # Logging
    # =====================================================

    def log_param(self, key: str, value: Any) -> None:
        self._assert_not_finalized()
        self._params[str(key)] = value

    def log_metric(self, key: str, value: Any) -> None:
        self._assert_not_finalized()
        self._metrics[str(key)] = value

    def log_artifact(self, name: str, metadata: Dict[str, Any]) -> None:
        self._assert_not_finalized()
        self._artifacts[str(name)] = dict(metadata)

    # =====================================================
    # Finalization
    # =====================================================

    def finalize(self) -> None:
        self._assert_not_finalized()

        payload = {
            "manifest": asdict(self._manifest),  # Safe dataclass serialization
            "params": dict(sorted(self._params.items())),
            "metrics": dict(sorted(self._metrics.items())),
            "artifacts": dict(sorted(self._artifacts.items())),
            "completed_at": datetime.utcnow().isoformat(),
        }

        self._storage.save_json(
            name="run",
            payload=payload,
            sort_keys=True,
        )

        self._finalized = True

    # =====================================================
    # Internal Guard
    # =====================================================

    def _assert_not_finalized(self) -> None:
        if self._finalized:
            raise RuntimeError("Run already finalized.")