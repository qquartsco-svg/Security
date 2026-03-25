from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

from .contracts import AccessDecision, LiveSignalFrame, PolicyThresholds, ReMeltEvent
from .dynamics import evolve_phase_dynamics
from .phase_control import build_access_decision, should_re_melt
from .profile import IdentityProfile, score_frame
from .trust import NullTrustAnchor, TrustAnchorProtocol


@dataclass(frozen=True)
class MemoryPhaseKernelConfig:
    policy: PolicyThresholds = PolicyThresholds()
    require_trust_anchor: bool = False


class MemoryPhaseKernel:
    """
    Facade: trust anchor (optional) + live frame → AccessDecision.

    Extend by:
    - custom TrustAnchorProtocol implementations
    - enriching LiveSignalFrame via edge adapters
    - tuning PolicyThresholds / IdentityProfile.channel_weights
    """

    def __init__(
        self,
        config: MemoryPhaseKernelConfig | None = None,
        trust_anchor: TrustAnchorProtocol | None = None,
    ) -> None:
        self._config = config or MemoryPhaseKernelConfig()
        self._trust = trust_anchor or NullTrustAnchor()
        self._history_by_subject: Dict[str, Tuple[float, ...]] = {}

    @property
    def config(self) -> MemoryPhaseKernelConfig:
        return self._config

    def evaluate(
        self,
        profile: IdentityProfile,
        frame: LiveSignalFrame,
        *,
        identity_score_override: float | None = None,
    ) -> AccessDecision:
        if self._config.require_trust_anchor and not self._trust.session_ok():
            bundle = score_frame(
                profile,
                frame,
                identity_score_override=0.0,
                confidence=0.0,
                intrusion_hint=1.0,
            )
            return build_access_decision(bundle, self._config.policy, frame)

        bundle = score_frame(
            profile,
            frame,
            identity_score_override=identity_score_override,
        )
        previous_history = self._history_by_subject.get(profile.subject_id, ())
        dynamics = evolve_phase_dynamics(
            resonance_index=bundle.resonance_index,
            identity_score=bundle.identity_score,
            intrusion_hint=bundle.intrusion_hint,
            previous_history=previous_history,
        )
        self._history_by_subject[profile.subject_id] = dynamics.history
        enriched_bundle = type(bundle)(
            identity_score=bundle.identity_score,
            confidence=bundle.confidence,
            drift_hint=bundle.drift_hint,
            intrusion_hint=bundle.intrusion_hint,
            resonance_index=bundle.resonance_index,
            symmetry_score=dynamics.symmetry_score,
            oscillation_score=dynamics.oscillation_score,
            damping_score=dynamics.damping_score,
            collapse_score=dynamics.collapse_score,
        )
        return build_access_decision(enriched_bundle, self._config.policy, frame)

    def re_melt_check(
        self,
        decision: AccessDecision,
        frame: LiveSignalFrame,
    ) -> ReMeltEvent | None:
        """Return a re-melt event if intrusion or idle policy triggers."""
        if should_re_melt(decision.score_bundle, frame, self._config.policy):
            return ReMeltEvent(reason="intrusion_or_idle", force_liquid=True)
        return None
