import pyaudio
from pygame import midi

import consts


class KeyRelease(Exception):
    pass


def initialize_audio(
    BUFFER_SIZE: int = consts.BUFFER_SIZE, SAMPLE_RATE: int = consts.SAMPLE_RATE
) -> pyaudio.Stream:
    stream = pyaudio.PyAudio().open(
        rate=SAMPLE_RATE,
        channels=1,
        format=pyaudio.paInt16,
        output=True,
        frames_per_buffer=BUFFER_SIZE,
    )

    return stream


def initialize_midi_input() -> midi.Input:
    midi.init()
    default_id = midi.get_default_input_id()
    if default_id == -1:
        raise IOError("No MIDI device detected")
    return midi.Input(device_id=default_id)
