from __future__ import annotations

from pygame import midi

from helpers import compose_oscillators, mutiply_generators
from patches.instrument import Instrument
from signal_components.envelopes import get_adsr_envelope
from signal_components.oscillators import Oscillator, SinWave
from signal_components.param_source import ModWheelSource
from typedefs import SignalGenerator


class Bells(Instrument):
    name = "Bells"

    def get_generator(self) -> SignalGenerator:
        note = midi.frequency_to_midi(self.freq)
        amp_env: SignalGenerator = get_adsr_envelope(0, 0.2, 0.4, 2.5, note)

        lo_osc = SinWave(self.freq, amp_env)

        am_freq = ModWheelSource(self.freq, self.freq * 2)

        am_mod0 = SinWave(am_freq, 1)

        am_mod: Oscillator = SinWave(am_freq, am_mod0)
        am_mod = am_mod.rescale(new_range=(0, 1))

        amp_env = mutiply_generators(amp_env, am_mod)
        hi_osc = SinWave(self.freq, amp_env)

        osc = compose_oscillators([hi_osc, lo_osc])

        return osc
