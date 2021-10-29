from __future__ import annotations

from typing import Any, Optional, Tuple

from helpers import perpetuity
from signal_components.signal_component import SignalComponent


class SignalSource(SignalComponent):
    def __init__(self, generator: Optional[Any] = None):
        if generator:
            self.generator = generator

    def __next__(self) -> float:
        return next(self.generator)

    def __iter__(self) -> SignalSource:
        return self

    def __add__(self, osc: SignalSource | Any) -> SignalSource:
        return SignalSource((next(self) + next(osc) for _ in perpetuity()))

    def rescale(
        self, *, old_range: Tuple[int, int] = (-1, 1), new_range: Tuple[int, int]
    ) -> SignalSource:
        def new_generator(
            osc: SignalSource | Any,
            old_range: Tuple[int, int],
            new_range: Tuple[int, int],
        ) -> Any:
            while True:
                next_val = next(osc)
                old_span = old_range[1] - old_range[0]
                new_span = new_range[1] - new_range[0]

                old_val = next_val / old_span
                new_val = (old_val * new_span) + new_range[0]

                yield new_val

        return SignalSource(new_generator(self, old_range, new_range))
