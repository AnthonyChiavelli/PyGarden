from __future__ import annotations

from typing import Optional

import consts
import global_data
from audio import KeyRelease
from global_data import midi_state
from typedefs import SignalGenerator

# TODO implement as classes


def get_adsr_envelope(
    attack: float,
    decay: float,
    sustain: float,
    release: float,
    note: Optional[int] = None,
    keep_alive: bool = False,
) -> SignalGenerator:

    sample_count: int = 0
    vol: float = 0

    # Avoids harsh cutoff
    if release == 0:
        release = 0.2

    # Duration of each segment (in samples)
    attack_t: float = consts.SAMPLE_RATE * attack
    decay_t: float = consts.SAMPLE_RATE * decay
    release_t: float = consts.SAMPLE_RATE * release

    # Change in volume per sample for each segment
    attack_delta: Optional[float] = (1 - 0) / attack_t if attack > 0 else None
    decay_delta: Optional[float] = (1 - sustain) / decay_t if decay > 0 else None
    release_delta: Optional[float] = (sustain - 0) / release_t if release > 0 else None

    # Throw exception if key is released to jump to release phase
    def check_key_release(for_note: Optional[int]) -> None:
        if note:
            if midi_state.get(for_note, {}).get("key_state", None) == "released":
                raise KeyRelease

    try:
        # The attack phase: Rise from 0 to 1
        if attack > 0 and attack_delta:
            while sample_count < attack_t:
                check_key_release(note)
                sample_count += 1
                # Increment the volume from 0 to 1, over 'attack' seconds
                vol += attack_delta
                yield vol
        else:
            vol = 1
        sample_count = 0

        # Decay phase: Fall from 1 to 'sustain' level
        if decay > 0 and decay_delta:
            while sample_count < decay_t:
                check_key_release(note)
                sample_count += 1
                # Decrement the volume from 1 down to 'decay', over 'sustain' seconds
                vol -= decay_delta
                yield vol
            sample_count = 0

        # Sustain phase; holds the 'sustain' level while key is pressed
        while True:
            check_key_release(note)
            sample_count += 1
            yield sustain

    except KeyRelease:
        # Release phase: fade from sustain volume down to 0
        sample_count = 0
        # while sample_count < release_t:
        if release and release_delta:
            while vol > 0:
                # sample_count += 1
                vol -= release_delta
                yield vol

    # The note is over
    if note in midi_state:
        if not keep_alive:
            if global_data.global_sound_mods["delay"]:
                # TODO keep alive according to delay length settings?
                for _ in range(consts.SAMPLE_RATE):
                    yield vol
                del midi_state[note]
            else:
                del midi_state[note]
    while True:
        yield 0


def get_ramp(min: float, max: float, time: int, upward: bool = True) -> SignalGenerator:
    # todo accept generator params
    if upward:
        v = min
        interval = (max - min) / time
        while v < max:
            yield v
            v += interval
        while True:
            yield max
    else:
        v = max
        interval = (max - min) / time
        while v > min:
            yield v
            v -= interval
        while True:
            yield min
