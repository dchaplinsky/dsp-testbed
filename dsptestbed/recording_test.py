#!/usr/bin/env python

import pyaudio
import wave
import math
from struct import unpack, pack


def record(output_filename):
    chunk = 128
    FORMAT = pyaudio.paInt32
    CHANNELS = 1
    RATE = 96000
    RECORD_SECONDS = 15

    FREQ_LP_BEAT = 150.0  # Low Pass filter frequency
    T_FILTER = 1.0 / (2.0 * math.pi * FREQ_LP_BEAT)  # Low Pass filter time constant
    BEAT_RTIME = 0.01  # Release time of enveloppe detector in second

    Filter1Out = 0.0
    Filter2Out = 0.0
    PeakEnv = 0.0
    BeatTrigger = False
    PrevBeatPulse = False
    num_beats = 0
    peak = 0.0

    KBeatFilter = 1.0 / (RATE * T_FILTER)
    BeatRelease = math.exp(-1.0 / (RATE * BEAT_RTIME))

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=3,
                    frames_per_buffer=chunk)

    print "* recording"
    all = []
    try:
        for i in range(0, RATE / chunk * RECORD_SECONDS):
            data = stream.read(chunk)

            float_data = []
            out_data = []
            for i in xrange(len(data) / 4):
                inp = unpack('i', data[i * 4:(i + 1) * 4])[0] / (2 ** 31 - 1.)

                Filter1Out = Filter1Out + (KBeatFilter * (inp - Filter1Out))
                Filter2Out = Filter2Out + (KBeatFilter * (Filter1Out - Filter2Out))

                out_data.append(pack('i', int(Filter2Out * (2 ** 31 - 1))))

                EnvIn = math.fabs(Filter2Out)

                if EnvIn > PeakEnv:
                    PeakEnv = EnvIn  # Attack time = 0
                else:
                    PeakEnv *= BeatRelease
                    PeakEnv += (1.0 - BeatRelease) * EnvIn

                if not BeatTrigger:
                    if PeakEnv > 0.02:
                        peak = PeakEnv
                        BeatTrigger = True
                else:
                    if PeakEnv < peak / 2.:
                        BeatTrigger = False
                        PrevBeatPulse = False

                BeatPulse = False

                if BeatTrigger and not PrevBeatPulse:
                    BeatPulse = True
                    print(num_beats)
                    num_beats += 1
                    PrevBeatPulse = BeatTrigger

            # all.append(data)
            all += out_data
    except KeyboardInterrupt:
        pass
    finally:
        print "* done recording"
        stream.stop_stream()
        stream.close()
        p.terminate()

        # write data to WAVE file
        data = ''.join(all)
        wf = wave.open(output_filename, 'wb')
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(data)
        wf.close()


def playback(output_filename):
    chunk = 1024

    PyAudio = pyaudio.PyAudio

    wf = wave.open(output_filename, 'rb')

    p = PyAudio()

    # open stream
    stream = p.open(format =
                    p.get_format_from_width(wf.getsampwidth()),
                    channels = wf.getnchannels(),
                    rate = wf.getframerate(),
                    output = True)

    # read data
    data = wf.readframes(chunk)

    # play stream
    while data != '':
        stream.write(data)
        data = wf.readframes(chunk)

    stream.stop_stream()
    stream.close()
    p.terminate()

if __name__ == "__main__":
    username = "foo"
#     username = raw_input("Please enter your name.\n")
#     raw_input("""I'll now record you saying your name.
# Hit enter when you are ready to begin,
# and then wait for the \"recording\" prompt to start.
# Use control-C to stop recording.
# Max recording time is 8 seconds.\n""")
    record(username + ".wav")
    # print "Thanks! Here's your file played back."
    # playback(username + ".wav")
