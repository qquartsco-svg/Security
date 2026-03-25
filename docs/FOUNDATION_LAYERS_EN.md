> **Korean (canonical):** [FOUNDATION_LAYERS.md](FOUNDATION_LAYERS.md)

# MPK Foundation Layers

This document explains `MemoryPhase_Kernel` not as a finished security product,
but as a **foundational layer stack** that can grow over time.

The core idea is simple:

- Data is liquid by default.
- When the local agent becomes confident that the current subject matches the remembered user, data becomes frozen enough to read meaningfully.
- When the user leaves or trust collapses, the state melts again.

In other words, MPK does not merely “open files.”
It controls whether information becomes **interpretable in a user-specific way**.

## Layer overview

### Layer 0 — Raw State Vault

Role:

- Store personal data, operational logs, and judgment outputs in a liquid-by-default form
- Separate raw state from interpretable state
- Keep data present without exposing personal meaning by default

Current status:

- Real storage and decrypt boundaries are still external
- But `raw_vault.py` now provides a minimal scaffold inside the package
- materialization may now also require a sufficient `collapse_score`

### Layer 1 — Identity Memory Engine

Role:

- Long-term memory of the user
- Channel importance, long-term tendencies, and trust history

Example channels:

- typing
- voice
- face
- language
- gaze
- device

Current status:

- `IdentityProfile` provides the minimal structure
- `memory_store.py` now provides a minimal accumulation scaffold
- Currently this is a weight-slot model, not a full learning memory engine
- minimal `forgetting` and `drift penalty` rules are now included

### Layer 2 — Continuous Identity Scoring

Role:

- Compare live input against long-term memory
- Estimate how much the current subject matches the remembered user

Current status:

- `compute_resonance_index()`
- `score_frame()`

Outputs:

- `resonance_index`
- `identity_score`
- quality / drift / intrusion hints

### Layer 3 — Access Dynamics Layer

Role:

- model how stored memory and live input converge over time
- express the flow `symmetry -> oscillation -> damping -> resonance -> collapse`
- provide a more stable continuous-authentication path than a single instant score

Current status:

- `dynamics.py`
- `compute_symmetry_score()`
- `compute_oscillation_score()`
- `compute_damping_score()`
- `compute_resonance_gain()`
- `compute_collapse_score()`
- `evolve_phase_dynamics()`

Interpretation:

- symmetry: structural alignment between remembered user and live subject
- oscillation: recent fluctuation
- damping: reduction of noise
- resonance: stable remembered-user alignment
- collapse: convergence strong enough to drive access decisions

### Layer 4 — Phase Transition Controller

Role:

- Move between `liquid / semi_frozen / frozen`
- Demote on intrusion, idleness, or drift

Current status:

- `phase_from_identity_score()`
- `build_access_decision()`
- `should_re_melt()`

What this layer really decides is:

- not only “should this be shown?”
- but **“should this become meaningfully ordered?”**

### Layer 5 — Access Kernel

Role:

- Map phases to sensitivity tiers
- Decide how far interpretation is allowed to go

Current status:

- `AccessDecision.phase`
- `AccessDecision.allowed_tiers`

Expected downstream targets:

- Atom state summaries
- Athena analysis outputs
- Pharaoh reports
- operational logs
- personal memory

### Layer 6 — Audit / Forgetting / Re-melt

Role:

- Re-melt on session end, user departure, intrusion, or idleness
- Close interpretation windows
- Discard keys and leave audit traces

Current status:

- `ReMeltEvent`
- `should_re_melt()`

Still missing:

- full audit chain
- key destruction policy
- long-term forgetting / relearning policy

## What MPK currently covers

Today `MemoryPhase_Kernel` mainly covers:

- Layer 1: minimal long-term memory slots
- Layer 1.5: minimal accumulation scaffold (`IdentityMemoryStore`)
- Layer 2: resonance / identity scoring
- Layer 3: access dynamics (`symmetry -> oscillation -> damping -> resonance -> collapse`)
- Layer 4: phase transition control
- Layer 5: sensitivity-tier allowance
- Layer 5 preparation scaffold (`RawStateVault`)
- Layer 6: re-melt hooks

So MPK is not yet the full memory-based security stack.
It is the **core decision kernel** inside that future stack.

## Principles for future expansion

1. Prefer storing features / embeddings / summaries over raw data
2. Keep phase decisions separate from actual decrypt/render layers
3. Preserve the trust-anchor slot
4. Separate audit from UX
5. Let memory accumulate, but guard against overfitting with drift policy
6. Treat this as strengthened continuous authentication, not immediate password elimination

## One-line definition

**MPK is the foundational access kernel that decides whether data may become ice-like and interpretable for the remembered user.**
