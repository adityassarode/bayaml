"""
Centralized exception hierarchy for Baya.
"""

from .core import BayaError
from .pipeline import PipelineError
from .config import ConfigError
from .plugin import PluginError

__all__ = [
    "BayaError",
    "PipelineError",
    "ConfigError",
    "PluginError",
]