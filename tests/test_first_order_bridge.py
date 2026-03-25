from memory_phase_kernel import parse_mak_access_bridge


def test_parse_mak_access_bridge() -> None:
    ev = {
        "mak_access_bridge": {
            "mak_sensitivity_tier": "executive",
            "mak_evidence_ref": "abc123",
            "operational_posture_stage": "positive",
        }
    }
    b = parse_mak_access_bridge(ev)
    assert b is not None
    assert b["mak_sensitivity_tier"] == "executive"
    assert b["mak_evidence_ref"] == "abc123"
    assert b["operational_posture_stage"] == "positive"


def test_parse_missing() -> None:
    assert parse_mak_access_bridge({}) is None
