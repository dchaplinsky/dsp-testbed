from plugins import LowPassFilter, RMS
from stacks import Stack
from aiff_reader import AiffReader
from signal_source import DiracSource, SineSource, CompoundSineSource
import pylab
from pylab_tools import ProbeResultsPlotter
import wave
from struct import pack

import math

def pack_to_int(f, bytes):
	"""
	Very simple downsampling to fixed point.
	"""
	return pack('i', int(f * (2 ** (bytes * 8 - 1) - 1)))[:bytes]


if __name__ == "__main__":
	r = AiffReader("samples/demo1_stereo.aif")
	# r = SineSource(channels=2, freq=100, amp=0.5, phase=math.pi / 2, length=1000)
	# r = DiracSource(channels = 1, length=1000)
	# r = SineSource(freq=1000, channels=2, length=1000)
	# r = CompoundSineSource([dict(freq=1000, amp=0.5), dict(freq=100, amp=2)], channels=2, length=1000)

	s = Stack([
			(LowPassFilter(samplerate=r.rate, channels=r.channels), "output"),
			(RMS(samplerate=r.rate, channels=r.channels), "rms"),
		]
	)

	out = s.process_source(r)
	ProbeResultsPlotter(s.probe_results, figure_name=1)
	pylab.show()

	wf = wave.open("out.wav", 'wb')
	wf.setnchannels(r.channels)
	wf.setsampwidth(r.depth)
	wf.setframerate(r.rate)
	wf.writeframes("".join(map(lambda x: "".join(map(lambda y: pack_to_int(y, r.depth), x)), out)))
	wf.close()
