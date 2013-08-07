import unittest
from itertools import islice
from copy import deepcopy
from dsptestbed.stacks import Stack
from dsptestbed.signal_source import SineSource
from dsptestbed.plugins import LowPassFilter, RMS

class StackTest(unittest.TestCase):
    def test_validation(self):
        self.assertRaises(Exception, Stack, [[]])
        self.assertRaises(Exception, Stack, [{}])
        self.assertRaises(Exception, Stack, [range(3)])

    def test_init(self):
        r1 = SineSource(freq=1000, channels=2)
        r2 = SineSource(freq=1000, channels=2)

        s1 = Stack([
                LowPassFilter(samplerate=r1.rate, channels=r1.channels),
                [RMS(samplerate=r1.rate, channels=r1.channels)],
            ])

        s2 = Stack([
                (LowPassFilter(samplerate=r2.rate, channels=r2.channels), "output"),
                [RMS(samplerate=r2.rate, channels=r2.channels), ("rms", "output")],
            ]
        )

        self.assertEqual(s1.process_source(r1, 1000), s2.process_source(r2, 1000))

    def test_sources(self):
        samples = 100
        r1 = SineSource(freq=1000, channels=2)
        r2 = SineSource(freq=1000, channels=2)

        s1 = Stack([
                (LowPassFilter(samplerate=r2.rate, channels=r2.channels), "output"),
                [RMS(samplerate=r2.rate, channels=r2.channels), ("rms", "output")],
            ]
        )

        s2 = Stack([
                (LowPassFilter(samplerate=r2.rate, channels=r2.channels), "output"),
                [RMS(samplerate=r2.rate, channels=r2.channels), ("rms", "output")],
            ]
        )

        s3 = Stack([
                [RMS(samplerate=r2.rate, channels=r2.channels), ("rms", "output")],
                (LowPassFilter(samplerate=r2.rate, channels=r2.channels), "output"),
            ]
        )

        chunk = list(islice(r1.read(), 0, samples))

        out1 = s1.process(chunk)
        out2 = s2.process_source(r2, samples)
        out3 = s3.process(chunk)

        self.assertEqual(out1, out2)
        self.assertEqual(out1, out3)
        self.assertEqual(out1, s2.probe_results["0_output"])
        self.assertEqual(out1, s2.probe_results["1_output"])
        self.assertEqual(chunk, s1.probe_results["input"])
