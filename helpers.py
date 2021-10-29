from __future__ import annotations
from typing import Generator, Tuple, List
from consts import BUFFER_SIZE
import numpy as np

SignalGenerator = Generator[float, None, None]


class KeyRelease(Exception):
    pass


def perpetuity() -> Generator[None, None, None]:
    while True:
        yield


def compose_oscillators(oscillators: List[SignalGenerator]) -> SignalGenerator:
    while True:
        # TODO remove magic const
        yield sum(next(o) for o in oscillators) * 0.6


def amplify(osc: SignalGenerator, factor: int) -> SignalGenerator:
    while True:
        yield next(osc) * factor


def mutiply_generators(osc: SignalGenerator, osc2: SignalGenerator) -> SignalGenerator:
    while True:
        yield next(osc) * next(osc2)


# Extract enough samples from an oscillator to fill the buffer
def get_samples(oscillator: SignalGenerator, num_samples: int = BUFFER_SIZE) -> bytes:
    return np.int16(
        [int(next(oscillator) * 32767) for _ in range(BUFFER_SIZE)]
    ).tobytes()


# Change the output range of a generator from one min/max to a new min/max
def rescale_generator(
    osc: SignalGenerator, old_range: Tuple[int, int], new_range: Tuple[int, int]
) -> SignalGenerator:
    while True:
        next_val = next(osc)
        old_span = old_range[1] - old_range[0]
        new_span = new_range[1] - new_range[0]

        old_val = next_val / old_span
        new_val = (old_val * new_span) + new_range[0]

        yield new_val


# Convert constants into infinite generators so parameters can be given as numbers or generators
def generatorize_param(param: float | SignalGenerator) -> SignalGenerator:
    if isinstance(param, int) or isinstance(param, float):
        return (param for _ in perpetuity())
    else:
        return param
