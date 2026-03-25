from memory_phase_kernel import (
    DataPhase,
    IdentityProfile,
    LiveSignalFrame,
    MemoryPhaseKernel,
    MemoryPhaseSessionLoop,
    RawStateVault,
    VaultRecord,
    readings_from_simple_map,
)


def test_session_loop_materializes_and_remains_open_when_trusted() -> None:
    kernel = MemoryPhaseKernel()
    vault = RawStateVault(
        {
            "atom.state": VaultRecord(
                record_id="atom.state",
                sensitivity_tier="operational",
                sealed_payload={"omega": 0.9},
                masked_summary={"omega": "masked"},
            )
        }
    )
    loop = MemoryPhaseSessionLoop(kernel, vault)
    obs = loop.tick(
        IdentityProfile("user-1", {"typing": 1.0}),
        LiveSignalFrame(readings=readings_from_simple_map({"typing": 0.95})),
        record_ids=("atom.state",),
    )
    assert obs.decision.phase == DataPhase.FROZEN
    assert obs.materialized["atom.state"].interpretable is True
    assert obs.re_melt is None


def test_session_loop_re_melts_on_idle() -> None:
    kernel = MemoryPhaseKernel()
    vault = RawStateVault(
        {
            "athena.judgment": VaultRecord(
                record_id="athena.judgment",
                sensitivity_tier="personal",
                sealed_payload={"maat_score": 0.7},
                masked_summary={"maat_score": "masked"},
            )
        }
    )
    loop = MemoryPhaseSessionLoop(kernel, vault)
    obs = loop.tick(
        IdentityProfile("user-2", {"voice": 1.0}),
        LiveSignalFrame(readings=readings_from_simple_map({"voice": 0.95}), idle_seconds=2000.0),
        record_ids=("athena.judgment",),
    )
    assert obs.decision.phase == DataPhase.LIQUID
    assert obs.materialized["athena.judgment"].interpretable is False
    assert obs.re_melt is not None
