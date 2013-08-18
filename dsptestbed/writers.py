import aifc
import wave
from struct import pack
from sys import platform
from math import ceil
from datetime import datetime

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
            return pack('>i', 
                int(f * (2 ** (self.depth * 8 - 1))))[4 - self.depth:]
        else:
            return pack('i', 
                int(f * (2 ** (self.depth * 8 - 1))))[:self.depth]

    def write(self, frames):
        self._writer.writeframes("".join(map(
            lambda x: "".join(map(self.pack_to_int, x)), frames)))

    def close(self):
        self._writer.close()


class WaveWriter(AbstractWriter):
    reader_class = wave
    endian = "small"


class AiffWriter(AbstractWriter):
    reader_class = aifc
    endian = "big"

# Export to Matlab (TM) 5 .mat files, according to specs from here:
# http://www.mathworks.com/access/helpdesk/help/pdf_doc/matlab/matfile_format.pdf

miINT8 = 1
miUINT8 = 2
miUINT16 = 4
miINT32 = 5
miUINT32 = 6
miSINGLE = 7
miDOUBLE = 9
miMATRIX = 14
mxDOUBLE_CLASS = 6


class MatWriter(object):
    default_header = "MATLAB 5.0 MAT-file, Platform: %s, " \
        "Created with DSP test bed on: %s" % \
        (platform, datetime.now().strftime("%c"))

    def __init__(self, filename, var_name="signal"):
        self._data = []
        self.filename = filename
        self.var_name = var_name
        self._f = open(self.filename, "wb")

    def write(self, frames):
        """
        Caveat:
        Unlike Aiff and Wave writers for Matlab export
        we need to know the size of the output data beforehand
        That's it, write method actually doesn't write but
        accumulate data until close method call. So be careful
        """
        self._data += frames

    def close(self):
        samples = len(self._data)
        channels = len(self._data[0])
        data_length = 8 * samples * channels

        # Header
        self._f.write(pack("116s", self.default_header)) # Descriptive text
        self._f.write(pack("8s", "")) # subsys data offset
        self._f.write(pack("<h", 0x0100)) # version
        self._f.write(pack("2s", "IM")) # endian indicator (little endian)

        var_name_length = int(ceil(len(self.var_name) / 8.) * 8)

        self._f.write(pack("<l", miMATRIX)) # Data type
        self._f.write(pack("<l", 48 + var_name_length + data_length)) # Number of bytes

        self._f.write(pack("<l", miUINT32)) # Array flags
        self._f.write(pack("<l", 8))
        self._f.write(pack("<l", mxDOUBLE_CLASS)) # No flags + type is set to double
        self._f.write(pack("<l", 0))

        self._f.write(pack("<l", miINT32)) # Array dimensions
        self._f.write(pack("<l", 8))
        self._f.write(pack("<l", samples)) # Samples
        self._f.write(pack("<l", channels)) # Channels

        self._f.write(pack("<l", miINT8)) # Array name
        self._f.write(pack("<l", len(self.var_name)))
        self._f.write(pack("%ds" % var_name_length, self.var_name))

        self._f.write(pack("<l", miDOUBLE)) # Data type
        self._f.write(pack("<l", data_length)) # Number of bytes

        # Data
        for channel in xrange(channels):
            for sample in self._data:
                self._f.write(pack("<d", sample[channel])) 

        self._f.close()