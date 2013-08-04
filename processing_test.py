from plugins import LowPassFilter, RMS
from stacks import Stack
from aiff_reader import AiffReader
import pylab
from pylab_tools import ProbeResultsPlotter
import wave
from struct import pack


def pack_to_int(f, bytes):
	"""
	Very simple downsampling to fixed point.
	"""
	return pack('i', int(f * (2 ** (bytes * 8 - 1) - 1)))[:bytes]


r = AiffReader("samples/demo1_stereo.aif")

s = Stack([
		(LowPassFilter(samplerate=r._rate, channels=r._channels), "output"),
		(RMS(samplerate=r._rate, channels=r._channels), "rms"),
	]
)

out = s.process_source(r)
ProbeResultsPlotter(s.probe_results, figure_name=1)
pylab.show()


wf = wave.open("out.wav", 'wb')
wf.setnchannels(r._channels)
wf.setsampwidth(r._depth)
wf.setframerate(r._rate)
wf.writeframes("".join(map(lambda x: "".join(map(lambda y: pack_to_int(y, r._depth), x)), out)))
wf.close()
