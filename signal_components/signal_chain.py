from __future__ import annotations

from typing import List

from signal_components.signal_component import SignalComponent


class SignalChain:
    components: List[SignalComponent]
