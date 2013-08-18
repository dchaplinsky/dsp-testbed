dsp-testbed
===========
[![Build Status](https://travis-ci.org/dchaplinsky/dsp-testbed.png?branch=master)](https://travis-ci.org/dchaplinsky/dsp-testbed) [![Coverage Status](https://coveralls.io/repos/dchaplinsky/dsp-testbed/badge.png?branch=master)](https://coveralls.io/r/dchaplinsky/dsp-testbed?branch=master)

Simple test bed for dsp experiments. Plugins, stacks of plugins, tools, measurements, graphics.

At the moment it can read aiff/wave files, process audio data with simple plugins (LP filter and RMS 
measurer is present), display signals with pylab and write results to aiff/wave files or export
to .mat.

Obviosly it's not a real project but a set of supporting tools for DSP programming, experiments
and rapid prototyping. However even now it's helpful to me and hopefully it'll grow a little bit more.

## Few words on architecture
* **Plugins**. Very similar to those you might seen in VST (except the multichannel input is interleaved, not stripped).
You are instantiating them with audio params (samplerate and number of channels) and plugin params (cut off, Q, etc).
You can feed data into them using **process** method. You can query inner states of them using **state** method.
* **Stacks**. Chain of plugins, where output of previous one is connected to the input of the next one.
Also stacks are capable to read data from signal sources (see below) and write down for you important values using
tool called probe.
You are instantiating stacks with list of plugins and for each of plugins you can specify a list of state variables to track
You can feed input data using **process** method or by directly connecting signal source to the stack with **process_source**
You can take some measures using **probe** method or just by accessing **probe_results** field (which is prepopulated
with probe values gathered after processing a batch with **process_source**).
* Descendants of **AbstractReader** providing input for Plugins or Stacks. Think Aiff/Wave reader,
sine generators, etc. Implemented at the moment: **DiracSource**, **AiffReader**, **WaveReader**, **SineSource**, **CompoundSineSource**.
**endless** property of class specifying if the data is generated forever.
* Graph tools like **ProbeResultsPlotter** which you can use with probe results produced by **Stacks**.
* You can write results into wave/aiff file (using variety of bit depths) and export to .mat file which you 
can later read with Matlab(tm), GNU Octave, Scipy etc. Check **writers.py** for details. 

## Compatibility
DSP test bed is working with Python 2.6, 2.7 and PyPy

## Requirements
Core files (plugins.py/stacks.py/readers.py/writers.py) doesn't require anything.
processing_test.py is using matplotlib for data visualisation
recording_test.py is using PyAudio and basically is heavily facelifted
script from http://www.stanford.edu/class/linguist278/notes/interactive-recorder.py
(kudos to it's author) with some beat detection based on this code:
http://musicdsp.org/archive.php?classid=2#200

## Speed
Well DSP test bed is built for comfort not for speed. However I have plans to profile it deeply once major
APIs will settle down. Also as core of the lib is written using pure python you can use DSP test bed with pypy.

## Signal displaying
DSP test bed is using pylab to display signals. Because speed of pylab is an issue when you have tons of
data points (like you usually do with audio signals) DSP test bed has simple yet effective signal decimation
implemented in pylab_tools.py. Results are pretty neat (and it's muuuch faster).

## Thanks
* DSPMaster[at]free[dot]fr for beat detection
* Christopher Potts (at least it's the only name I found around interactive-recorder.py)

Not so many of external code has been used but it was a great inspiration for me.

[![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/dchaplinsky/dsp-testbed/trend.png)](https://bitdeli.com/free "Bitdeli Badge")
