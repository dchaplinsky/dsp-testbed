from itertools import count
from math import pi, sin

class AbstractSource(object):
    """Very simple Abstract Source of audio signal"""

    def __init__(self, length=None):
        self.channels = 1
        self.depth = 4
        self.endless = length == None
        self.length = length
        self.rate = 44100

    def read(self):
        """
        Iterator that returns signal in following format
         [channel1_sampleX, 
          channel2_sampleX,...]

        """
        for i in count():
            if self.length is not None and i == self.length:
                break
            yield [0.0] * self.channels


class DiracSource(AbstractSource):
    def __init__(self, length=None, channels=1, depth=4, rate=44110):
        """
        Dirac impulse (or Dirac delta function)
        https://en.wikipedia.org/wiki/Dirac_delta_function
        """
        super(DiracSource, self).__init__(length)
        self.channels = channels
        self.depth = depth
        self.rate = rate

    def read(self):
        yield [1.0] * self.channels
        for i in count(1):
            if self.length is not None and i == self.length:
                break

            yield [0.0] * self.channels


class SineSource(AbstractSource):
    def __init__(self, freq, amp=1.0, phase=0.0, length=None, channels=1, depth=4, rate=44110):
        """
        Simple source of sine wave with adjustable frequency/amplitude/phase
        Straightforward implementation.
        For better ideas see http://www.rossbencina.com/code/sinusoids
        """
        super(SineSource, self).__init__(length)
        self.channels = channels
        self.depth = depth
        self.rate = rate
        self._freq = freq
        self._amp = amp
        self._phase = phase
        self._w = self._freq * 2 * pi / self.rate

    def read(self):
        for i in count():
            if self.length is not None and i == self.length:
                break
            yield [sin(i * self._w + self._phase) * self._amp] * self.channels

class CompoundSineSource(AbstractSource):
    def __init__(self, bands, normalize=True, length=None, channels=1, depth=4, rate=44110):
        """
        Compound sine wave with adjustable frequency/amplitude/phase for each 
        band. Also can normalize amplitudes for bands to ensure that resulting
        sum will be strictly 1.0 or below
        Straightforward implementation.
        """
        super(CompoundSineSource, self).__init__(length)
        self.channels = channels
        self.depth = depth
        self.rate = rate

        self._freq = []
        self._amp = []
        self._phase = []
        self._w = []
        self._bands = len(bands)

        for band in bands:
            self._freq.append(band["freq"])
            self._amp.append(band.get("amp", 1.0))
            self._phase.append(band.get("phase", 0.0))
            self._w.append(self._freq[-1] * 2 * pi / self.rate)

        if normalize:
            amps = float(sum(self._amp))
            if amps > 1 and amps != 0:
                self._amp = [a / amps for a in self._amp]

    def read(self):
        for i in count():
            if self.length is not None and i == self.length:
                break
            
            res = sum(sin(i * self._w[b] + self._phase[b]) * self._amp[b]
                    for b in xrange(self._bands))

            yield [res] * self.channels
