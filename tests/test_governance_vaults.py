from memory_phase_kernel import (
    atom_result_to_vault_record,
    athena_result_to_vault_record,
    pharaoh_result_to_vault_record,
)


def test_atom_result_to_vault_record() -> None:
    record = atom_result_to_vault_record({"mode": "guard", "warning_signal": 0.42})
    assert record.record_id == "atom.state"
    assert record.sensitivity_tier == "operational"
    assert record.masked_summary["mode"] == "guard"


def test_athena_result_to_vault_record() -> None:
    record = athena_result_to_vault_record({"crisis_level": "주의", "maat_score": 0.61})
    assert record.record_id == "athena.judgment"
    assert record.sensitivity_tier == "personal"
    assert record.masked_summary["crisis_level"] == "주의"


def test_pharaoh_result_to_vault_record() -> None:
    record = pharaoh_result_to_vault_record({"decision": "health_campaign", "priority": "high"})
    assert record.record_id == "pharaoh.report"
    assert record.sensitivity_tier == "executive"
    assert record.masked_summary["decision"] == "health_campaign"
