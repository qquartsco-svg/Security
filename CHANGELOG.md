# Changelog

## 0.1.10 - 2026-03-25

- Tightened README pair around implementation boundaries:
  - clarified `resonance_index` vs `identity_score`
  - added concrete `liquid / semi_frozen / frozen` examples
  - clarified that `materialize` is not the same as real cryptographic reveal
  - defined `implemented` vs `foundational` status labels

## 0.1.9 - 2026-03-25

- Added `docs/GITHUB_OVERVIEW.md` with suggested repository tagline/description/onboarding sequence.
- Added `scripts/verify_signature.py` for local SHA-256 manifest verification.
- Expanded README pair with explicit integrity verification instructions.

## 0.1.8 - 2026-03-25

- Expanded README pair with:
  - why the concept is unfamiliar
  - practical use cases
  - comparison to password / biometric / behavioral security
  - clearer layer-growth path
  - current implementation table
- Added `docs/SECURITY_MODEL.md` and `SECURITY_MODEL_EN.md`.
- Added repository integrity docs:
  - `BLOCKCHAIN_INFO.md`
  - `PHAM_BLOCKCHAIN_LOG.md`
- Prepared the package for release/push to the `Security` repository with explicit explanation of concept, expansion path, and integrity model.

## 0.1.7 - 2026-03-25

- Added `integrations/governance_vaults.py`:
  - `atom_result_to_vault_record()`
  - `athena_result_to_vault_record()`
  - `pharaoh_result_to_vault_record()`
- Added `session_loop.py`:
  - `MemoryPhaseSessionLoop`
  - `SessionObservation`
- Added regression tests for governance-to-vault bridges and the session loop.
- Updated docs to show that MPK now has a minimal operational bridge and observer loop.

## 0.1.6 - 2026-03-25

- Added `VaultMaterializationPolicy` so `RawStateVault` can require both phase eligibility and sufficient `collapse_score`.
- Added `ForgettingPolicy` plus:
  - `IdentityMemoryStore.apply_forgetting()`
  - `IdentityMemoryStore.apply_drift_penalty()`
- Added regression tests for collapse-gated materialization and memory decay / drift handling.
- Updated docs to clarify that memory should strengthen over time without becoming naive monotonic accumulation.

## 0.1.5 - 2026-03-25

- Wired the dynamics layer into real access decisions.
- Added `collapse_score`, `symmetry_score`, `oscillation_score`, and `damping_score` to `IdentityScoreBundle`.
- `MemoryPhaseKernel.evaluate()` now evolves per-subject dynamics history across evaluations.
- `phase_control.build_access_decision()` now blends `identity_score` and `collapse_score` through `effective_identity_score()`.
- Added regression tests proving the dynamics layer affects the production decision path.

## 0.1.4 - 2026-03-25

- Added `dynamics.py` as the mathematical access-dynamics layer for:
  - symmetry
  - oscillation
  - damping
  - resonance
  - collapse
- Added:
  - `PhaseDynamicsConfig`
  - `PhaseDynamicsState`
  - `evolve_phase_dynamics()`
- Exported the new dynamics API from the package root.
- Added regression tests for the new convergence layer.
- Updated README and architecture docs to place the dynamics layer between identity scoring and phase transition.

## 0.1.3 - 2026-03-25

- Added `raw_vault.py` as a minimal Layer 0 scaffold:
  - `VaultRecord`
  - `MaterializedRecord`
  - `RawStateVault`
- Added `memory_store.py` as a minimal Layer 1 scaffold:
  - `MemoryObservation`
  - `SubjectMemoryState`
  - `IdentityMemoryStore`
- Exported the new foundational types from the package root.
- Added regression tests for vault materialization and memory accumulation.
- Updated docs to state that these are scaffolds for the broader memory-based security stack.

## 0.1.2 - 2026-03-25

- Clarified MPK as a **foundational memory-based access kernel**, not a complete security product.
- Added `docs/FOUNDATION_LAYERS.md` and `FOUNDATION_LAYERS_EN.md` to define the expandable layer stack:
  Raw State Vault → Identity Memory → Continuous Scoring → Phase Transition → Access Kernel → Audit/Re-melt.
- Expanded README pair with:
  - plain-language water/ice explanation
  - implemented vs not-yet-implemented boundary
  - current layer coverage
- Updated architecture doc to state current implementation coverage explicitly.

## 0.1.1 - 2026-03-25

- `extensions.ChannelAdapter` protocol + `KeystrokeRhythmStubAdapter` demo.
- `integrations.parse_mak_access_bridge` for FirstOrder `evidence["mak_access_bridge"]`.
- FirstOrder `run_force_assessment` emits `mak_access_bridge` (no hard dependency on this package).

## 0.1.0 - 2026-03-25

- Initial **standalone** package `memory_phase_kernel` under `_staging/MemoryPhase_Kernel/`.
- Core: `contracts`, `resonance` (Ω_res), `profile`, `phase_control`, `trust` protocol, `MemoryPhaseKernel` facade.
- `extensions/` namespace for edge adapters.
- Documentation: `docs/ARCHITECTURE.md` / `ARCHITECTURE_EN.md`, `README` pair.
- Tests: `tests/test_resonance.py`, `tests/test_kernel.py`.
