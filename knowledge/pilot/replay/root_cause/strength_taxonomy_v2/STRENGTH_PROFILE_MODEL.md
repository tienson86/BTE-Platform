# Strength Profile Model (Design)

**Status:** DESIGN — not implemented  
**Principle:** Profile explains *why*; taxonomy classifies *how*; score measures *how much*.

## Candidate dimensions

| Dimension | Meaning | Publication class |
|---|---|---|
| `support_score` | Companion / same-element support mass | PUBLISHED_CANDIDATE |
| `restriction_score` | Officer / control mass | PUBLISHED_CANDIDATE |
| `resource_score` | Seal / resource mass | PUBLISHED_CANDIDATE |
| `companion_score` | Peer/rob wealth mass (may nest under support) | DIAGNOSTIC_ONLY or merge into support |
| `output_score` | Output / drain mass | PUBLISHED_CANDIDATE |
| `root_score` | Rooting strength | PUBLISHED_CANDIDATE (already partially public) |
| `season_alignment` | Month-status / season contribution | PUBLISHED_CANDIDATE |
| `temperature_adjustment` | Climate adjustment (declare source) | DIAGNOSTIC_ONLY until sources unify |
| `interaction_adjustment` | Combo/clash/sitting | CANONICAL_INTERNAL until producer exists |
| `structural_adjustment` | Special structural rules | CANONICAL_INTERNAL |
| `evidence_completeness` | Fraction of expected evidence present | PUBLISHED_CANDIDATE |
| `evidence_confidence` | Aggregate evidence reliability | PUBLISHED_CANDIDATE |

## Relationship to current public contract

Today public: `strength_score`, component season/root/support/drain/control, `strength_level`, `confidence`, `reasoning`.

Profile v2 **extends** explanation; it does not replace `strength_score`.

## Why profile is mandatory

CASE-0003 and CASE-0005 share **normalized score 0.66** but differ in bucket composition:

| Case | sea | root | support | drain | ctl | Expert |
|---|---:|---:|---:|---:|---:|---|
| 0003 | +25 | +22 | 0 | −23 | −8 | slightly weak |
| 0005 | −10 | +30 | +13 | −11 | −6 | slightly strong |

Identical scores, different profiles → taxonomy must consume **profile + score**, not score alone.

## Publication policy

| Class | Meaning |
|---|---|
| CANONICAL_INTERNAL | Required for engine reasoning; may stay off public API |
| PUBLISHED_CANDIDATE | Eligible for future public Strength contract |
| DIAGNOSTIC_ONLY | Pilot / QC / expert tools only |
