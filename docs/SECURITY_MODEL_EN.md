> **Korean (canonical):** [SECURITY_MODEL.md](SECURITY_MODEL.md)

# MPK Security Model

This document explains the security idea behind `MemoryPhase_Kernel` and how it differs from more familiar login models.

## 1. Core definition

MPK is not just a login package.

- Typical login asks: “Should this subject be let in?”
- MPK asks: “Who may interpret this information as their own?”

So MPK is best understood as a **memory-based access kernel**.

## 2. Water and ice

- `liquid`
  - information exists but does not yet reveal personal meaning
  - masked / summarized / non-interpretable state

- `semi_frozen`
  - partial ordering
  - operational information may open

- `frozen`
  - enough confidence that the subject matches the remembered user
  - personal and sensitive meaning may become ordered

## 3. What memory-based security means here

“Memory” in MPK is not just raw recordings or photos.

- channel weights
- trust history
- behavior tendencies
- long-term matching structure

The local agent remembers who the user is over time and compares live signals against that remembered structure.

## 4. Current package scope

Provided today:

- memory-based identity scoring
- resonance / access dynamics
- collapse-based access decision
- phase transition
- sensitivity-tier allowance
- vault materialization scaffold
- session observer loop scaffold

Not yet provided:

- real encrypted storage
- full biometric inference models
- full long-term adaptive learning
- full audit chain

## 5. Difference from other approaches

### Password-based

- simple
- but static and weak once leaked

### Biometric-only

- strong single channel
- but brittle if that channel fails or is spoofed

### Behavioral authentication

- good for continuous checks
- but may remain ad-hoc without a stronger organizing structure

### MPK

- long-term memory
- multi-channel comparison
- continuous authentication
- phase-based information ordering

Its strength is not one credential, but organizing many signals into remembered-user access.

## 6. Why it must stay separate from operational systems

Atom / Athena / Pharaoh produce judgments and operational outputs.

MPK decides:

- who may read them
- how far they may open
- when they should melt shut again

That separation is essential.

## 7. Expansion principles

1. prefer features over raw storage
2. preserve trust-anchor roots
3. separate phase decisions from real decrypt/render layers
4. strengthen the session observer
5. expand audit separately
6. let memory accumulate, but also allow forgetting and drift handling

## One-line conclusion

**MPK is the memory-based access security kernel that decides whether information may become ice-like and interpretable for the remembered user.**
