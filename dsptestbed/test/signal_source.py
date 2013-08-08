import unittest
from math import pi
from itertools import islice
from dsptestbed.signal_source import (AbstractSource, DiracSource, SineSource,
    CompoundSineSource)


class AbstractSourceTest(unittest.TestCase):
    def setUp(self):
        self.s = AbstractSource()
        self.s1 = AbstractSource(length=100)

    def test_params(self):
        self.assertEqual(self.s.channels, 1)
        self.assertEqual(self.s.rate, 44100)
        self.assertEqual(self.s.depth, 4)
        self.assertTrue(self.s.endless)
        self.assertTrue(not self.s1.endless)

    def test_read(self):
        for i, x in enumerate(self.s.read()):
            self.assertEqual(x, [0.0])
            if i > 100:
                break

        chunk = list(self.s1.read())
        self.assertEqual(chunk, [[0.0]] * 100)


class DiracSourceTest(unittest.TestCase):
    def setUp(self):
        self.s = DiracSource(channels=3)
        self.s1 = DiracSource(channels=3, length=1)

    def test_params(self):
        self.assertEqual(self.s.channels, 3)
        self.assertTrue(self.s.endless)

    def test_one_sample(self):
        chunk = list(self.s1.read())
        self.assertEqual(chunk, [[1.0, 1.0, 1.0]])

    def test_read(self):
        for i, x in enumerate(self.s.read()):
            if i == 0:
                self.assertEqual(x, [1.0, 1.0, 1.0])
            else:
                self.assertEqual(x, [0.0, 0.0, 0.0])

            if i > 100:
                break

class SineSourceTest(unittest.TestCase):
    def setUp(self):
        self.s = SineSource(channels=2, freq=1, amp=0.5, phase=pi / 2)
        self.s2 = SineSource(channels=2, freq=1, amp=0.5, phase=pi / 2, length=self.s.rate)

    def test_params(self):
        self.assertEqual(self.s.channels, 2)
        self.assertTrue(self.s.endless)

    def test_read(self):
        second = list(islice(self.s.read(), 0, self.s.rate))
        
        self.assertAlmostEqual(second[0][0], 0.5)
        self.assertAlmostEqual(second[0][1], 0.5)
        self.assertAlmostEqual(second[-1][0], 0.5)
        self.assertAlmostEqual(second[-1][1], 0.5)

        self.assertAlmostEqual(second[int(self.s.rate / 2)][0], -0.5)
        self.assertAlmostEqual(second[int(self.s.rate / 2)][1], -0.5)

        self.assertAlmostEqual(second[int(self.s.rate / 4)][0], 0.0, 4)
        self.assertAlmostEqual(second[int(self.s.rate / 4)][1], 0.0, 4)

        self.assertTrue(second[int(self.s.rate / 4 - 1)][0] > 0.0)
        self.assertTrue(second[int(self.s.rate / 4 - 1)][1] > 0.0)

        self.assertTrue(second[int(self.s.rate / 4 + 1)][0] < 0.0)
        self.assertTrue(second[int(self.s.rate / 4 + 1)][1] < 0.0)

        self.assertEqual(second, list(self.s2.read()))


class CompoundSineSourceTest(unittest.TestCase):
    def setUp(self):
        self.s1 = CompoundSineSource([dict(freq=4, amp=0.5, phase = 3 * pi / 2),
                                          dict(freq=1, amp=2, phase = 3 * pi / 2)])

        self.s2 = CompoundSineSource([dict(freq=4, amp=0.5, phase = 3 * pi / 2), 
                                          dict(freq=1, amp=2, phase = 3 * pi / 2)], 
                                          normalize=False, length=self.s1.rate)

    def test_read(self):
        second = list(islice(self.s1.read(), 0, self.s1.rate))
        self.assertAlmostEqual(second[0][0], -1.0)
        
        another_second = list(self.s2.read())
        self.assertAlmostEqual(another_second[0][0], -2.5)

        self.assertEqual(len(second), len(another_second))