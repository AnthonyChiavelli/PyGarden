from __future__ import annotations

import random

from helpers import generatorize_param, perpetuity
from signal_components.signal_source import SignalSource
from typedefs import SignalGenerator


class WhiteNoise(SignalSource):
    def __init__(self, amp: SignalGenerator):
        amp = generatorize_param(amp)
        random_generator = ((random.random() - 0.5) * next(amp) for _ in perpetuity())
        super().__init__(random_generator)
