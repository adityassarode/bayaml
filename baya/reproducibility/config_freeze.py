from __future__ import annotations

import json
import hashlib
from typing import Dict, Any


def freeze_config(config: Dict[str, Any]) -> Dict[str, Any]:
    serialized = json.dumps(config, sort_keys=True, separators=(",", ":"))
    return {
        "config": json.loads(serialized),
        "config_hash": hashlib.sha256(serialized.encode()).hexdigest(),
    }