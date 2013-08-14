import unittest
from dsptestbed.writers import AiffWriter, WaveWriter
from dsptestbed.readers import AiffReader, WaveReader
from tempfile import gettempdir
from os import path, unlink
from dsptestbed.signal_source import SineSource
from math import pi

class AiffWriterTest(unittest.TestCase):
    r = AiffReader
    w = AiffWriter

    def test_write(self):
        source = SineSource(channels=2, freq=441, amp=0.5, phase=pi / 2, length=44100)
        data = list(source.read())

        for f in xrange(1, 5):
            fname = path.join(gettempdir(), "%s" % f)

            w = self.w(fname, channels=source.channels,
                           rate=source.rate,
                           depth=f)

            w.write(data)
            w.close()

            r = self.r(fname)

            self.assertEqual(r.rate, 44100)
            self.assertEqual(r.channels, 2)
            self.assertEqual(r.depth, f)

            chunk = list(r.read())
            self.assertEqual(chunk[0], [0.5, 0.5])
            self.assertEqual(chunk[25], [0.0, 0.0])
            self.assertEqual(chunk[50], [-0.5, -0.5])

            unlink(fname)

class WaveWriterTest(AiffWriterTest):
    r = WaveReader
    w = WaveWriter
