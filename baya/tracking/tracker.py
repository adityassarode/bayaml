from __future__ import annotations

from typing import Dict, Any
from pathlib import Path
from datetime import datetime
from dataclasses import asdict
import json

from baya.reproducibility.run_manifest import RunManifest
from .storage import Storage


class Tracker:
    """
    Run lifecycle logger.

    Guarantees:
    - Deterministic JSON persistence
    - No post-finalization mutation
    - Atomic storage semantics
    - Manifest integrity preservation
    """

    def __init__(self, manifest: RunManifest, root: Path) -> None:
        self._manifest = manifest
        self._run_path = root / manifest.run_id

        if self._run_path.exists():
            raise RuntimeError(
                f"Run directory already exists: {self._run_path}"
            )

        self._storage = Storage(self._run_path)

        self._metrics: Dict[str, Any] = {}
        self._params: Dict[str, Any] = {}
        self._artifacts: Dict[str, Any] = {}

        self._finalized: bool = False

        # Auto-log manifest parameters deterministically
        self._params.update({
            "run_id": manifest.run_id,
            "dataset_hash": manifest.dataset_hash,
            "code_hash": manifest.code_hash,
            "config_hash": manifest.config_hash,
            "run_hash": manifest.run_hash,
            "seed": manifest.seed,
            "framework_version": manifest.framework_version,
            "schema_version": manifest.schema_version,
        })

    # =====================================================
    # Logging
    # =====================================================

    def log_param(self, key: str, value: Any) -> None:
        self._assert_not_finalized()
        self._ensure_serializable(value)
        self._params[str(key)] = value

    def log_metric(self, key: str, value: Any) -> None:
        self._assert_not_finalized()
        self._ensure_serializable(value)
        self._metrics[str(key)] = value

    def log_artifact(self, name: str, metadata: Dict[str, Any]) -> None:
        self._assert_not_finalized()
        self._ensure_serializable(metadata)
        self._artifacts[str(name)] = dict(metadata)

    # =====================================================
    # Finalization
    # =====================================================

    def finalize(self) -> None:
        self._assert_not_finalized()

        completed_at = (
            datetime.utcnow()
            .replace(microsecond=0)
            .isoformat() + "Z"
        )

        payload = {
            "manifest": asdict(self._manifest),
            "params": dict(sorted(self._params.items())),
            "metrics": dict(sorted(self._metrics.items())),
            "artifacts": dict(sorted(self._artifacts.items())),
            "completed_at": completed_at,
        }

        # Validate full JSON serializability
        try:
            json.dumps(payload, sort_keys=True)
        except TypeError as e:
            raise ValueError(
                f"Non-serializable data in tracker payload: {e}"
            )

        self._storage.save_json(
            name="run",
            payload=payload,
            sort_keys=True,
        )

        self._finalized = True

    # =====================================================
    # Internal Guards
    # =====================================================

    def _assert_not_finalized(self) -> None:
        if self._finalized:
            raise RuntimeError("Run already finalized.")

    @staticmethod
    def _ensure_serializable(value: Any) -> None:
        try:
            json.dumps(value)
        except TypeError:
            raise ValueError(
                f"Value not JSON serializable: {type(value)}"
            )