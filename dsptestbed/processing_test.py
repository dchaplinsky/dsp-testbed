from plugins import LowPassFilter, RMS
from stacks import Stack
from readers import AiffReader, WaveReader
from signal_source import DiracSource, SineSource, CompoundSineSource
import pylab
from writers import WaveWriter, AiffWriter, MatWriter
from pylab_tools import ProbeResultsPlotter
import wave
import math

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

	w = AiffWriter("out.aif", r.channels, r.depth, r.rate)
	w.write(out[:20000])
	w.write(out[20000:])
	w.close()
