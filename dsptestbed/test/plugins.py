import unittest
from dsptestbed.plugins import Plugin, LowPassFilter
from operator import itemgetter
from random import random

class PluginTest(unittest.TestCase):
    def setUp(self):
        self.p = Plugin(samplerate=48000, channels=3, params={"foo": "bar"})

    def test_params(self):
        self.assertEqual(self.p._samplerate, 48000)
        self.assertEqual(self.p._channels, 3)
        self.assertEqual(self.p._params["foo"], "bar")

    def test_process(self):
        out = self.p.process(map(lambda x: [x / 100.] * 3, xrange(100)))
        self.assertEqual(len(out), 100)
        self.assertEqual(len(out[0]), 3)

        for x in xrange(3):
            self.assertEqual(sum(map(itemgetter(x), out)), 49.5)

    def test_state(self):
        inp = [[random() - 0.5 for c in xrange(3)] for x in xrange(10)]

        out = self.p.process(inp)
        self.assertEqual(inp, out)
        self.assertEqual(inp, self.p.get_state()["output"])