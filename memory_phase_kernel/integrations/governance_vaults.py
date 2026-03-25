from __future__ import annotations

from typing import Any, Mapping

from ..contracts import SensitivityTier
from ..raw_vault import VaultRecord


def atom_result_to_vault_record(
    atom_state: Mapping[str, Any],
    *,
    record_id: str = "atom.state",
    sensitivity_tier: SensitivityTier = "operational",
) -> VaultRecord:
    """Map an Atom-style state/result dict into a vault record."""

    summary = {
        "mode": atom_state.get("mode", "masked"),
        "warning_signal": atom_state.get("warning_signal", "masked"),
    }
    return VaultRecord(
        record_id=record_id,
        sensitivity_tier=sensitivity_tier,
        sealed_payload=dict(atom_state),
        masked_summary=summary,
        metadata={"source": "atom", "kind": "state"},
    )


def athena_result_to_vault_record(
    athena_result: Mapping[str, Any],
    *,
    record_id: str = "athena.judgment",
    sensitivity_tier: SensitivityTier = "personal",
) -> VaultRecord:
    """Map an Athena-style analysis/judgment dict into a vault record."""

    summary = {
        "crisis_level": athena_result.get("crisis_level", "masked"),
        "maat_score": athena_result.get("maat_score", "masked"),
    }
    return VaultRecord(
        record_id=record_id,
        sensitivity_tier=sensitivity_tier,
        sealed_payload=dict(athena_result),
        masked_summary=summary,
        metadata={"source": "athena", "kind": "judgment"},
    )


def pharaoh_result_to_vault_record(
    pharaoh_result: Mapping[str, Any],
    *,
    record_id: str = "pharaoh.report",
    sensitivity_tier: SensitivityTier = "executive",
) -> VaultRecord:
    """Map a Pharaoh-style decree/report dict into a vault record."""

    summary = {
        "decision": pharaoh_result.get("decision", "masked"),
        "priority": pharaoh_result.get("priority", "masked"),
    }
    return VaultRecord(
        record_id=record_id,
        sensitivity_tier=sensitivity_tier,
        sealed_payload=dict(pharaoh_result),
        masked_summary=summary,
        metadata={"source": "pharaoh", "kind": "report"},
    )
