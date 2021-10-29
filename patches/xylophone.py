from patches.instrument import Instrument
from pygame import midi
from signal_sources.oscillators import SinWave
from signal_sources.envelopes import get_adsr_envelope


class Xylophone(Instrument):
    name = "Xylophone"

    def get_generator(self):

        note = midi.frequency_to_midi(self.freq)

        env = get_adsr_envelope(0, 0.05, 0.3, 1, note, True)
        osc1 = SinWave(freq=self.freq * 1.8, amp=env)
        oscillator = SinWave(self.freq, osc1)

        return oscillator
