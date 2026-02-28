from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RunManifest:
    run_id: str
    dataset_hash: str
    config_hash: str
