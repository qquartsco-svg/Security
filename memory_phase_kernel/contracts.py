from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import FrozenSet, Literal, Mapping, Tuple

SensitivityTier = Literal["public", "operational", "personal", "executive"]


class DataPhase(str, Enum):
    """Interpretability phase: liquid (masked) → semi → frozen (full decode window)."""

    LIQUID = "liquid"
    SEMI_FROZEN = "semi_frozen"
    FROZEN = "frozen"


class AuditSurface(str, Enum):
    """What class of audit record this kernel may emit (implementations choose storage)."""

    PHASE_TRANSITION = "phase_transition"
    RE_MELT = "re_melt"
    TRUST_ANCHOR_CHALLENGE = "trust_anchor_challenge"


@dataclass(frozen=True)
class PolicyThresholds:
    """Tunable policy bands; inject for A/B or maturity schedules."""

    frozen_threshold: float = 0.82
    semi_threshold: float = 0.55
    intrusion_re_melt_threshold: float = 0.65
    idle_re_melt_seconds: float = 900.0


@dataclass(frozen=True)
class ChannelReading:
    """Single channel contribution before weighting."""

    channel_id: str
    match_score: float  # 0..1
    quality: float = 1.0  # 0..1 anti-spoof / signal quality


@dataclass(frozen=True)
class LiveSignalFrame:
    """One tick of live observations (edge AI feeds this)."""

    readings: Tuple[ChannelReading, ...] = field(default_factory=tuple)
    idle_seconds: float = 0.0


@dataclass(frozen=True)
class IdentityScoreBundle:
    """Scoring layer output."""

    identity_score: float
    confidence: float
    drift_hint: float
    intrusion_hint: float
    resonance_index: float
    symmetry_score: float | None = None
    oscillation_score: float | None = None
    damping_score: float | None = None
    collapse_score: float | None = None


@dataclass(frozen=True)
class AccessDecision:
    """What interpretability phase is allowed and which data tiers may decode."""

    phase: DataPhase
    allowed_tiers: Tuple[SensitivityTier, ...]
    reason: str
    score_bundle: IdentityScoreBundle


@dataclass(frozen=True)
class ReMeltEvent:
    """Policy signal to drop keys / mask UI / end interpretation window."""

    reason: str
    force_liquid: bool = True
    suggested_audit: FrozenSet[AuditSurface] = field(
        default_factory=lambda: frozenset({AuditSurface.RE_MELT})
    )
