import math

import consts
from helpers import generatorize_param
from signal_components.signal_source import SignalSource


class LowPassFilter(SignalSource):
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
        cutoff = next(self.cutoff)

        # Filter coefficients
        c = 1 / math.tan((math.pi / consts.SAMPLE_RATE) * cutoff)
        c2 = c * c
        c_sqr_2 = math.sqrt(2) * c
        d = c2 + c_sqr_2 + 1
        b0 = 1 / d
        b1 = b0 * 2
        b2 = b0
        a1 = (2 * (1 - c2)) / d
        a2 = (c2 - c_sqr_2 + 1) / d

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
