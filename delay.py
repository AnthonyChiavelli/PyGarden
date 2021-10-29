from __future__ import annotations
from signal_sources.signal_source import SignalSource
import consts


class DelayLine(SignalSource):
    def __init__(self, *, delay_ms: float = 450, decay: float = 0.4, signal):
        super().__init__()
        self.signal = signal
        self.delay_ms = delay_ms
        self.delay_samples = (delay_ms / 1000) * consts.SAMPLE_RATE
        self.decay = decay
        # TODO accept as param?
        self.limit = self.delay_samples
        self.buffer: list[float] = []
        self.i = 0

    def __next__(self) -> float:
        s = next(self.signal)

        if len(self.buffer) < self.delay_samples:
            fs = s
            self.buffer.append(fs)
        else:
            ds = self.buffer.pop(0)
            fs = s + (ds * self.decay)
            self.buffer.append(fs)
        # if self.i > self.limit:
        #     self.buffer.clear()

        self.i += 1
        return fs

        return next(self.signal)
