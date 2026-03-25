from memory_phase_kernel import (
    DataPhase,
    IdentityScoreBundle,
    LiveSignalFrame,
    MemoryPhaseKernel,
    MemoryPhaseKernelConfig,
    PolicyThresholds,
    effective_identity_score,
)
from memory_phase_kernel import IdentityProfile, readings_from_simple_map


def test_kernel_frozen_band() -> None:
    k = MemoryPhaseKernel()
    p = IdentityProfile("u1", {"typing": 1.0})
    frame = LiveSignalFrame(readings=readings_from_simple_map({"typing": 0.9}))
    d = k.evaluate(p, frame)
    assert d.phase == DataPhase.FROZEN
    assert "executive" in d.allowed_tiers


def test_trust_anchor_required_blocks() -> None:
    class BadAnchor:
        def anchor_subject_id(self) -> str:
            return "x"

        def session_ok(self) -> bool:
            return False

    k = MemoryPhaseKernel(
        MemoryPhaseKernelConfig(require_trust_anchor=True),
        trust_anchor=BadAnchor(),
    )
    p = IdentityProfile("u1", {"typing": 1.0})
    frame = LiveSignalFrame(readings=readings_from_simple_map({"typing": 1.0}))
    d = k.evaluate(p, frame)
    assert d.phase == DataPhase.LIQUID


def test_re_melt_idle() -> None:
    policy = PolicyThresholds(idle_re_melt_seconds=10.0)
    k = MemoryPhaseKernel(MemoryPhaseKernelConfig(policy=policy))
    p = IdentityProfile("u1", {"a": 1.0})
    frame = LiveSignalFrame(readings=readings_from_simple_map({"a": 1.0}), idle_seconds=20.0)
    d = k.evaluate(p, frame)
    assert d.phase == DataPhase.LIQUID


def test_effective_identity_score_blends_collapse() -> None:
    bundle = IdentityScoreBundle(
        identity_score=0.9,
        confidence=1.0,
        drift_hint=0.0,
        intrusion_hint=0.0,
        resonance_index=0.9,
        collapse_score=0.2,
    )
    assert effective_identity_score(bundle) == 0.55


def test_kernel_uses_dynamics_in_real_decision_path() -> None:
    k = MemoryPhaseKernel()
    p = IdentityProfile("volatile-user", {"typing": 1.0})
    volatile_scores = (0.95, 0.1, 0.95, 0.1, 0.95)
    for score in volatile_scores:
        frame = LiveSignalFrame(readings=readings_from_simple_map({"typing": score}))
        decision = k.evaluate(p, frame, identity_score_override=0.9)

    assert decision.score_bundle.collapse_score is not None
    assert decision.score_bundle.oscillation_score is not None
    assert decision.phase != DataPhase.FROZEN
