from plugins import LowPassFilter, RMS
from aiff_reader import AiffReader
import pylab
from pylab_tools import ProbeResultsPlotter
import wave
from struct import pack
from time import time


def pack_to_int(f, bytes):
	"""
	Very simple downsampling to fixed point.
	"""
	return pack('i', int(f * (2 ** (bytes * 8 - 1) - 1)))[:bytes]


r = AiffReader("samples/demo1_stereo.aif")
it = r.read()

x_list = []
y_list = []
yp_list = []
rms_list = []

lp = LowPassFilter(samplerate=r._rate, channels=r._channels)
rms = RMS(samplerate=r._rate, channels=r._channels)

for sample in it:
    # sample = it.next()

    y_list.append(sample)
    yp_list.append(lp.process([sample])[0])
    rms.process([yp_list[-1]])

    rms_list.append(rms.get_state()["rms"])

ProbeResultsPlotter({
	"Source": y_list,
	"Proc": yp_list,
	"RMS": rms_list,
	}, figure_name=1)

pylab.show()

wf = wave.open("out.wav", 'wb')
wf.setnchannels(r._channels)
wf.setsampwidth(r._depth)
wf.setframerate(r._rate)
wf.writeframes("".join(map(lambda x: "".join(map(lambda y: pack_to_int(y, r._depth), x)), yp_list)))
wf.close()
