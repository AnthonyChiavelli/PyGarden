from filters.low_pass import LowPassFilter
from patches.instrument import Instrument
from helpers import amplify, compose_oscillators
from signal_sources.oscillators import SawtoothWave, SinWave
from signal_sources.param_source import PitchModWheelSource
from pygame import midi
from signal_sources.envelopes import get_adsr_envelope


class QuadSaw(Instrument):
    name = "Quad Saw"

    def get_generator(self):
        note = midi.frequency_to_midi(self.freq)
        detune = 1
        amp_env = get_adsr_envelope(0.1, 0.2, 0.7, 0.5, note)
        filter_lfo = SinWave(5, 1).rescale(old_range=(-1, 1), new_range=(6400, 10000))

        oscillators = [
            SawtoothWave(
                freq=PitchModWheelSource(self.freq + (detune * i), (self.freq)),
                amp=amp_env,
            )
            for i in range(4)
        ]

        osc = compose_oscillators(oscillators)
        osc = LowPassFilter(filter_lfo, osc)
        osc = amplify(osc, 3)
        return osc
