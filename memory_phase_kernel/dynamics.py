from __future__ import annotations

from dataclasses import dataclass, field
from typing import Tuple


@dataclass(frozen=True)
class PhaseDynamicsConfig:
    """Tunable dynamics for symmetry -> oscillation -> damping -> resonance -> collapse."""

    symmetry_gain: float = 1.0
    damping_gain: float = 1.0
    collapse_gain: float = 1.0
    history_window: int = 8


@dataclass(frozen=True)
class PhaseDynamicsState:
    """
    Minimal mathematical state for identity convergence.

    The idea is not physics literalism; it is a stable access-control dynamic
    that tracks whether remembered-user alignment is stabilizing or breaking down.
    """

    symmetry_score: float
    oscillation_score: float
    damping_score: float
    resonance_score: float
    collapse_score: float
    history: Tuple[float, ...] = field(default_factory=tuple)


def compute_symmetry_score(resonance_index: float, identity_score: float) -> float:
    """How structurally aligned stored memory and live input currently are."""
    resonance_index = _clamp01(resonance_index)
    identity_score = _clamp01(identity_score)
    return 1.0 - abs(resonance_index - identity_score)


def compute_oscillation_score(history: Tuple[float, ...], current_value: float) -> float:
    """
    Measure instability across recent ticks.

    High oscillation means the session still fluctuates a lot; low oscillation
    means the user model is settling.
    """

    current_value = _clamp01(current_value)
    if not history:
        return 0.0
    values = (*history, current_value)
    span = max(values) - min(values)
    return _clamp01(span)


def compute_damping_score(oscillation_score: float) -> float:
    """Inverse of oscillation in the simplest stable form."""
    return _clamp01(1.0 - _clamp01(oscillation_score))


def compute_resonance_gain(
    symmetry_score: float,
    damping_score: float,
    resonance_index: float,
    *,
    gain: float = 1.0,
) -> float:
    """Stable alignment grows when symmetry and damping are both healthy."""
    resonance_gain = _clamp01(symmetry_score) * _clamp01(damping_score) * _clamp01(resonance_index)
    return _clamp01(resonance_gain * max(0.0, gain))


def compute_collapse_score(
    resonance_gain: float,
    identity_score: float,
    intrusion_hint: float,
    *,
    gain: float = 1.0,
) -> float:
    """
    Final decision convergence.

    High intrusion should suppress collapse into trusted access even when
    resonance looks superficially strong.
    """

    trusted = _clamp01(resonance_gain) * _clamp01(identity_score)
    safety = 1.0 - _clamp01(intrusion_hint)
    return _clamp01(trusted * safety * max(0.0, gain))


def evolve_phase_dynamics(
    *,
    resonance_index: float,
    identity_score: float,
    intrusion_hint: float,
    previous_history: Tuple[float, ...] = (),
    config: PhaseDynamicsConfig | None = None,
) -> PhaseDynamicsState:
    """One-tick evolution of the access dynamics layer."""

    cfg = config or PhaseDynamicsConfig()
    symmetry = compute_symmetry_score(resonance_index, identity_score) * max(0.0, cfg.symmetry_gain)
    symmetry = _clamp01(symmetry)
    oscillation = compute_oscillation_score(previous_history, resonance_index)
    damping = compute_damping_score(oscillation) * max(0.0, cfg.damping_gain)
    damping = _clamp01(damping)
    resonance = compute_resonance_gain(
        symmetry,
        damping,
        resonance_index,
        gain=1.0,
    )
    collapse = compute_collapse_score(
        resonance,
        identity_score,
        intrusion_hint,
        gain=cfg.collapse_gain,
    )
    history = (*previous_history, _clamp01(resonance_index))[-max(1, int(cfg.history_window)) :]
    return PhaseDynamicsState(
        symmetry_score=symmetry,
        oscillation_score=oscillation,
        damping_score=damping,
        resonance_score=resonance,
        collapse_score=collapse,
        history=history,
    )


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))
