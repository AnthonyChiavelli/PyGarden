from filters.low_pass import LowPassFilter
from patches.instrument import Instrument
from helpers import amplify, compose_oscillators
from pygame import midi
from signal_sources.oscillators import SawtoothWave
from signal_sources.envelopes import get_adsr_envelope, get_ramp
from consts import SAMPLE_RATE
from signal_sources.param_source import ModWheelSource


class QuirkySaw(Instrument):
    name = "Quirky Saw"

    def get_generator(self):
        note = midi.frequency_to_midi(self.freq)

        amp_env = get_adsr_envelope(0.1, 0.2, 0.7, 1, note)
        osc = SawtoothWave(freq=self.freq, amp=amp_env)

        downramp = get_ramp(self.freq, self.freq * 1.1, SAMPLE_RATE / 6, upward=False)
        osc2 = SawtoothWave(freq=downramp, amp=amp_env)

        osc = compose_oscillators([osc, osc2])
        osc = LowPassFilter(ModWheelSource(20, 8000), osc)
        osc = amplify(osc, 3)
        return osc
