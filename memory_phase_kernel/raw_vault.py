from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, Mapping

from .contracts import AccessDecision, DataPhase, SensitivityTier


@dataclass(frozen=True)
class VaultRecord:
    """
    Layer 0 placeholder: keep data opaque by default and materialize only by phase.

    Real encryption, keys, and storage backends remain external.
    """

    record_id: str
    sensitivity_tier: SensitivityTier
    sealed_payload: object
    masked_summary: object | None = None
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class MaterializedRecord:
    """What a host app may expose after applying an MPK access decision."""

    record_id: str
    sensitivity_tier: SensitivityTier
    phase: DataPhase
    interpretable: bool
    presented_payload: object | None
    metadata: Mapping[str, str] = field(default_factory=dict)


@dataclass(frozen=True)
class VaultMaterializationPolicy:
    """
    Minimal policy for turning phase decisions into actual readable state.

    `collapse_threshold` lets the vault require that convergence is not only
    phase-qualified but also sufficiently stabilized.
    """

    collapse_threshold: float = 0.35
    allow_semi_frozen_materialization: bool = True


class RawStateVault:
    """
    Minimal Layer 0 scaffold for the water/ice metaphor.

    It does not claim to be a production vault. It only gives future integrations
    a stable API surface for phase-bound materialization.
    """

    def __init__(
        self,
        records: Mapping[str, VaultRecord] | None = None,
        *,
        policy: VaultMaterializationPolicy | None = None,
    ) -> None:
        self._records: Dict[str, VaultRecord] = dict(records or {})
        self._policy = policy or VaultMaterializationPolicy()

    def put(self, record: VaultRecord) -> None:
        self._records[record.record_id] = record

    def get(self, record_id: str) -> VaultRecord:
        return self._records[record_id]

    def materialize(self, record_id: str, decision: AccessDecision) -> MaterializedRecord:
        record = self.get(record_id)
        allowed = record.sensitivity_tier in decision.allowed_tiers
        phase_ok = decision.phase == DataPhase.FROZEN or (
            self._policy.allow_semi_frozen_materialization and decision.phase == DataPhase.SEMI_FROZEN
        )
        collapse = decision.score_bundle.collapse_score
        collapse_ok = collapse is None or collapse >= self._policy.collapse_threshold
        interpretable = phase_ok and allowed and collapse_ok
        payload = record.sealed_payload if interpretable else record.masked_summary
        return MaterializedRecord(
            record_id=record.record_id,
            sensitivity_tier=record.sensitivity_tier,
            phase=decision.phase,
            interpretable=interpretable,
            presented_payload=payload,
            metadata=record.metadata,
        )
