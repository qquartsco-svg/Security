from __future__ import annotations

from typing import Any, Mapping, Optional, TypedDict


class MakAccessBridgeDict(TypedDict, total=False):
    """Shape of ``evidence["mak_access_bridge"]`` from FirstOrder pipeline."""

    mak_sensitivity_tier: str
    mak_evidence_ref: str
    operational_posture_stage: str


def parse_mak_access_bridge(evidence: Mapping[str, Any]) -> Optional[MakAccessBridgeDict]:
    """
    Extract MPK-oriented fields from a FirstOrder (or compatible) ``evidence`` map.

    Returns None if the host did not attach a bridge payload.
    """
    raw = evidence.get("mak_access_bridge")
    if not isinstance(raw, dict):
        return None
    out: MakAccessBridgeDict = {}
    if "mak_sensitivity_tier" in raw and isinstance(raw["mak_sensitivity_tier"], str):
        out["mak_sensitivity_tier"] = raw["mak_sensitivity_tier"]
    if "mak_evidence_ref" in raw and isinstance(raw["mak_evidence_ref"], str):
        out["mak_evidence_ref"] = raw["mak_evidence_ref"]
    if "operational_posture_stage" in raw and isinstance(
        raw["operational_posture_stage"], str
    ):
        out["operational_posture_stage"] = raw["operational_posture_stage"]
    return out or None
