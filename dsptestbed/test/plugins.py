import unittest
from dsptestbed.plugins import Plugin, LowPassFilter, RMS
from itertools import islice
from signal_source import DiracSource, SineSource
from operator import itemgetter
from random import random
from math import sqrt

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


class LowPassFilterTest(unittest.TestCase):
    def setUp(self):
        self.p1 = LowPassFilter()
        self.s1 = DiracSource()

        self.p2 = LowPassFilter()
        self.s2 = SineSource(freq=400, amp=1.0)

        self.p3 = LowPassFilter()
        self.s3 = SineSource(freq=40, amp=1.0)

    def test_on_dirac(self):
        chunk = list(islice(self.s1.read(), 0, 100))
        proc = self.p1.process(chunk)
        # Lets check if IIR filter is really infinite.
        self.assertTrue(abs(proc[-1][0]) > 0.001)

    def test_on_sin(self):
        # A bit weird way to check if LP filter passing low frequences
        # Freq for filter is 150 Hz, so:
        # 400 Hz freq should be dimmed
        chunk_len = self.s2.rate / 400
        chunk = list(islice(self.s2.read(), 0, chunk_len * 2))
        proc = self.p2.process(chunk)
        self.assertTrue(max(map(lambda x: abs(x[0]), proc)) < 0.3)

        # 40 Hz should be pretty much left intact
        chunk_len = self.s2.rate / 40
        chunk = list(islice(self.s3.read(), 0, chunk_len * 2))
        proc = self.p3.process(chunk)
        self.assertTrue(max(map(lambda x: abs(x[0]), proc)) > 0.8)


class RMSTest(unittest.TestCase):
    def setUp(self):
        self.p = RMS()
        self.s = SineSource(freq=1000, amp=0.5)

    def test_on_sin(self):
        chunk_len = 100 * self.s.rate / self.s._freq

        chunk = list(islice(self.s.read(), 0, chunk_len))
        self.p.process(chunk)

        # RMS for sine is Amplitude / sqrt(2)
        self.assertAlmostEqual(self.p.get_state()["rms"][0], self.s._amp / sqrt(2.0), 3)