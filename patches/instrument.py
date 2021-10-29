from signal_sources.oscillators import Oscillator


class Instrument(Oscillator):
    def __init__(self, freq: int, amp: float):
        self.freq: int = freq
        self.amp: float = amp
        if getattr(self, "get_generator"):
            self.generator = self.get_generator()

    def get_name(self):
        if self.name:
            return self.name
        raise NotImplementedError("Must implement Instrument.get_name in subclasses")
