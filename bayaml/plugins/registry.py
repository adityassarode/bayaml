class PluginRegistry:
    _plugins = {}

    @classmethod
    def register(cls, plugin) -> None:
        cls._plugins[plugin.name] = plugin

    @classmethod
    def list_plugins(cls):
        return sorted(cls._plugins)
