import math

from signal_sources import SignalSource

import consts
from global_data import global_sound_mods
from helpers import generatorize_param


class BandPassFilter(SignalSource):
    def __init__(self, cutoff, signal):
        self.signal = signal
        self.cutoff = generatorize_param(cutoff)
        self.buffer = []

        self.delay_in_1 = 0
        self.delay_in_2 = 0
        self.delay_out_1 = 0
        self.delay_out_2 = 0

    def __next__(self):
        sample = next(self.signal)
        mod_wheel = global_sound_mods["mod_wheel"]

        cutoff = max(20000 * mod_wheel, 10)

        c = 1 / math.tan((math.pi / consts.SAMPLE_RATE) * cutoff)
        d = 1 + c
        b0 = 1 / d
        b1 = 0
        b2 = -b0
        a1 = (-c * 2 * math.cos(math.pi * 2 * cutoff / consts.SAMPLE_RATE)) / d
        a2 = (c - 1) / d

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
