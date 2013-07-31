from plugins import BeatDetector, RMS
from aiff_reader import AiffReader
import pylab  # matplotlib
import wave
from struct import pack


def pack_to_32(f):
    return pack('i', int(f * (2 ** 31 - 1)))


r = AiffReader("samples/demo1.aif")
it = r.read()

x_list = []
y_list = []
yp_list = []
rms_list = []

bd = BeatDetector(r._rate)
rms = RMS(r._rate)

for i in range(30000):
    sample = it.next()

    x_list.append(i)
    y_list.append(sample[0])
    yp_list += bd.process([[sample[0]]])[0]
    rms.process([[yp_list[-1]]])

    rms_list.append(rms.get_state()["rms"])

pylab.subplot(211)
pylab.plot(x_list, y_list, 'b')

pylab.subplot(212)
pylab.plot(x_list, yp_list, 'g')
pylab.plot(x_list, rms_list, 'r')
pylab.show()

wf = wave.open("out.wav", 'wb')
wf.setnchannels(r._channels)
wf.setsampwidth(r._depth)
wf.setframerate(r._rate)
wf.writeframes("".join(map(pack_to_32, yp_list)))
wf.close()
