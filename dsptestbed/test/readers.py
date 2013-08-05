import os
import unittest
from itertools import islice
from dsptestbed.aiff_reader import AiffReader

class AiffReaderTest(unittest.TestCase):
    def setUp(self):
        self.s = {}

        for f in ["8bit", "16bit", "24bit", "32bit", "16bit_stereo"]:
            self.s[f] = AiffReader("../samples/tests/sin440_%s.aif" % f)
     

    def test_params(self):
        self.assertEqual(self.s["8bit"].depth, 1)
        self.assertEqual(self.s["8bit"].channels, 1)
        self.assertEqual(self.s["8bit"].rate, 44100)
        self.assertEqual(self.s["16bit"].depth, 2)
        self.assertEqual(self.s["16bit_stereo"].channels, 2)
        self.assertEqual(self.s["24bit"].depth, 3)
        self.assertEqual(self.s["32bit"].depth, 4)


    def test_data(self):
        for n, s in self.s.iteritems():
            chunk = list(s.read())
            quart_period = s.rate / (440 * 4)

            self.assertAlmostEqual(chunk[0][0], 0.0)

            precision = 1 if "8bit" in n else 3
            channel = 1 if "stereo" in n else 0

            self.assertAlmostEqual(chunk[quart_period][channel], 1.0, precision)
            self.assertAlmostEqual(chunk[3 * quart_period][channel], -1.0, precision)
