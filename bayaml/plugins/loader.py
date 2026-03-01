from .registry import PluginRegistry


def load_plugins() -> list[str]:
    return PluginRegistry.list_plugins()
