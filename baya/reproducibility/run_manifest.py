from __future__ import annotations

from dataclasses import dataclass, asdict
from datetime import datetime
from typing import Dict, Any
import json
from pathlib import Path


@dataclass(frozen=True)
class RunManifest:
    run_id: str
    timestamp: str

    dataset_hash: str
    code_hash: str
    config_hash: str

    environment: Dict[str, Any]
    config: Dict[str, Any]

    seed: int

    # --------------------------

    def save(self, path: Path) -> None:
        path.write_text(json.dumps(asdict(self), indent=2, sort_keys=True))

    # --------------------------

    @staticmethod
    def load(path: Path) -> "RunManifest":
        data = json.loads(path.read_text())
        return RunManifest(**data)

    # --------------------------

    @staticmethod
    def new(
        run_id: str,
        dataset_hash: str,
        code_hash: str,
        config_hash: str,
        environment: Dict[str, Any],
        config: Dict[str, Any],
        seed: int,
    ) -> "RunManifest":
        return RunManifest(
            run_id=run_id,
            timestamp=datetime.utcnow().isoformat(),
            dataset_hash=dataset_hash,
            code_hash=code_hash,
            config_hash=config_hash,
            environment=environment,
            config=config,
            seed=seed,
        )