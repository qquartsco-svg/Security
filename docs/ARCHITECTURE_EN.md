> **Korean (canonical):** [ARCHITECTURE.md](ARCHITECTURE.md)

# Memory Phase Kernel (MPK) — Architecture Canon

**Package root**: `_staging/MemoryPhase_Kernel/`  
**Import name**: `memory_phase_kernel`  
**Version**: keep in sync with `VERSION` and `pyproject.toml`

**Concept canon (portfolio meta)**: [design_workspace/MEMORY_ACCESS_KERNEL_DESIGN_EN.md](../design_workspace/MEMORY_ACCESS_KERNEL_DESIGN_EN.md). **This document** focuses on the **shipping module’s boundaries and extension contracts**.
**Foundation layers**: [FOUNDATION_LAYERS_EN.md](FOUNDATION_LAYERS_EN.md) — explains which part of the broader memory-based security stack MPK actually implements today.

---

## 1. Purpose and non-goals

### 1.1 Purpose

- **Edge-AI-friendly** access/interpretability kernel: combine on-device observations with a **long-term profile** to move data across **liquid / semi_frozen / frozen** phases.
- **Isolated from operational cores**: Atom/Athena/Pharaoh/FirstOrder **produce** artifacts; MPK only decides **who reads which sensitivity tier in which phase** (artifacts unchanged).
- **Extensible**: core is **stdlib-only**; cameras/voice/keystroke live in `extensions/` or separate packages feeding `LiveSignalFrame`.

### 1.2 Non-goals (v0.1)

- Built-in crypto (AES/GCM, HSM) — stays behind **TrustAnchorProtocol**.
- Built-in ML inference — only **per-channel match_score** injection.
- Claiming passwords are obsolete — **trust anchor slot** remains in API and docs.

---

## 2. Concept mapping

| Narrative | MPK type / module |
|-----------|-------------------|
| Water (non-interpretable) | `DataPhase.LIQUID` |
| Ice (interpretation window) | `DataPhase.FROZEN` (+ `SEMI_FROZEN`) |
| Resonance | `resonance.compute_resonance_index` → `IdentityScoreBundle.resonance_index` |
| Memory (weights) | `IdentityProfile.channel_weights` |
| Trust root | `TrustAnchorProtocol` / `NullTrustAnchor` |
| Re-melt | `ReMeltEvent` + `should_re_melt` policy |

---

## 2.5 Current implementation coverage

MPK does not implement the full memory-based security system by itself.

- Strongly implemented today: long-term memory slots, resonance scoring, access dynamics, phase transition, allowed-tier decisions
- Present as hooks or scaffolds today: re-melt hooks, trust-anchor slot, `RawStateVault`, `IdentityMemoryStore`
- Still external: real raw-state vault storage, actual decrypt/masking/render layer, learned long-term memory engine, full audit chain

So MPK should be read as a **decision kernel**, not as the complete storage or biometric inference product.

---

## 3. Module layout

```
memory_phase_kernel/
  contracts.py      # phases, tiers, frames, thresholds, audit surfaces
  resonance.py      # Ω_res
  profile.py        # IdentityProfile, score_frame
  phase_control.py  # phase/tier + re-melt
  trust.py          # TrustAnchorProtocol
  kernel.py         # MemoryPhaseKernel facade
  extensions/       # adapter namespace
```

**Dependency rule**: `kernel` → `profile` → `resonance` / `contracts`; `trust` is protocol-only.

---

## 4. Runtime dataflow

1. Edge adapters build `LiveSignalFrame` from `ChannelReading` tuples.  
2. `IdentityProfile` supplies channel weights.  
3. `score_frame()` computes `resonance_index` and `identity_score` (overridable).  
4. `evolve_phase_dynamics()` computes the `symmetry -> oscillation -> damping -> resonance -> collapse` state.  
5. `build_access_decision()` applies `PolicyThresholds` using both `identity_score` and `collapse_score`; intrusion/idle forces liquid.  
6. App layer performs conditional decrypt/UI masking **outside** MPK.

---

## 5. Commercial / extension guide

### 5.1 Tunables

- `PolicyThresholds`  
- `MemoryPhaseKernelConfig.require_trust_anchor` (recommended True in production)  
- `IdentityProfile.version` for enrollment migrations  

### 5.2 Extension points

| Need | How |
|------|-----|
| New sensor | Add `ChannelReading` + profile weight |
| Edge adapter | Implement `extensions.ChannelAdapter` → `capture()` returns `LiveSignalFrame` (see `KeystrokeRhythmStubAdapter`) |
| Anchor | Implement `TrustAnchorProtocol` |
| Maturity schedule | External policy engine updates thresholds |
| Audit | App persists logs using `AuditSurface` hints |
| FirstOrder bridge | `integrations.parse_mak_access_bridge(evidence)` intersects with `AccessDecision.allowed_tiers` |

Added foundational scaffolds:

- `RawStateVault` now exposes a `phase + collapse_score` based materialization path
- `IdentityMemoryStore` now exposes `apply_forgetting()` / `apply_drift_penalty()`
- `integrations.governance_vaults` maps Atom/Athena/Pharaoh outputs into `VaultRecord`
- `MemoryPhaseSessionLoop` provides a minimal `entry -> materialize -> re-melt` observer loop

### 5.3 Distribution

- `pip install -e .` or wheel to private index; **no native deps** in core.

---

## 6. Optional operational hooks

**FirstOrder (v0.1.2+)** embeds in `evidence`:

```json
"mak_access_bridge": {
  "mak_sensitivity_tier": "operational",
  "mak_evidence_ref": "<blackbox head hash>",
  "operational_posture_stage": "neutral"
}
```

Parser: `parse_mak_access_bridge(evidence)`.

| Field | Role |
|-------|------|
| `mak_sensitivity_tier` | Suggested data sensitivity tier from the host |
| `mak_evidence_ref` | Audit pointer (e.g. blackbox head) |
| `operational_posture_stage` | Posture used when tier was auto-mapped |

The MPK **decision core** ignores these; an **app bridge** intersects them with `AccessDecision.allowed_tiers`.

---

## 7. Security notes

- `NullTrustAnchor` is **dev-only**.  
- Spoofing mitigated via per-channel `quality` + anchor + multi-channel diversity.  
- Log frozen transitions for internal audit separately from UX minimal traces.

---

## 8. Package roadmap

- v0.2: optional `ChannelAdapter` protocol + sample adapter  
- v0.3: optional YAML policy loader  
- v1.0: API stability + security review checklist

---

*v0.1.2 — update with Korean canon and changelogs when editing.*
