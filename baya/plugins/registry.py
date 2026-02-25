from __future__ import annotations
from typing import Dict
from .base_plugin import BasePlugin


class PluginRegistry:
    """
    Holds loaded plugin instances.
    Attached to Context.
    """

    def __init__(self) -> None:
        self._plugins: Dict[str, BasePlugin] = {}

    def register(self, plugin: BasePlugin) -> None:
        if plugin.name in self._plugins:
            raise RuntimeError(f"Plugin '{plugin.name}' already registered.")

        self._plugins[plugin.name] = plugin

    def get(self, name: str) -> BasePlugin:
        return self._plugins[name]

    def list(self) -> list[str]:
        return list(self._plugins.keys())