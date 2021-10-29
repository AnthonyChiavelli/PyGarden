import math
from helpers import generatorize_param
from signal_sources import SignalSource
import consts


class HighPassFilter(SignalSource):
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

        c = math.tan((math.pi / consts.SAMPLE_RATE) * self.cutoff)
        c2 = c * c
        csqr2 = math.sqrt(2) * c
        d = c2 + csqr2 + 1
        b0 = 1 / d
        b1 = -(b0 + b0)
        b2 = b0
        a1 = (2 * (c2 - 1)) / d
        a2 = (c2 - csqr2 + 1) / d

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
