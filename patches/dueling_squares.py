from filters.low_pass import LowPassFilter
from patches.instrument import Instrument
from helpers import amplify, compose_oscillators
from signal_sources.oscillators import SinWave, SquareWave
from pygame import midi
from signal_sources.envelopes import get_adsr_envelope
from signal_sources.param_source import ModWheelSource


class DuelingSquares(Instrument):
    name = "Dueling Squares"

    def get_generator(self):
        note = midi.frequency_to_midi(self.freq)
        detune = 5
        amp_env = get_adsr_envelope(0, 0.2, 0.7, 0.7, note)

        osc = SquareWave(freq=self.freq, amp=amp_env)
        osc1 = SquareWave(freq=self.freq + (detune), amp=amp_env)

        osc = compose_oscillators([osc, osc1])

        mod_src = ModWheelSource(1, 10)
        filter_lfo = SinWave(mod_src, 1).rescale(
            old_range=(-1, 1), new_range=(1600, 3200)
        )

        osc = LowPassFilter(filter_lfo, osc)
        osc = amplify(osc, 1.5)
        return osc
