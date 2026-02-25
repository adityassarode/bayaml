from __future__ import annotations

import platform
import sys
from typing import Dict, List
from importlib import metadata


def capture_environment() -> Dict[str, object]:
    """
    Deterministic environment capture.

    Includes:
        - Python version
        - Python implementation
        - Platform
        - Installed packages (name==version)
    """

    return {
        "python_version": platform.python_version(),
        "python_implementation": platform.python_implementation(),
        "platform": platform.platform(),
        "packages": _installed_packages(),
    }


# =====================================================
# Package Capture (No subprocess)
# =====================================================

def _installed_packages() -> List[str]:
    """
    Deterministically list installed packages.
    Avoids subprocess and pip dependency.
    """

    packages: List[str] = []

    for dist in metadata.distributions():
        name = dist.metadata.get("Name")
        version = dist.version

        if name and version:
            packages.append(f"{name}=={version}")

    return sorted(packages)