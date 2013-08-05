from plugins import Plugin
from itertools import izip
from signal_source import AbstractSource
from utils import DefaultOrderedDict

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
        self._input = []
        self._clean_probe_results()

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
        if isinstance(probe, basestring):
            probe = [probe]

        self._probes.append(probe)

    def _clean_probe_results(self):
        self.probe_results = DefaultOrderedDict(list)

    def process(self, channels):
        self._input = channels
        for plugin in self._plugins:
            channels = plugin.process(channels)

        self.probe()
        return channels

    def process_source(self, source, limit=None):
        output = []
        self._clean_probe_results()

        for i, sample in enumerate(source.read()):
            if i == limit:
                break

            output += self.process([sample])

        return output

    def probe(self):
        probe_results = {}
        probe_results["input"] = self._input
        self.probe_results["input"] += self._input

        for i, plugin, probe_request in izip(xrange(len(self._plugins)), 
                                             self._plugins, self._probes):
            for probe in probe_request:
                data = plugin.get_state()
                probe_name = "%s_%s" % (i, probe)

                if probe in data:
                    probe_results[probe_name] = data[probe]

                    if probe == "output":
                        self.probe_results[probe_name] += data[probe]
                    else:
                        self.probe_results[probe_name].append(data[probe])

        return probe_results