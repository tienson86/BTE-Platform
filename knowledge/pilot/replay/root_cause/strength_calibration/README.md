# PILOT-1B — Strength Calibration & Taxonomy

Investigation and calibration only. No production Strength formula changes. AF-1 intact.

## Objective

Determine whether Pilot Strength discrepancies (CASE-0001…0007) are caused by evidence, weighting, score math, thresholds, taxonomy, confidence, upstream chart, or expert disagreement.

**Truth before PASS count.**

## Artifacts

| File | Content |
|---|---|
| [PILOT_1B_SUMMARY.md](PILOT_1B_SUMMARY.md) | Executive summary + final decision |
| [STRENGTH_EVIDENCE_LEDGER.md](STRENGTH_EVIDENCE_LEDGER.md) | Per-case pipeline + matched rules |
| [STRENGTH_SCORE_ANALYSIS.md](STRENGTH_SCORE_ANALYSIS.md) | Raw / normalized / band / label separation |
| [STRENGTH_POLARITY_ANALYSIS.md](STRENGTH_POLARITY_ANALYSIS.md) | CASE-0001 polarity ledger |
| [STRENGTH_TAXONOMY_AUDIT.md](STRENGTH_TAXONOMY_AUDIT.md) | Current 3-band contract audit |
| [STRENGTH_CONFIDENCE_AUDIT.md](STRENGTH_CONFIDENCE_AUDIT.md) | Confidence behavior |
| [EXPERT_AGREEMENT_MATRIX.md](EXPERT_AGREEMENT_MATRIX.md) | Expert vs runtime matrix |
| [TAXONOMY_PROPOSAL.md](TAXONOMY_PROPOSAL.md) | Candidate 7-level proposal (not implemented) |
| [RECOMMENDED_CHANGES.md](RECOMMENDED_CHANGES.md) | P0–P3 recommendations |
| [VALIDATION.md](VALIDATION.md) | Freeze / scope confirmation |
| `evidence/*.json` | Machine-readable extraction |

## Final decision (preview)

**STRENGTH_TAXONOMY_LIMITATION_CONFIRMED**

No objective polarity-sign / arithmetic implementation bug proven. Taxonomy insufficient for expert lexicon. CASE-0001 score plausibility remains a modeling/research item (not a P0 code defect).

## How evidence was produced

```text
PYTHONPATH=. python knowledge/pilot/replay/root_cause/strength_calibration/_extract_evidence.py
```

Uses live `CalendarEngine` → `BaziEngine` → `build_strength_context` → `StrengthEngine` (analyzer + scorer). CASE-0006 uses live corrected month **Mậu Ngọ** (PILOT-1A).
