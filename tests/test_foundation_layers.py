from memory_phase_kernel import (
    AccessDecision,
    DataPhase,
    ForgettingPolicy,
    IdentityMemoryStore,
    IdentityProfile,
    IdentityScoreBundle,
    MemoryObservation,
    RawStateVault,
    VaultMaterializationPolicy,
    VaultRecord,
)


def _decision(*tiers: str, phase: DataPhase = DataPhase.FROZEN) -> AccessDecision:
    return AccessDecision(
        phase=phase,
        allowed_tiers=tiers,
        reason="test",
        score_bundle=IdentityScoreBundle(
            identity_score=1.0,
            confidence=1.0,
            drift_hint=0.0,
            intrusion_hint=0.0,
            resonance_index=1.0,
            collapse_score=1.0,
        ),
    )


def test_raw_vault_materializes_allowed_record() -> None:
    vault = RawStateVault()
    vault.put(
        VaultRecord(
            record_id="atom-summary",
            sensitivity_tier="operational",
            sealed_payload={"omega": 0.91, "verdict": "stable"},
            masked_summary={"omega": "masked"},
        )
    )
    materialized = vault.materialize("atom-summary", _decision("public", "operational"))
    assert materialized.interpretable is True
    assert materialized.presented_payload == {"omega": 0.91, "verdict": "stable"}


def test_raw_vault_liquid_keeps_payload_masked() -> None:
    vault = RawStateVault(
        {
            "pharaoh-report": VaultRecord(
                record_id="pharaoh-report",
                sensitivity_tier="executive",
                sealed_payload={"title": "royal"},
                masked_summary={"title": "hidden"},
            )
        }
    )
    materialized = vault.materialize(
        "pharaoh-report",
        _decision("public", "operational", phase=DataPhase.LIQUID),
    )
    assert materialized.interpretable is False
    assert materialized.presented_payload == {"title": "hidden"}


def test_raw_vault_respects_collapse_threshold() -> None:
    vault = RawStateVault(
        {
            "personal-log": VaultRecord(
                record_id="personal-log",
                sensitivity_tier="personal",
                sealed_payload={"note": "visible"},
                masked_summary={"note": "masked"},
            )
        },
        policy=VaultMaterializationPolicy(collapse_threshold=0.5),
    )
    decision = AccessDecision(
        phase=DataPhase.FROZEN,
        allowed_tiers=("public", "operational", "personal"),
        reason="test",
        score_bundle=IdentityScoreBundle(
            identity_score=0.9,
            confidence=1.0,
            drift_hint=0.0,
            intrusion_hint=0.0,
            resonance_index=0.9,
            collapse_score=0.2,
        ),
    )
    materialized = vault.materialize("personal-log", decision)
    assert materialized.interpretable is False
    assert materialized.presented_payload == {"note": "masked"}


def test_memory_store_accumulates_and_normalizes_weights() -> None:
    store = IdentityMemoryStore()
    store.enroll(IdentityProfile("user-1", {"typing": 1.0}))
    state = store.accumulate(
        "user-1",
        (
            MemoryObservation("voice", 0.5, confidence=1.0),
            MemoryObservation("typing", 0.5, confidence=0.5),
        ),
        observed_identity_score=0.88,
    )
    assert state.profile.version == 2
    assert state.observation_count == 2
    assert abs(sum(state.profile.channel_weights.values()) - 1.0) < 1e-9
    assert state.last_identity_score == 0.88


def test_memory_store_fetch_returns_latest_state() -> None:
    store = IdentityMemoryStore()
    store.enroll(IdentityProfile("user-2", {"voice": 1.0}))
    store.accumulate("user-2", (MemoryObservation("language", 1.0),))
    latest = store.fetch("user-2")
    assert latest.profile.version == 2
    assert "language" in latest.profile.channel_weights


def test_memory_store_apply_forgetting_decays_weights() -> None:
    store = IdentityMemoryStore(forgetting=ForgettingPolicy(weight_decay=0.1))
    store.enroll(IdentityProfile("user-3", {"typing": 0.7, "voice": 0.3}))
    decayed = store.apply_forgetting("user-3")
    assert decayed.profile.version == 2
    assert abs(sum(decayed.profile.channel_weights.values()) - 1.0) < 1e-9


def test_memory_store_apply_drift_penalty_reduces_recent_trust() -> None:
    store = IdentityMemoryStore(forgetting=ForgettingPolicy(drift_penalty=0.2))
    store.enroll(IdentityProfile("user-4", {"typing": 1.0}))
    store.accumulate("user-4", (MemoryObservation("typing", 0.1),), observed_identity_score=0.9)
    penalized = store.apply_drift_penalty("user-4", drift_hint=0.5)
    assert penalized.last_identity_score == 0.8
