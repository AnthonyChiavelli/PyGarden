from pygame import midi

from filters.low_pass import LowPassFilter
from helpers import compose_oscillators, mutiply_generators
from patches.instrument import Instrument
from signal_components.envelopes import get_adsr_envelope
from signal_components.noise import WhiteNoise
from signal_components.oscillators import SinWave


class Flute(Instrument):
    name = "Flute"

    def get_generator(self):
        note = midi.frequency_to_midi(self.freq)
        amp_env = get_adsr_envelope(0.2, 0, 0.9, 0, note)

        vibratto_lfo = SinWave(5, 1).rescale(
            old_range=(-1, 1), new_range=(self.freq - 10, self.freq + 10)
        )
        vibratto_lfo2 = SinWave(5, 1).rescale(
            old_range=(-1, 1), new_range=(self.freq * 2 - 10, self.freq * 2 + 10)
        )

        oscs = [
            SinWave(freq=vibratto_lfo, amp=1 / 2),
            SinWave(freq=vibratto_lfo2, amp=1 / 2),
            LowPassFilter(1200, WhiteNoise(get_adsr_envelope(0.1, 0.3, 0, 0))),
        ]

        osc = compose_oscillators(oscs)
        osc = mutiply_generators(osc, amp_env)
        return osc
