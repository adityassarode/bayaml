from __future__ import annotations
from .core import BayaError


class PluginError(BayaError):
    """General plugin failure."""


class PluginRegistrationError(PluginError):
    """Plugin registration conflict."""


class PluginSetupError(PluginError):
    """Plugin setup lifecycle failure."""