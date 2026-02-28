from __future__ import annotations

import hashlib
import json


def freeze_config(config: dict) -> dict:
    raw = json.dumps(config, sort_keys=True)
    return {"config": config, "config_hash": hashlib.sha256(raw.encode("utf-8")).hexdigest()}
