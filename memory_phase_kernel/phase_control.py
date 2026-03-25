from __future__ import annotations

from .contracts import (
    AccessDecision,
    DataPhase,
    IdentityScoreBundle,
    LiveSignalFrame,
    PolicyThresholds,
    SensitivityTier,
)


def effective_identity_score(bundle: IdentityScoreBundle) -> float:
    """
    Blend direct identity and convergence/collapse.

    Identity score remains the main signal, but collapse_score now acts as a real
    convergence factor so the dynamics layer participates in access decisions.
    """

    if bundle.collapse_score is None:
        return bundle.identity_score
    collapse = max(0.0, min(1.0, bundle.collapse_score))
    ident = max(0.0, min(1.0, bundle.identity_score))
    return max(0.0, min(1.0, (ident + collapse) / 2.0))


def phase_from_identity_score(score: float, policy: PolicyThresholds) -> DataPhase:
    if score >= policy.frozen_threshold:
        return DataPhase.FROZEN
    if score >= policy.semi_threshold:
        return DataPhase.SEMI_FROZEN
    return DataPhase.LIQUID


def tiers_for_phase(phase: DataPhase) -> tuple[SensitivityTier, ...]:
    if phase == DataPhase.FROZEN:
        return ("public", "operational", "personal", "executive")
    if phase == DataPhase.SEMI_FROZEN:
        return ("public", "operational")
    return ("public",)


def build_access_decision(
    bundle: IdentityScoreBundle,
    policy: PolicyThresholds,
    live: LiveSignalFrame,
) -> AccessDecision:
    """Apply intrusion / idle caps on effective phase."""
    effective_score = effective_identity_score(bundle)
    phase = phase_from_identity_score(effective_score, policy)
    reason = "identity/collapse band" if bundle.collapse_score is not None else "identity_score band"

    if bundle.intrusion_hint >= policy.intrusion_re_melt_threshold:
        phase = DataPhase.LIQUID
        reason = "intrusion_hint >= threshold"
    elif live.idle_seconds >= policy.idle_re_melt_seconds:
        phase = DataPhase.LIQUID
        reason = "idle >= policy"

    capped = phase
    if bundle.drift_hint > 0.75 and capped == DataPhase.FROZEN:
        capped = DataPhase.SEMI_FROZEN
        reason = "high drift_hint caps at semi_frozen"

    return AccessDecision(
        phase=capped,
        allowed_tiers=tiers_for_phase(capped),
        reason=reason,
        score_bundle=bundle,
    )


def should_re_melt(
    bundle: IdentityScoreBundle,
    live: LiveSignalFrame,
    policy: PolicyThresholds,
) -> bool:
    if bundle.intrusion_hint >= policy.intrusion_re_melt_threshold:
        return True
    if live.idle_seconds >= policy.idle_re_melt_seconds:
        return True
    return False
