from __future__ import annotations
from typing import Iterable
from baya.context import Context
from .base_plugin import BasePlugin


def load_plugins(
    context: Context,
    plugins: Iterable[BasePlugin],
) -> None:
    """
    Explicit plugin loading.
    No dynamic module scanning.
    """

    for plugin in plugins:
        context.plugins.register(plugin)
        plugin.setup(context)