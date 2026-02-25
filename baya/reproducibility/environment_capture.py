from __future__ import annotations

import platform
import sys
import subprocess
from typing import Dict


def capture_environment() -> Dict[str, object]:
    return {
        "python_version": sys.version,
        "platform": platform.platform(),
        "packages": _pip_freeze(),
    }


def _pip_freeze() -> list[str]:
    result = subprocess.run(
        [sys.executable, "-m", "pip", "freeze"],
        capture_output=True,
        text=True,
        check=True,
    )
    return sorted(result.stdout.splitlines())