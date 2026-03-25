from __future__ import annotations

from typing import Protocol, Tuple, runtime_checkable

from ..contracts import LiveSignalFrame


@runtime_checkable
class ChannelAdapter(Protocol):
    """
    Edge sensor / modality plugin: produces a :class:`LiveSignalFrame` per tick.

    Implementations may call into on-device ML; the kernel only consumes scores.
    """

    @property
    def adapter_id(self) -> str:
        """Stable id for logging and profile weight keys."""

    def capture(self) -> LiveSignalFrame:
        """Return current observations (may be empty if sensor unavailable)."""
