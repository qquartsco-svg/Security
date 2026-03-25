"""
Memory Phase Kernel (MPK) — edge-oriented access & interpretability security module.

Public API: facade :class:`MemoryPhaseKernel`, contracts, resonance, trust protocol.
"""

from .contracts import (
    AccessDecision,
    AuditSurface,
    ChannelReading,
    DataPhase,
    IdentityScoreBundle,
    LiveSignalFrame,
    PolicyThresholds,
    ReMeltEvent,
    SensitivityTier,
)
from .dynamics import (
    PhaseDynamicsConfig,
    PhaseDynamicsState,
    compute_collapse_score,
    compute_damping_score,
    compute_oscillation_score,
    compute_resonance_gain,
    compute_symmetry_score,
    evolve_phase_dynamics,
)
from .memory_store import (
    ForgettingPolicy,
    IdentityMemoryStore,
    MemoryObservation,
    SubjectMemoryState,
)
from .kernel import MemoryPhaseKernel, MemoryPhaseKernelConfig
from .phase_control import phase_from_identity_score, should_re_melt, tiers_for_phase
from .phase_control import effective_identity_score
from .profile import ChannelSpec, IdentityProfile, readings_from_simple_map
from .raw_vault import MaterializedRecord, RawStateVault, VaultMaterializationPolicy, VaultRecord
from .resonance import compute_resonance_index, normalize_channel_weights
from .trust import NullTrustAnchor, TrustAnchorProtocol
from .integrations import parse_mak_access_bridge
from .integrations import (
    atom_result_to_vault_record,
    athena_result_to_vault_record,
    pharaoh_result_to_vault_record,
)
from .extensions import ChannelAdapter, KeystrokeRhythmStubAdapter
from .session_loop import MemoryPhaseSessionLoop, SessionObservation

__all__ = [
    "AccessDecision",
    "AuditSurface",
    "ChannelReading",
    "LiveSignalFrame",
    "ChannelAdapter",
    "ChannelSpec",
    "DataPhase",
    "PhaseDynamicsConfig",
    "PhaseDynamicsState",
    "ForgettingPolicy",
    "IdentityProfile",
    "IdentityMemoryStore",
    "IdentityScoreBundle",
    "KeystrokeRhythmStubAdapter",
    "MaterializedRecord",
    "MemoryObservation",
    "MemoryPhaseKernel",
    "MemoryPhaseKernelConfig",
    "MemoryPhaseSessionLoop",
    "NullTrustAnchor",
    "parse_mak_access_bridge",
    "PolicyThresholds",
    "RawStateVault",
    "VaultMaterializationPolicy",
    "ReMeltEvent",
    "SensitivityTier",
    "SessionObservation",
    "SubjectMemoryState",
    "TrustAnchorProtocol",
    "VaultRecord",
    "atom_result_to_vault_record",
    "athena_result_to_vault_record",
    "compute_resonance_index",
    "compute_collapse_score",
    "compute_damping_score",
    "compute_oscillation_score",
    "compute_resonance_gain",
    "compute_symmetry_score",
    "evolve_phase_dynamics",
    "effective_identity_score",
    "normalize_channel_weights",
    "pharaoh_result_to_vault_record",
    "readings_from_simple_map",
    "phase_from_identity_score",
    "should_re_melt",
    "tiers_for_phase",
]

__version__ = "0.1.8"
