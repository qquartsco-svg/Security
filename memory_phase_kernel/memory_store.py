from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Dict, Mapping, Tuple

from .profile import IdentityProfile
from .resonance import normalize_channel_weights


@dataclass(frozen=True)
class MemoryObservation:
    """
    Minimal remembered-user update signal.

    This is intentionally small: it captures that memory can accumulate over time
    without pretending to already be a full biometric or cognitive model.
    """

    channel_id: str
    weight_delta: float
    confidence: float = 1.0


@dataclass(frozen=True)
class SubjectMemoryState:
    """Stored long-term state for one remembered subject."""

    profile: IdentityProfile
    trust_history: Tuple[float, ...] = field(default_factory=tuple)
    observation_count: int = 0
    last_identity_score: float | None = None


@dataclass(frozen=True)
class ForgettingPolicy:
    """
    Minimal memory hygiene policy.

    This keeps accumulation from becoming naive monotonic growth forever.
    """

    weight_decay: float = 0.04
    drift_penalty: float = 0.12
    min_weight_floor: float = 0.0
    trust_history_limit: int = 32


class IdentityMemoryStore:
    """
    Layer 1 scaffold for remembered-user accumulation.

    It stores channel-weight profiles and trust history without claiming to be the
    final learning engine.
    """

    def __init__(
        self,
        states: Mapping[str, SubjectMemoryState] | None = None,
        *,
        forgetting: ForgettingPolicy | None = None,
    ) -> None:
        self._states: Dict[str, SubjectMemoryState] = dict(states or {})
        self._forgetting = forgetting or ForgettingPolicy()

    def enroll(self, profile: IdentityProfile) -> SubjectMemoryState:
        state = SubjectMemoryState(profile=profile)
        self._states[profile.subject_id] = state
        return state

    def fetch(self, subject_id: str) -> SubjectMemoryState:
        return self._states[subject_id]

    def accumulate(
        self,
        subject_id: str,
        observations: Tuple[MemoryObservation, ...],
        *,
        observed_identity_score: float | None = None,
    ) -> SubjectMemoryState:
        current = self.fetch(subject_id)
        weights = dict(current.profile.channel_weights)

        for obs in observations:
            delta = max(0.0, float(obs.weight_delta)) * max(0.0, min(1.0, float(obs.confidence)))
            weights[obs.channel_id] = max(0.0, float(weights.get(obs.channel_id, 0.0)) + delta)

        normalized = normalize_channel_weights(weights)
        next_profile = IdentityProfile(
            subject_id=current.profile.subject_id,
            channel_weights=normalized,
            version=current.profile.version + 1,
        )

        history = current.trust_history
        if observed_identity_score is not None:
            history = (*history, max(0.0, min(1.0, float(observed_identity_score))))

        next_state = SubjectMemoryState(
            profile=next_profile,
            trust_history=history[-self._forgetting.trust_history_limit :],
            observation_count=current.observation_count + len(observations),
            last_identity_score=history[-1] if history else current.last_identity_score,
        )
        self._states[subject_id] = next_state
        return next_state

    def apply_forgetting(self, subject_id: str) -> SubjectMemoryState:
        """Apply gentle decay so old memory does not only grow forever."""
        current = self.fetch(subject_id)
        decay = max(0.0, min(1.0, self._forgetting.weight_decay))
        floor = max(0.0, self._forgetting.min_weight_floor)
        decayed = {
            channel_id: max(floor, float(weight) * (1.0 - decay))
            for channel_id, weight in current.profile.channel_weights.items()
        }
        normalized = normalize_channel_weights(decayed)
        next_state = replace(
            current,
            profile=IdentityProfile(
                subject_id=current.profile.subject_id,
                channel_weights=normalized,
                version=current.profile.version + 1,
            ),
        )
        self._states[subject_id] = next_state
        return next_state

    def apply_drift_penalty(self, subject_id: str, *, drift_hint: float) -> SubjectMemoryState:
        """
        Reduce recent trust when the live subject drifts too far from remembered patterns.
        """

        current = self.fetch(subject_id)
        penalty = max(0.0, min(1.0, self._forgetting.drift_penalty)) * max(0.0, min(1.0, drift_hint))
        history = current.trust_history
        if history:
            history = (*history[:-1], max(0.0, history[-1] - penalty))
        next_state = replace(
            current,
            trust_history=history[-self._forgetting.trust_history_limit :],
            last_identity_score=history[-1] if history else current.last_identity_score,
        )
        self._states[subject_id] = next_state
        return next_state
