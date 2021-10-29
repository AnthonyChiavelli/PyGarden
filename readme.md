# SquareGarden

## A toy Python synthesizer

SquareGarden is a simple proof-of-concept synthesizer written in Python. It allows the creation of custom patches by combining various signal sources and filters. Currently it responds to MIDI commands.

### To Run

Run 'pipenv install' in the root folder
Run 'pipenv shell' to enter a virtualenv (mico-environment with the right python version + packages)
Run 'python backend.py', making sure a MIDI device is plugged in

Use the 'prev track' and 'next track' buttons on the MIDI controller to switch pactches
Use the 'stop track' button to exit
Use the pitch wheel and mod wheel to modify any patch that is set up to use them as a signal source

### Formatting

The scripts folders contains a script format.sh (runs black), lint.sh (runs flake8), typing.sh (runs mypy), and a script full_clean.sh to run them all

### Architecture

All signal sources and filters are implemented as generator classes that yield successive sound samples. Any generator classes designed to output a signal should be a subclass of SignalSource (e.g. LGO's, wave oscillators, ADSR envelopes). A SignalSource may take input from another SignalSource, or it may
not.

SignalSources that generate a wave signal subclass Oscillator, which requires implementation of either get_generator(), to provide a sample-yielding generator, or implementation of **next**, making the class itself a generator.

Patches are configurations of SignalSources that you wish to save as a present instrument. These classes should subclass Instrument, and implement the get_generator() method to return a sample-yielding generator.

The main loop of the app listens on midi commands and invokes the relevant generator (depending on current patch selection) to send sound samples to the audio interface. Various MIDI controls (pitch wheel, mod wheel, etc) are monitored, and are represented by SignalSource subclasses that emit the current mod setting as a signal.

In the future there will be a graphical interface for controlling the synthesizer.

### TODO

TODO: Implement a parent class for all signal acceptors
TODO: Implement a SignalChain construct that can take a chain of SignalAcceptors/SignalGenerators and compose them together
TODO: Make type-safe and lint-free
