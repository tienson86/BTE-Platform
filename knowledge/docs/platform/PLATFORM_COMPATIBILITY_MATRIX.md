# Platform Compatibility Matrix

| Field | Value |
|-------|-------|
| **Document** | PLATFORM_COMPATIBILITY_MATRIX |
| **Platform version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## Rule

A consumer is compatible with Platform 1.0.0 only when **every** required axis below is satisfied.

Unsupported combinations MUST fail closed (contract / version diagnostic). Silent coercion is forbidden.

---

## Version axes

| Axis | Compatible with Platform 1.0.0 |
|------|--------------------------------|
| Foundation | `==1.0.0` |
| Knowledge version | `>=1.0.0` within schema 2.0.0 |
| Knowledge schema | `==2.0.0` |
| Package spec | `==1.0.0` |
| Canonical Analysis Pipeline | `==2.0.0` |
| Canonical Decision Pipeline | `==1.0.0` |
| Canonical Luck Pipeline | `==1.0.0` |
| Canonical Interpretation Pipeline | `==1.0.0` |
| Canonical Report Pipeline | `==1.0.0` |
| Report Foundation / Layout / Rendering | `==1.0.0` |
| Released packages | sealed checksums in `COMPONENT_CHECKSUMS.json` |
| API | public contracts as of AF-1; no silent field rename |

AX-1 Analysis Pipeline `1.0.0` remains importable for backward compatibility. New Analysis Knowledge work MUST bind AX-2 `canonical_analysis_pipeline` 2.0.0.

---

## Layer compatibility

| Producer | Consumer | Constraint |
|----------|----------|------------|
| Foundation 1.0.0 | All engines | Frozen identities and schema 2.0.0 |
| Knowledge packages 2.0.0 | Rule / Analysis / Decision / Luck | `status=released`, checksum match |
| Calendar / Bazi | Analysis | Chart inputs only; no reverse import |
| Analysis 2.0.0 | Decision 1.0.0 | Published analysis outputs only |
| Analysis 2.0.0 + Decision 1.0.0 | Luck 1.0.0 | Snapshots; Luck does not recompute Useful God |
| Analysis + Decision + Luck | Interpretation 1.0.0 | Dict snapshots; no reverse import |
| Interpretation 1.0.0 | Report 1.0.0 | Structure / layout / render only |
| Report artifact | API / Portal | In-memory mime envelope; no filesystem persist in RX-1 |
| API | Engines | Public API only; no internal module import |

---

## Package ↔ pipeline

| Package | Pipeline stage |
|---------|----------------|
| `bz_02` Seasonal | Analysis `seasonal` |
| `bz_01` Strength | Analysis `strength` |
| `bz_03` Temperature | Analysis `temperature` |
| `bz_04` Pattern Core | Analysis `pattern` |
| `bz_05` Pattern Evaluation | Analysis `pattern_evaluation` |
| `bz_06` UG Foundation | Decision `useful_god_foundation` |
| `bz_07` UG Priority | Decision `useful_god_priority` |
| `bz_08` UG Override | Decision `useful_god_override` |
| `bz_09` Luck Foundation | Luck `timeline` |

Optional peer packages are checked only when co-loaded.

---

## Forbidden combinations

- Schema 1.x package executing as V2 without dual-read declaration
- Decision package executed outside Canonical Decision Pipeline
- Report components executed outside Canonical Report Pipeline for new work
- Interpretation AI rewrite enabled
- Renderer `xlsx` / `pptx` enabled
- Engine importing a downstream engine

---

## Dual-read

Knowledge Database V1 dual-read remains authorized only where a package declares `compatible_with_v1: true`. V1 files are not rewritten by Platform 1.0.0.

---

## Matrix file

Machine-readable copy: `knowledge/releases/v1.0/VERSION_MATRIX.json`.
