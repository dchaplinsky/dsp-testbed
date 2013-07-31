import math
from copy import deepcopy


class Plugin(object):
    """Abstract plugin for audio processing and analysis"""
    _default_params = {}

    def __init__(self, samplerate, params={}):
        super(Plugin, self).__init__()
        self._samplerate = samplerate
        self._params = deepcopy(self._default_params)
        self._params.update(params)

    def process(self, channels):
        """
        Pass data in form 
        [[channel1_sample1, channel1_sample2...], 
         [channel2_sample1, channel2_sample2...], ...]

        Beware, most of plugins is strictly mono right now
        """
        out = []
        for i, channel in enumerate(channels):
            out.append([self._process_sample(sample, i) for sample in channel])

        return out

    def get_state(self):
        """
        Feturns dict with the inner state of plugin.
        Useful for measurments (like RMS plugin) or debugging.
        """
        return {}

    def _process_sample(self, sample, channel_number):
        return sample


class BeatDetector(Plugin):
    """BeatDetector plugin. Strictly mono atm"""
    _default_params = {
        "lowpass_frequency": 150.0,  # Herts
        "beat_release_time": 0.01,  # seconds
    }

    def __init__(self, samplerate, params={}):
        super(BeatDetector, self).__init__(samplerate, params)

        # Low Pass filter time constant
        self.t_filter = 1.0 / (2.0 * math.pi * self._params["lowpass_frequency"])

        self.filter1_out = 0.0
        self.filter2_out = 0.0
        self.peak_env = 0.0
        self.beat_trigger = False
        self.prev_beat_pulse = False
        self.num_beats = 0
        self.peak = 0.0

        self.kbeat_filter = 1.0 / (self._samplerate * self.t_filter)
        self.beat_release = math.exp(-1.0 / (self._samplerate *
                                     self._params["beat_release_time"]))

    def _process_sample(self, sample, channel_number):
        self.filter1_out = self.filter1_out + \
            (self.kbeat_filter * (sample - self.filter1_out))
        self.filter2_out = self.filter2_out + \
            (self.kbeat_filter * (self.filter1_out - self.filter2_out))

        return self.filter2_out


class RMS(Plugin):
    """RMS measure for the data. Strictly mono atm"""
    _default_params = {
        "rms_window": 1024,  # Samples
    }

    def __init__(self, samplerate, params={}):
        super(RMS, self).__init__(samplerate, params)
        self._rms = [0.0] * self._params["rms_window"]

    def _process_sample(self, sample, channel_number):
        self._rms = self._rms[1:] + [sample ** 2]
        self._rms_value = math.sqrt(sum(self._rms) / self._params["rms_window"])

        return sample

    def get_state(self):
        return {"rms": self._rms_value}
