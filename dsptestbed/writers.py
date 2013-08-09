import aifc
import wave
from struct import pack

class AbstractWriter(object):
    def __init__(self, filename, channels, depth, rate):
        self.channels = channels
        self.depth = depth
        self.rate = rate
        self.filename = filename
        self._writer = self.reader_class.open(filename, "wb")
        self._writer.setnchannels(channels)
        self._writer.setsampwidth(depth)
        self._writer.setframerate(rate)

    def pack_to_int(self, f):
        """
        Very simple downsampling to fixed point.
        """
        if self.endian == "big":
            return pack('>i', int(f * (2 ** (self.depth * 8 - 1))))[4 - self.depth:]
        else:
            return pack('i', int(f * (2 ** (self.depth * 8 - 1))))[:self.depth]

    def write(self, frames):
        self._writer.writeframes("".join(map(lambda x: "".join(map(self.pack_to_int, x)), frames)))

    def close(self):
        self._writer.close()


class WaveWriter(AbstractWriter):
    reader_class = wave
    endian = "small"

class AiffWriter(AbstractWriter):
    reader_class = aifc
    endian = "big"
