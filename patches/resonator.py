from pygame import midi

from filters.resonant import ResonantFilter
from patches.instrument import Instrument
from signal_components.envelopes import get_adsr_envelope
from signal_components.oscillators import SawtoothWave
from signal_components.param_source import ModWheelSource


class Resonator(Instrument):
    name = "Resonator"

    def get_generator(self):
        note = midi.frequency_to_midi(self.freq)
        amp_env = get_adsr_envelope(0, 0.2, 0.7, 0.7, note)

        osc = SawtoothWave(freq=self.freq, amp=amp_env)
        osc = ResonantFilter(0, ModWheelSource(0.2, 0.8), osc)

        return osc
