from __future__ import annotations

from typing import Generator, Union

from signal_components.signal_source import SignalSource

GeneratorT = Union[Generator[float, None, None], SignalSource]

# Old
SignalGenerator = Union[Generator[float, None, None], SignalSource]

ModParameter = Union[float, SignalGenerator]
