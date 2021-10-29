from __future__ import annotations
from typing import Generator, Union
from signal_sources.signal_source import SignalSource

SignalGenerator = Union[Generator[float, None, None], SignalSource]

ModParameter = Union[float, SignalGenerator]
