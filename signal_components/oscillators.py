from __future__ import annotations

import math
from typing import Optional

from consts import SAMPLE_RATE
from helpers import generatorize_param, perpetuity
from signal_components.signal_source import SignalSource
from typedefs import ModParameter, SignalGenerator


class Oscillator(SignalSource):
    def __init__(
        self,
        freq: ModParameter,
        amp: ModParameter,
        shape: Optional[ModParameter] = None,
    ):

        self.i: float = 0
        if getattr(self, "get_generator"):
            self.generator = self.get_generator()

        self.amp = generatorize_param(amp)
        self.freq = generatorize_param(freq)
        if shape:
            self.shape = generatorize_param(shape)

    def get_params(self) -> tuple[float, float, float]:
        return (
            next(self.freq),
            next(self.amp),
            next(self.shape) if hasattr(self, "shape") else 1,
        )

    def __next__(self) -> float:
        if not getattr(self, "get_generator"):
            raise NotImplementedError("Must implement __next__ or get_generator")
        return super().__next__()

    def get_generator(self) -> SignalGenerator:
        if not getattr(self, "__next__"):
            raise NotImplementedError("Must implement __next__ or get_generator")
        return (0 for _ in perpetuity())


class SinWave(Oscillator):
    def __next__(self) -> float:
        freq, amp, *_ = self.get_params()
        self.i += (2 * math.pi * (freq)) / SAMPLE_RATE
        v = math.sin(self.i) * amp
        if self.i == (2 * math.pi * (freq)):
            self.i = 0
        return v


class SawtoothWave(Oscillator):
    def __next__(self) -> float:
        freq, amp, *_ = self.get_params()
        increment = (2 * freq) / SAMPLE_RATE
        r = self.i * amp * 0.2
        self.i += increment
        if self.i > 1:
            self.i -= 2
        return r


class SquareWave(Oscillator):
    def __next__(self) -> float:
        freq, amp, shape = self.get_params()

        pulse_width = 2 * SAMPLE_RATE / freq
        self.i += 1
        if self.i >= ((pulse_width / 2) * shape):
            r = 0.5 * amp
        else:
            r = -0.5 * amp
        if self.i > pulse_width:
            self.i = 0

        return r
