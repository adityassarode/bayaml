from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any
import json
from pathlib import Path
import tempfile
import os


@dataclass(frozen=True)
class RunManifest:
    """
    Immutable run reproducibility manifest.
    """

    run_id: str
    timestamp: str

    dataset_hash: str
    code_hash: str
    config_hash: str

    environment: Dict[str, Any]
    config: Dict[str, Any]

    seed: int
    framework_version: str

    # =====================================================
    # Persistence
    # =====================================================

    def save(self, path: Path) -> None:
        """
        Atomic save to prevent corruption.
        """

        payload = json.dumps(
            asdict(self),
            indent=2,
            sort_keys=True,
        )

        path.parent.mkdir(parents=True, exist_ok=True)

        with tempfile.NamedTemporaryFile(
            mode="w",
            delete=False,
            dir=path.parent,
            encoding="utf-8",
        ) as tmp:
            tmp.write(payload)
            temp_name = tmp.name

        os.replace(temp_name, path)

    # =====================================================
    # Load
    # =====================================================

    @staticmethod
    def load(path: Path) -> "RunManifest":
        if not path.exists():
            raise FileNotFoundError(f"Run manifest not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))

        required_keys = {
            "run_id",
            "timestamp",
            "dataset_hash",
            "code_hash",
            "config_hash",
            "environment",
            "config",
            "seed",
            "framework_version",
        }

        missing = required_keys - data.keys()
        if missing:
            raise ValueError(
                f"RunManifest missing required fields: {missing}"
            )

        return RunManifest(**data)

    # =====================================================
    # Factory
    # =====================================================

    @staticmethod
    def new(
        *,
        run_id: str,
        dataset_hash: str,
        code_hash: str,
        config_hash: str,
        environment: Dict[str, Any],
        config: Dict[str, Any],
        seed: int,
        framework_version: str,
    ) -> "RunManifest":

        timestamp = (
            datetime.utcnow()
            .replace(microsecond=0)
            .isoformat() + "Z"
        )

        return RunManifest(
            run_id=run_id,
            timestamp=timestamp,
            dataset_hash=dataset_hash,
            code_hash=code_hash,
            config_hash=config_hash,
            environment=environment,
            config=config,
            seed=seed,
            framework_version=framework_version,
        )