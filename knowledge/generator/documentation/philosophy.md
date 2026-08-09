# Generator Philosophy

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Status** | Canonical |

---

## 1. Knowledge is packaged, not piled

BTE does not grow a single unbounded rule dump. Every official knowledge unit ships as a KD-3 **Knowledge Package**: identified, versioned, validated, checksummed, and independently releasable.

The Generator exists so that creating the next package is a **repeatable, deterministic process**, not a one-off folder copy.

---

## 2. Profile before content

A package begins as a **profile**, not as a pile of rules.

Identity, type, domain, taxonomy, ontology, completeness flags, validation profile, and quality target are decided first. Content fills a declared shape. This prevents accidental mixed-purpose packages and silent incompleteness.

---

## 3. Standards over invention

The Generator does not create analytical schools.

It binds authors (human or AI) to:

- KD-1 envelopes
- KD-2 taxonomy / ontology
- KD-3 package anatomy
- KD-4 authoring, review, and release
- KX-1B evidence (when required)
- KX-1C reasoning (when required)

New theory requires a Domain Reviewer and an explicit profile change — never a silent `if` in an engine.

---

## 4. Determinism is trust

Same profile + same templates + same authored facts ⇒ same package bytes (after locale `C` sort and two-pass checksum).

Random identifiers, unordered emission, and undocumented scoring are incompatible with commercial explainability.

---

## 5. Draft is cheap; release is sacred

Generation may be fast. Release is slow on purpose.

AI may draft. Humans review. Released bytes are immutable. Corrections are new versions.

---

## 6. Dual-read, additive platform

V1 Rule Database and existing packages (including Strength Core) remain valid. The Generator is additive Foundation. It does not rewrite history to make generation easier.

---

## 7. Scale without renaming

Identifiers, folders, and checksums must remain valid at 100,000+ records and across unlimited future package types (Feng Shui, Qi Men, I Ching, …). New types bump `generator_version` when the enum must grow; they do not fork a second generator.
