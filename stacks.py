from plugins import Plugin
from itertools import izip


class Stack(object):
    """
    Stub for plugins stack.
    Will allow to chain plugins and get the inner state
    from all of them using tool called probe.
    """
    def __init__(self, plugins_and_probes):
        super(Stack, self).__init__()
        self._plugins = []
        self._probes = []

        for item in plugins_and_probes:
            if isinstance(item, Plugin):
                self._add_plugin_and_probe(item, [])
            elif isinstance(item, (tuple, list)):
                if len(item) > 1:
                    self._add_plugin_and_probe(item[0], item[1])
                elif len(item) == 1:
                    self._add_plugin_and_probe(item, [])
                else:
                    raise Exception("Wrong plugin entry")
            else:
                raise Exception("Wrong plugin entry")

    def _add_plugin_and_probe(self, plugin, probe):
        self._plugins.append(plugin)
        self._probes(probe)

    def process(self, channels):
        for plugin in self._plugins:
            channels = plugin.process(channels)

        return channels

    def probe(self):
        for plugin, probe in izip(self._plugins, self._probes):
            pass
