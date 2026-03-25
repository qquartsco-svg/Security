from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Tuple

from ..contracts import ChannelReading, LiveSignalFrame


@dataclass
class KeystrokeRhythmStubAdapter:
    """
    Demo / test adapter: simulates keystroke rhythm match scores.

    Replace with real digraph latency + entropy features in production code.
    """

    adapter_id: str = "keystroke_rhythm_stub"
    _scores: Dict[str, float] = field(default_factory=lambda: {"typing": 0.85})

    def capture(self) -> LiveSignalFrame:
        readings: Tuple[ChannelReading, ...] = tuple(
            ChannelReading(channel_id=k, match_score=float(v), quality=0.95)
            for k, v in sorted(self._scores.items())
        )
        return LiveSignalFrame(readings=readings, idle_seconds=0.0)

    def set_score(self, channel_id: str, value: float) -> None:
        self._scores[channel_id] = max(0.0, min(1.0, value))
