from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Mapping

from .contracts import AccessDecision, LiveSignalFrame, ReMeltEvent
from .kernel import MemoryPhaseKernel
from .profile import IdentityProfile
from .raw_vault import MaterializedRecord, RawStateVault


@dataclass(frozen=True)
class SessionObservation:
    """
    One observer-loop tick.

    The loop ties together:
    - remembered-user evaluation
    - vault materialization
    - optional re-melt signal
    """

    decision: AccessDecision
    materialized: Mapping[str, MaterializedRecord]
    re_melt: ReMeltEvent | None


class MemoryPhaseSessionLoop:
    """Minimal observer/session loop for MPK-backed access materialization."""

    def __init__(self, kernel: MemoryPhaseKernel, vault: RawStateVault) -> None:
        self._kernel = kernel
        self._vault = vault

    def tick(
        self,
        profile: IdentityProfile,
        frame: LiveSignalFrame,
        *,
        record_ids: tuple[str, ...],
        identity_score_override: float | None = None,
    ) -> SessionObservation:
        decision = self._kernel.evaluate(
            profile,
            frame,
            identity_score_override=identity_score_override,
        )
        materialized: Dict[str, MaterializedRecord] = {
            record_id: self._vault.materialize(record_id, decision) for record_id in record_ids
        }
        re_melt = self._kernel.re_melt_check(decision, frame)
        return SessionObservation(decision=decision, materialized=materialized, re_melt=re_melt)
