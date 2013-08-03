dsp-testbed
===========

Simple test bed for my dsp experiments. Plugins, stacks of plugins, tools, measurements.

Very alpha stage, just a direct dump of my thoughts to the IDE.

At the moment it can read aiff files, process audio data with simple plugins (LP filter and RMS 
measurer is present), display signals with pylab and write results to wave files.

Obviosly it's not a real project but a set of supporting tools for DSP programming, experiments
and rapid prototyping. However even now it's helpful to me and hopefully it'll grow a little bit more.

## Requirements
Core files (plugins.py/stacks.py) doesn't require anything.
processing_test.py is using matplotlib for data visualisation
recording_test.py is using PyAudio and basically is heavily facelifted
script from http://www.stanford.edu/class/linguist278/notes/interactive-recorder.py
(kudos to it's author) with some beat detection based on this code:
http://musicdsp.org/archive.php?classid=2#200

## Speed
Well DSP test bed is built for comfort not for speed. However I have plans to profile it deeply once major
APIs will settle down.

## Signal displaying
DSP test bed is using pylab to display signals. Because speed of pylab is an issue when you have tons of
data points (like you usually do with audio signals) DSP test bed has simple yet effective signal decimation
implemented in pylab_tools.py. Results are pretty neat (and it muuuch faster).

## Thanks
* DSPMaster[at]free[dot]fr for beat detection
* Christopher Potts (at least it's the only name I found around interactive-recorder.py)
Not so many of external code has been used but it was a great inspiration for me.