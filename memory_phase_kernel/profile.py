from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Tuple

from .contracts import ChannelReading, IdentityScoreBundle, LiveSignalFrame
from .resonance import compute_resonance_index


@dataclass(frozen=True)
class ChannelSpec:
    """Declared channel for enrollment / edge adapter registration."""

    channel_id: str
    weight: float = 1.0
    description: str = ""


@dataclass(frozen=True)
class IdentityProfile:
    """
    Long-term memory slice (embeddings live outside this module).

    `channel_weights` map channel_id → policy weight for Ω_res.
    """

    subject_id: str
    channel_weights: Mapping[str, float] = field(default_factory=dict)
    version: int = 1


def score_frame(
    profile: IdentityProfile,
    frame: LiveSignalFrame,
    *,
    confidence: float = 0.9,
    drift_hint: float = 0.1,
    intrusion_hint: float = 0.05,
    identity_score_override: float | None = None,
) -> IdentityScoreBundle:
    """
    Combine resonance (Ω_res) with optional override.

    v0.1: identity_score defaults to resonance_index; callers may blend trust anchor.
    """
    omega = compute_resonance_index(frame.readings, profile.channel_weights)
    ident = omega if identity_score_override is None else identity_score_override
    ident = max(0.0, min(1.0, ident))
    return IdentityScoreBundle(
        identity_score=ident,
        confidence=max(0.0, min(1.0, confidence)),
        drift_hint=max(0.0, min(1.0, drift_hint)),
        intrusion_hint=max(0.0, min(1.0, intrusion_hint)),
        resonance_index=omega,
        symmetry_score=None,
        oscillation_score=None,
        damping_score=None,
        collapse_score=None,
    )


def readings_from_simple_map(scores: Mapping[str, float]) -> Tuple[ChannelReading, ...]:
    """Helper for tests and thin adapters: channel_id -> raw match score."""
    return tuple(
        ChannelReading(channel_id=k, match_score=max(0.0, min(1.0, float(v))))
        for k, v in sorted(scores.items())
    )
