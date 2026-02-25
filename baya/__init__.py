"""
Baya - Structured ML Orchestration Framework

Public API exposure layer.
"""

from __future__ import annotations

from .version import __version__
from .project import Project

__all__ = [
    "Project",
    "__version__",
]

__author__ = "Aditya Sarode"
__license__ = "MIT"
