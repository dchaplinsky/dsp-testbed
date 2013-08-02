import aifc
import struct
from signal_source import AbstractSource

class AiffReader(AbstractSource):
    def __init__(self, filename):
        super(AiffReader, self).__init__(filename)

        self._reader = aifc.open(filename, "rb")
        self._channels, self._depth, self._rate, _, _, _ = self._reader.getparams()

    def read(self):
        bits = self._depth * 8
        denominator = 2 ** (bits - 1) - 1.0

        while True:
            frames = self._reader.readframes(8192)

            if not frames:
                break

            while frames:
                frame, frames = frames[:self._depth * self._channels], frames[self._depth * self._channels:]
                output = []

                for c in range(self._channels):
                    chunk = frame[c * self._depth:(c + 1) * self._depth]

                    pad_char = ('\0' if chunk[0] < '\x80' else '\xff')
                    sample = struct.unpack('>i', pad_char * (4 - self._depth) + chunk)[0]

                    output.append(sample / denominator)

                yield output

if __name__ == "__main__":
    import pylab  # matplotlib

    r = AiffReader("demo1.aif")
    it = r.read()

    x_list = []
    y_list = []

    for i in range(30000):
        sample = it.next()

        x_list.append(i)
        y_list.append(sample[0])

    pylab.plot(x_list, y_list, 'b')
    pylab.show()
