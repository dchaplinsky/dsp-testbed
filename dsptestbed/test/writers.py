import unittest
from dsptestbed.writers import AiffWriter, WaveWriter, MatWriter
from dsptestbed.readers import AiffReader, WaveReader
from tempfile import gettempdir
from os import path, unlink
from dsptestbed.signal_source import SineSource
from math import pi
from struct import unpack

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


class MatWriterTest(unittest.TestCase):
    def test_write(self):
        source = SineSource(channels=2, freq=441, 
                            amp=0.5, phase=pi / 2, length=44100)

        data = list(source.read())

        fname = path.join(gettempdir(), "test.mat")
        w = MatWriter(fname)

        w.write(data)
        w.close()

        # Comprehensive testing using scipy loadmat routine
        try:
            from scipy.io import loadmat
            f = loadmat(fname)
            self.assertTrue("signal" in f)
            self.assertEqual(f["signal"].shape, (len(data), 2))
            self.assertEqual(tuple(f["signal"][0]), (0.5, 0.5))
        except ImportError:
            print("No scipy found :(")
            pass

        # Less comprehensive testing for scipy-poor systems (like pypy)

        # File size
        self.assertEqual(path.getsize(fname), 
                128 +               # Header
                8 + 16 + 16 + 16 +  # Array tag, array flags, dimensions, name
                8 +                 # Data tag
                len(data) * 2 * 8   # Data size
        )

        with open(fname, "rb") as f:
            f.seek(128 + 8 + 16 + 16 + 16 + 8)
            s = f.read(8)
            self.assertEqual(unpack("<d", s)[0], 0.5)

            f.seek((len(data) - 1) * 8)
            self.assertEqual(unpack("<d", s)[0], 0.5)

        unlink(fname)
