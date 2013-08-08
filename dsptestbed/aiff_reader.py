import aifc
import struct
from signal_source import AbstractSource

class AiffReader(AbstractSource):    
    def __init__(self, filename):
        super(AiffReader, self).__init__()
        self.endless = False
        self._filename = filename
        self._reader = aifc.open(filename, "rb")
        self.channels, self.depth, self.rate, _, _, _ = self._reader.getparams()

    def read(self):
        bits = self.depth * 8
        denominator = float(2 ** (bits - 1))

        while True:
            frames = self._reader.readframes(8192)

            if not frames:
                break

            while frames:
                frame, frames = frames[:self.depth * self.channels], frames[self.depth * self.channels:]
                output = []

                for c in range(self.channels):
                    chunk = frame[c * self.depth:(c + 1) * self.depth]

                    pad_char = ('\0' if chunk[0] < '\x80' else '\xff')
                    sample = struct.unpack('>i', pad_char * (4 - self.depth) + chunk)[0]

                    output.append(sample / denominator)

                yield output

if __name__ == "__main__": # pragma: no cover
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
