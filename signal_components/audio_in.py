from __future__ import annotations

from typing import Generator

from helpers import generatorize_param
from signal_components.signal_source import SignalSource


class AudioInSource(SignalSource):
    def __init__(self, amp: Generator | float):
        self.i: float = 0
        self.amp: Generator[float, None, None] = generatorize_param(amp)

    def get_params(self) -> float:
        return next(self.amp)

    def __next__(self) -> float:
        pass
