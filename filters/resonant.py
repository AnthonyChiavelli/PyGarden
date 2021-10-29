import math
from helpers import generatorize_param
from signal_sources.signal_source import SignalSource
from global_data import global_sound_mods
import consts


class ResonantFilter(SignalSource):
    def __init__(self, cutoff, resonance, signal):
        self.signal = signal
        self.cutoff = generatorize_param(cutoff)
        self.resonance = generatorize_param(resonance)
        self.buffer = []

        self.delay_in_1 = 0
        self.delay_in_2 = 0
        self.delay_out_1 = 0
        self.delay_out_2 = 0

    def __next__(self):
        sample = next(self.signal)
        resonance = next(self.resonance)
        mod_wheel = global_sound_mods["mod_wheel"]

        freq_cutoff = consts.SAMPLE_RATE / 2 * mod_wheel

        c = 2 * resonance * math.cos((2 * math.pi / consts.SAMPLE_RATE) * freq_cutoff)
        a1 = -c
        a2 = resonance ** 2
        b0 = 0.5 - ((resonance ** 2) / 2)
        b1 = 0
        b2 = c

        out = (
            (b0 * sample)
            + (b1 * self.delay_in_1)
            + (b2 * self.delay_in_2)
            - (a1 * self.delay_out_1)
            - (a2 * self.delay_out_2)
        )

        self.delay_out_2 = self.delay_out_1
        self.delay_out_1 = out
        self.delay_in_2 = self.delay_in_1
        self.delay_in_1 = sample

        return out
