from __future__ import annotations

from global_data import global_sound_mods
from signal_components.signal_source import SignalSource


class PitchModWheelSource(SignalSource):
    def __init__(self, base_freq: int, range: int):
        self.base_freq = base_freq
        self.range = range

    def __next__(self) -> float:
        mod_val: float = global_sound_mods["pitch_mod"]
        delta: float = mod_val * self.range
        return self.base_freq + delta


class ModWheelSource(SignalSource):
    def __init__(self, min: int, max: int):
        self.min: int = min
        self.max: int = max

    def __next__(self) -> float:
        mod_val: float = global_sound_mods["mod_wheel"]
        return mod_val * (self.max - self.min) + self.min
