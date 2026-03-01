from bayaml.plugins import BasePlugin, PluginRegistry, load_plugins


class DemoPlugin(BasePlugin):
    name = "demo"


def test_plugin_registry():
    PluginRegistry.register(DemoPlugin())
    assert "demo" in load_plugins()
