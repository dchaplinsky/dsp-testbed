class AbstractSource(object):
    """Very simple Abstract Source of audio signal"""

    def __init__(self, filename):
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
