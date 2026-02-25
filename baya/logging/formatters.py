from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any, Dict


class StructuredFormatter(logging.Formatter):
    """
    Deterministic structured log formatter.

    Output format:
    2026-02-25T10:12:33Z | INFO | module | message | key=value...
    """

    def format(self, record: logging.LogRecord) -> str:
        timestamp = datetime.fromtimestamp(
            record.created, tz=timezone.utc
        ).isoformat()

        base = f"{timestamp} | {record.levelname} | {record.name} | {record.getMessage()}"

        extra = self._extract_extra(record)
        if extra:
            extras = " ".join(f"{k}={v}" for k, v in sorted(extra.items()))
            base += f" | {extras}"

        return base

    def _extract_extra(self, record: logging.LogRecord) -> Dict[str, Any]:
        reserved = vars(logging.LogRecord("", 0, "", 0, "", (), None)).keys()
        return {
            k: v for k, v in record.__dict__.items()
            if k not in reserved and not k.startswith("_")
        }