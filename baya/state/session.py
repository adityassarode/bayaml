from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Dict, Any
import uuid


@dataclass(frozen=True, slots=True)
class RunSession:
    """
    Immutable execution identity.

    Created at pipeline start.
    Passed through Context → Tracking → Reproducibility → Orchestration
    """

    run_id: str
    created_at: datetime
    seed: int
    config_hash: str
    dataset_hash: str

    metadata: Dict[str, Any] = field(default_factory=dict)

    # -----------------------------

    @staticmethod
    def create(
        *,
        seed: int,
        config_hash: str,
        dataset_hash: str,
    ) -> "RunSession":
        """
        Deterministically create new session.
        """

        return RunSession(
            run_id=str(uuid.uuid4()),
            created_at=datetime.now(timezone.utc),
            seed=seed,
            config_hash=config_hash,
            dataset_hash=dataset_hash,
        )