"""
Scipy backend registration.

Importing this module does NOT auto register backend.
Registration must be done by integration loader/plugin system.
"""

from .scipy_backend import ScipyBackend

__all__ = ["ScipyBackend"]