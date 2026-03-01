from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict
import uuid


@dataclass(frozen=True)
class RunSession:
    run_id: str
    created_at: datetime
    seed: int
    metadata: Dict[str, Any] = field(default_factory=dict)

    @staticmethod
    def create(seed: int) -> "RunSession":
        return RunSession(run_id=str(uuid.uuid4()), created_at=datetime.utcnow(), seed=seed)
