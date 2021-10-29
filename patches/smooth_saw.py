from pygame import midi

from filters.low_pass import LowPassFilter
from helpers import amplify, rescale_generator
from patches.instrument import Instrument
from signal_components.envelopes import get_adsr_envelope
from signal_components.oscillators import SawtoothWave


class SmoothSaw(Instrument):
    name = "Smooth Saw"

    def get_generator(self):
        note = midi.frequency_to_midi(self.freq)
        amp_env = get_adsr_envelope(0, 0.2, 0.7, 0.7, note)
        filter_env = get_adsr_envelope(0.2, 1, 0.2, 0.7, note)
        filter_env = rescale_generator(filter_env, (0, 1), (800, 2400))

        osc = SawtoothWave(self.freq, amp_env)
        osc = LowPassFilter(filter_env, osc)
        osc = amplify(osc, 3)
        return osc
