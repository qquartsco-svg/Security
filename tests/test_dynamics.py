from memory_phase_kernel import (
    PhaseDynamicsConfig,
    compute_collapse_score,
    compute_damping_score,
    compute_oscillation_score,
    compute_resonance_gain,
    compute_symmetry_score,
    evolve_phase_dynamics,
)


def test_symmetry_is_high_when_resonance_and_identity_match() -> None:
    assert compute_symmetry_score(0.9, 0.9) == 1.0


def test_oscillation_grows_with_recent_span() -> None:
    score = compute_oscillation_score((0.2, 0.8), 0.4)
    assert score > 0.0


def test_damping_is_inverse_of_oscillation() -> None:
    assert compute_damping_score(0.25) == 0.75


def test_resonance_gain_requires_symmetry_and_damping() -> None:
    gain = compute_resonance_gain(0.9, 0.8, 0.95)
    assert 0.0 < gain <= 1.0


def test_collapse_is_suppressed_by_intrusion() -> None:
    safe = compute_collapse_score(0.9, 0.9, 0.0)
    blocked = compute_collapse_score(0.9, 0.9, 1.0)
    assert blocked < safe


def test_evolve_phase_dynamics_tracks_history_and_scores() -> None:
    state = evolve_phase_dynamics(
        resonance_index=0.88,
        identity_score=0.9,
        intrusion_hint=0.05,
        previous_history=(0.81, 0.84),
        config=PhaseDynamicsConfig(history_window=4),
    )
    assert len(state.history) == 3
    assert state.symmetry_score > 0.0
    assert state.damping_score >= 0.0
    assert state.collapse_score > 0.0
