"""
Extension namespace: edge adapters and protocols.

- :class:`ChannelAdapter` — implement ``capture()`` → :class:`memory_phase_kernel.contracts.LiveSignalFrame`
- :class:`KeystrokeRhythmStubAdapter` — demo keystroke channel scores
"""

from .keystroke_stub import KeystrokeRhythmStubAdapter
from .protocols import ChannelAdapter

__all__ = ["ChannelAdapter", "KeystrokeRhythmStubAdapter"]
