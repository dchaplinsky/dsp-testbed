import pylab
from math import ceil
from operator import itemgetter

def plot_signal(signal, *args):
    channels = len(signal[0])
    margin = 0.1
    client_space = 1 - 2 * margin

    if channels == 1:
        pylab.plot(signal, *args)
    else:
        yprops = {"rotation": 0,
                  "horizontalalignment": "right",
                  "verticalalignment": "center",
                  "x": -0.01}

        axprops = {}
        fig = pylab.figure()

        for channel in xrange(channels):
            ax =fig.add_axes([margin, 1 - margin - client_space / channels * (channel + 1), 
                              client_space, client_space / channels], **axprops)
            ax.plot(map(itemgetter(channel), signal), *args)
            ax.set_ylabel('S%s' % channel, **yprops)

            if channel == 0:
                axprops['sharex'] = ax
                # axprops['sharey'] = ax

            if channel < channels - 1:
                pylab.setp(ax.get_xticklabels(), visible=False)

class ProbeResultsPlotter(object):
    """docstring for ProbeResultsPlotter"""
    def __init__(self, results, margin=0.1, figure_name=None, decimate=True, bins=None):
        self._results = results
        self._margin = margin
        self._fig = pylab.figure(figure_name, figsize=(10, 10))
        self._client_space = 1.0 - 2.0 * self._margin
        self._total_height = 0.0
        self._decimate = decimate
        self._bins = bins

        get_height = lambda res: (len(res[0]), True) \
            if isinstance(res[0], (tuple, list)) else (1.0, False)

        for label, res in results.iteritems():
            self._total_height += get_height(res)[0]

        self._counter = 0
        self._yprops = {"rotation": 0,
                        "horizontalalignment": "right",
                        "verticalalignment": "center",
                        "x": -0.01}

        self._axprops = {}

        for label, res in results.iteritems():
            res_height, is_multichannel = get_height(res)

            if is_multichannel:
                channels = len(res[0])
                for channel in xrange(channels):
                    ax = self._add_graph(map(itemgetter(channel), res))
                    if channels > 1:
                        ax.set_ylabel('%s #%s' % (label, channel + 1), **self._yprops)
                    else:
                        ax.set_ylabel(label, **self._yprops)
            else:
                ax = self._add_graph(res)
                ax.set_ylabel(label, **self._yprops)

    def _decimate_data(self, data, bins=None):
        if not bins:
            bins = self._get_width()

        if bins == 0:
            bins = 1

        bin_width = int(len(data) / bins) or 1

        out = []
        x = []
        for i in xrange(int(ceil(len(data) / float(bin_width)))):
            chunk = data[i * bin_width:(i + 1) * bin_width]

            y_max = max(chunk)
            y_min = min(chunk)
            x_max = chunk.index(y_max) + i * bin_width
            x_min = chunk.index(y_min) + i * bin_width

            if x_min > x_max:
                x += [x_max, x_min]
                out += [y_max, y_min]
            else:
                x += [x_min, x_max]
                out += [y_min, y_max]

        return x, out

    def _get_width(self):
        return self._fig.get_figwidth() * self._fig.get_dpi() * (self._client_space - self._margin)

    def _add_graph(self, data):
        x = False
        if self._decimate:
            x, data = self._decimate_data(data, self._bins)

        ax = self._fig.add_axes([self._margin * 2, # left
                                    1 - self._margin - self._client_space / self._total_height * (self._counter + 1), # bottom
                                    self._client_space - self._margin, # width
                                    self._client_space / self._total_height * 0.9 # height
                                ], **self._axprops)

        if x:
            ax.plot(x, data)
        else:
            ax.plot(data)

        self._counter += 1

        if self._counter == 1:
            self._axprops['sharex'] = ax

        if self._counter < self._total_height:
            pylab.setp(ax.get_xticklabels(), visible=False)

        return ax
