import aifc
import wave
import struct
from signal_source import AbstractSource

class AbstractFileReader(AbstractSource):
    """
    To use it you should inherit it and replace readerclass and endian class fields
    """

    def __init__(self, filename):
        super(AbstractFileReader, self).__init__()
        self.endless = False
        self._filename = filename
        self._reader = self.reader_class.open(filename, "rb")
        self.channels, self.depth, self.rate, _, _, _ = self._reader.getparams()
        self.length = self._reader.getnframes()

    def read(self):
        bits = self.depth * 8
        denominator = float(2 ** (bits - 1))

        while True:
            frames = self._reader.readframes(8192)

            if not frames:
                break

            n = self.depth * self.channels
            for i in xrange(int(len(frames) / n)):
                frame = frames[i * n:(i + 1) * n]
                output = []

                for c in xrange(self.channels):
                    chunk = frame[c * self.depth:(c + 1) * self.depth]

                    if self.endian == "big":
                        pad_char = ('\0' if chunk[0] < '\x80' else '\xff')
                        sample = struct.unpack(">i", pad_char * (4 - self.depth) + chunk)[0]
                    else:
                        pad_char = ('\0' if chunk[-1] < '\x80' else '\xff')
                        sample = struct.unpack("i", chunk + pad_char * (4 - self.depth))[0]
                    
                    output.append(sample / denominator)

                yield output

class AiffReader(AbstractFileReader):
    reader_class = aifc
    endian = "big"


class WaveReader(AbstractFileReader):
    reader_class = wave
    endian = "small"


if __name__ == "__main__": # pragma: no cover
    import pylab  # matplotlib

    r = AiffReader("samples/demo1.aif")
    it = r.read()

    x_list = []
    y_list = []

    for i in range(30000):
        sample = it.next()

        x_list.append(i)
        y_list.append(sample[0])

    pylab.plot(x_list, y_list, 'b')
    pylab.show()
