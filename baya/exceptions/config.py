from __future__ import annotations
from .core import BayaError


class ConfigError(BayaError):
    """Invalid configuration detected."""


class MissingConfigField(ConfigError):
    """Required config field missing."""


class InvalidConfigValue(ConfigError):
    """Invalid config value."""