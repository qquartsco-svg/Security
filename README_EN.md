> **Korean (canonical):** [README.md](README.md)

# MemoryPhase_Kernel (MPK)

**Memory Phase Kernel** — a **standalone, edge-AI-oriented** package for **memory/resonance-based access and interpretability**. Data defaults to **liquid** (non-interpretable to the viewer); trusted channel alignment may allow **semi_frozen → frozen** interpretation windows.

In plain language:

- Data flows like water by default and does not immediately reveal personal meaning.
- A local AI agent asks, “How much does the current subject match the user I remember?”
- If the match becomes strong enough, data becomes ice-like: ordered and interpretable for that user.
- If the user leaves or trust falls, the data melts again and the interpretation window closes.

- **Version**: `VERSION` / `pyproject.toml`  
- **Dependencies**: core is **stdlib-only** (edge/deployment friendly)  
- **Architecture canon**: [docs/ARCHITECTURE_EN.md](docs/ARCHITECTURE_EN.md)  
- **Foundation layers**: [docs/FOUNDATION_LAYERS_EN.md](docs/FOUNDATION_LAYERS_EN.md)
- **Security model**: [docs/SECURITY_MODEL_EN.md](docs/SECURITY_MODEL_EN.md)
- **Integrity / signature**: [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md), [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md), `SIGNATURE.sha256`
- **GitHub overview draft**: [docs/GITHUB_OVERVIEW.md](docs/GITHUB_OVERVIEW.md)
- **Concept portfolio doc**: [design_workspace/MEMORY_ACCESS_KERNEL_DESIGN_EN.md](../design_workspace/MEMORY_ACCESS_KERNEL_DESIGN_EN.md)

## What this package does / does not do

This package is not a complete memory-based security product.
It is the **foundational kernel** inside that future system.

What it does today:

- compare long-term profile against live signals
- compute resonance and identity scores
- compute minimal access dynamics for `symmetry -> oscillation -> damping -> resonance -> collapse`
- decide `liquid / semi_frozen / frozen`
- decide which sensitivity tiers may be interpreted
- demote back toward `liquid` on intrusion, idleness, or drift
- provide minimal `RawStateVault` / `IdentityMemoryStore` scaffolding

What it does not do yet:

- implement real encryption/decryption
- ship built-in face/voice/iris/fingerprint models
- provide a fully learned long-term user memory engine
- store the full operational vault itself
- directly decrypt or render Atom/Athena/Pharaoh outputs

So MPK is the kernel that decides **who may read** and **how far meaning may open**.

## Why this concept feels unfamiliar

This package does not look like a normal login package because its goal is not
simply “open the door.”

Typical login:

- verify password / token / passkey
- allow or deny entry

MPK-style access:

- there is a remembered long-term user profile
- live user signals arrive
- both states converge over time
- when convergence becomes strong enough, information becomes meaningfully ordered
- when convergence breaks, interpretation melts away again

So MPK cares less about one-time entry and more about **who may interpret data as their own**.

## Quick start

```bash
cd _staging/MemoryPhase_Kernel
python3 -m pytest tests/ -q
python3 scripts/verify_signature.py
```

```python
from memory_phase_kernel import (
    IdentityProfile,
    LiveSignalFrame,
    MemoryPhaseKernel,
    readings_from_simple_map,
)

k = MemoryPhaseKernel()
profile = IdentityProfile("user-1", {"typing": 0.6, "voice": 0.4})
frame = LiveSignalFrame(
    readings=readings_from_simple_map({"typing": 0.9, "voice": 0.85}),
)
decision = k.evaluate(profile, frame)
print(decision.phase, decision.allowed_tiers, decision.score_bundle.resonance_index)
```

## Public API (summary)

| Piece | Role |
|-------|------|
| `MemoryPhaseKernel` | Optional trust anchor + frame → `AccessDecision` |
| `IdentityProfile` | Per-channel weights (long-term memory slot) |
| `LiveSignalFrame` | One tick of edge observations |
| `compute_resonance_index` | Ω_res |
| `evolve_phase_dynamics` | symmetry→oscillation→damping→resonance→collapse flow |
| `TrustAnchorProtocol` | Inject passkey / Secure Enclave / TPM-backed root |

## Foundational layer map

1. `Raw State Vault`
The storage layer that keeps data liquid by default. Real storage and decrypt logic remain external, but a `RawStateVault` scaffold now exists inside the package.

2. `Identity Memory Engine`
Long-term remembered-user slots. Today this starts with `IdentityProfile`, and `IdentityMemoryStore` provides the first accumulation scaffold.

3. `Continuous Identity Scoring`
Live-vs-memory comparison. Today this is `score_frame()` and `compute_resonance_index()`.

4. `Access Dynamics Layer`
The mathematical layer for symmetry -> oscillation -> damping -> resonance -> collapse. Today this begins with `dynamics.py`.

5. `Phase Transition Controller`
`liquid / semi_frozen / frozen` transitions. Today this is `phase_control.py`.

6. `Access Kernel`
Sensitivity-tier allowance. Today this is `AccessDecision.allowed_tiers`.

7. `Audit / Forgetting / Re-melt`
Session end, intrusion, and melt-back hooks. Today this starts with `ReMeltEvent`.

Important:

- MPK currently implements mostly layers 2 through 6.
- MPK now also exposes minimal scaffolds for Layer 0 and Layer 1 growth.
- The real raw-data vault and decrypt/render boundary are still external.
- The long-term adaptive memory engine is still ahead.

Important:

- The dynamics layer is no longer observational only.
- `collapse_score` now participates in real phase/access decisions.
- In other words, the `collapse -> entry` path is now beginning to affect production decisions.

The package now also has one more layer of practical hardening:

- `RawStateVault` may require both phase eligibility and sufficient `collapse_score`
- `IdentityMemoryStore` may apply `forgetting` and `drift penalty` instead of only growing forever

Operational bridges now also begin to exist:

- `atom_result_to_vault_record()`
- `athena_result_to_vault_record()`
- `pharaoh_result_to_vault_record()`
- `MemoryPhaseSessionLoop`

So MPK can now turn operational outputs into vault records and observe a minimal
`entry -> materialize -> re-melt` session flow.

## Practical use

This package does not yet replace production login stacks.
It is most useful today in:

- local personal-agent access kernels
- environments where operational outputs must open by sensitivity tier
- continuous-authentication experiments
- security workbenches that non-specialists can extend layer by layer
- systems that want to separate operational judgment from interpretation rights

## Integrity and verification

This repository uses “blockchain” in the sense of **integrity continuity**, not distributed consensus.

- [BLOCKCHAIN_INFO.md](BLOCKCHAIN_INFO.md)
- [PHAM_BLOCKCHAIN_LOG.md](PHAM_BLOCKCHAIN_LOG.md)
- [SIGNATURE.sha256](SIGNATURE.sha256)

Verification:

```bash
python3 scripts/verify_signature.py
```

The script checks that the SHA-256 manifest matches the current file contents.

## Relationship to other security models

MPK does not reject existing security. It is more realistic to combine it with:

1. password / passkey / Secure Enclave
- root-of-trust and possession

2. biometric checks
- strong single channels such as face / fingerprint / iris

3. behavioral continuous authentication
- typing, phrasing, usage rhythm, device flow, time-of-day

4. MPK
- organizes the above into a remembered-user access kernel
- `water -> ice`
- `symmetry -> oscillation -> damping -> resonance -> collapse`
- `entry -> re-melt`

So MPK is not just another credential.
It is a higher-order kernel for organizing many signals into memory-based access.

## How the layers should grow

Recommended order:

1. real `TrustAnchorProtocol`
2. richer `LiveSignalFrame` channels
3. stronger `IdentityMemoryStore`
4. stronger `RawStateVault`
5. broader operational bridges
6. fuller observer loop and audit chain

## Current status table

| Area | Status |
|------|--------|
| memory-based scoring | implemented |
| resonance / dynamics | implemented |
| collapse-based entry decision | implemented |
| vault materialization | foundational |
| forgetting / drift | foundational |
| operational bridges | foundational |
| session observer loop | foundational |
| real cryptography / key lifecycle | external responsibility |
| full audit chain | not yet implemented |

## Extension

- `memory_phase_kernel.extensions` — `ChannelAdapter` protocol + `KeystrokeRhythmStubAdapter` sample.
- `parse_mak_access_bridge` — parse FirstOrder `evidence["mak_access_bridge"]`.
- Operational stacks can emit bridge fields **without** installing MPK (FirstOrder v0.1.2+).

## License

MIT per `pyproject.toml` (change to match org policy if needed).
