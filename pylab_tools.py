import pylab
import operator

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
            ax.plot(map(operator.itemgetter(channel), signal), *args)
            ax.set_ylabel('S%s' % channel, **yprops)

            if channel == 0:
                axprops['sharex'] = ax
                # axprops['sharey'] = ax

            if channel < channels - 1:
                pylab.setp(ax.get_xticklabels(), visible=False)

class ProbeResultsPlotter(object):
    """docstring for ProbeResultsPlotter"""
    def __init__(self, results, margin=0.1, figure_name=None):
        self._results = results
        self._margin = margin
        self._fig = pylab.figure(figure_name, figsize=(10, 10))
        self._client_space = 1.0 - 2.0 * self._margin
        self._total_height = 0.0

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
                    ax = self._add_graph(map(operator.itemgetter(channel), res))
                    if channels > 1:
                        ax.set_ylabel('%s #%s' % (label, channel + 1), **self._yprops)
                    else:
                        ax.set_ylabel(label, **self._yprops)
            else:
                ax = self._add_graph(res)
                ax.set_ylabel(label, **self._yprops)


    def _add_graph(self, data):
        ax = self._fig.add_axes([self._margin * 2, # left
                                    1 - self._margin - self._client_space / self._total_height * (self._counter + 1), # bottom
                                    self._client_space - self._margin, # width
                                    self._client_space / self._total_height * 0.9 # height
                                ], **self._axprops)

        ax.plot(data)
        self._counter += 1

        if self._counter == 1:
            self._axprops['sharex'] = ax

        if self._counter < self._total_height:
            pylab.setp(ax.get_xticklabels(), visible=False)

        return ax
