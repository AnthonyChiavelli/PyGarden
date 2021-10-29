from patches.instrument import Instrument
from signal_sources.oscillators import SinWave, SquareWave
from pygame import midi
from signal_sources.envelopes import get_adsr_envelope


class Pulsar(Instrument):
    name = "Pulsar"

    def get_generator(self):
        note = midi.frequency_to_midi(self.freq)
        amp_env = get_adsr_envelope(0, 0.2, 0.7, 0.7, note)

        shape_lfo = SinWave(3, 1).rescale(old_range=(-1, 1), new_range=(0.5, 1))
        osc = SquareWave(freq=self.freq, amp=amp_env, shape=shape_lfo)

        return osc
