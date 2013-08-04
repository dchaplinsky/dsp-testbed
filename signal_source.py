from itertools import count
from math import pi, sin

class AbstractSource(object):
    """Very simple Abstract Source of audio signal"""

    def __init__(self, filename=None):
        self._filename = filename
        self._channels = 1
        self._depth = 4
        self._rate = 44100

    def read(self):
        """
        Iterator that returns signal in following format
         [channel1_sampleX, 
          channel2_sampleX,...]

        """
        while True:
            yield [0.0] * self._channels


class DiracSource(AbstractSource):
    def __init__(self, channels=1, depth=4, rate=44110):
        """
        Dirac impulse (or Dirac delta function)
        https://en.wikipedia.org/wiki/Dirac_delta_function
        """
        super(DiracSource, self).__init__()
        self._channels = channels
        self._depth = depth
        self._rate = rate

    def read(self):
        yield [1.0] * self._channels
        while True:
            yield [0.0] * self._channels


class SineSource(AbstractSource):
    def __init__(self, freq, amp=1.0, phase=0.0, channels=1, depth=4, rate=44110):
        """
        Simple source of sine wave with adjustable frequency/amplitude/phase
        Straightforward implementation.
        For better ideas see http://www.rossbencina.com/code/sinusoids
        """
        super(SineSource, self).__init__()
        self._channels = channels
        self._depth = depth
        self._rate = rate
        self._freq = freq
        self._amp = amp
        self._phase = phase
        self._w = self._freq * 2 * pi / self._rate

    def read(self):
        for i in count():
            yield [sin(i * self._w + self._phase) * self._amp] * self._channels
