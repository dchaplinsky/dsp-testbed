import math
from copy import deepcopy

class Plugin(object):
    """Abstract plugin for audio processing and analysis"""
    _default_params = {}

    def __init__(self, samplerate=44100, channels=1, params={}):
        super(Plugin, self).__init__()
        self._samplerate = samplerate
        self._channels = channels
        self._params = deepcopy(self._default_params)
        self._params.update(params)

    def process(self, samples):
        """
        Pass data in form 
        [[channel1_sample1, channel2_sample1...], 
         [channel1_sample2, channel2_sample2...], ...]

        Beware, most of plugins is strictly mono right now
        """
        self._last_output = []
        for sample in samples:
            self._last_output.append([self._process_sample(s, i) for i, s in enumerate(sample)])

        return self._last_output

    def get_state(self):
        """
        Feturns dict with the inner state of plugin.
        Useful for measurments (like RMS plugin) or debugging.
        """
        return {
            "output": self._last_output
        }

    def _process_sample(self, sample, channel_number):
        return sample


class LowPassFilter(Plugin):
    """LowPassFilter plugin. 2'nd order"""
    _default_params = {
        "lowpass_frequency": 150.0,  # Herts
        "beat_release_time": 0.01,  # seconds
    }

    def __init__(self, samplerate=44100, channels=1, params={}):
        super(LowPassFilter, self).__init__(samplerate, channels, params)

        # Low Pass filter time constant
        self.t_filter = 1.0 / (2.0 * math.pi * self._params["lowpass_frequency"])

        self.filter1_out = [0.0] * channels
        self.filter2_out = [0.0] * channels

        self.kbeat_filter = 1.0 / (self._samplerate * self.t_filter)

    def _process_sample(self, sample, channel_number):
        self.filter1_out[channel_number] = self.filter1_out[channel_number] + \
            (self.kbeat_filter * (sample - self.filter1_out[channel_number]))
        self.filter2_out[channel_number] = self.filter2_out[channel_number] + \
            (self.kbeat_filter * (self.filter1_out[channel_number] - self.filter2_out[channel_number]))

        return self.filter2_out[channel_number]


class RMS(Plugin):
    """RMS measure for the data."""
    _default_params = {
        "rms_window": 1024,  # Samples
    }

    def __init__(self, samplerate=44100, channels=1, params={}):
        super(RMS, self).__init__(samplerate, channels, params)
        self._rms = [[0.0] * self._params["rms_window"]] * channels
        self._rms_value = [0.0] * channels

    def _process_sample(self, sample, channel_number):
        self._rms[channel_number] = self._rms[channel_number][1:] + [sample ** 2]
        self._rms_value[channel_number] = math.sqrt(sum(self._rms[channel_number]) / self._params["rms_window"])

        return sample

    def get_state(self):
        state = super(RMS, self).get_state()
        state.update({"rms": deepcopy(self._rms_value)})
        return state
