# Strength Taxonomy v2 — Design & Expert Calibration (PILOT-1C)

**Mode:** DESIGN ONLY — no production implementation  
**Predecessor:** PILOT-1B → `STRENGTH_TAXONOMY_LIMITATION_CONFIRMED`  
**Architecture Freeze:** AF-1 unchanged  

## Separation of concerns

| Concept | Question |
|---|---|
| Strength Score | How much strength does the model measure? |
| Strength Profile | Why did the model arrive there? |
| Strength Taxonomy | How should that profile be classified? |
| Strength Confidence | How certain is the classification? |

These must not collapse into one field.

## Artifacts

| File | Purpose |
|---|---|
| [PILOT_1C_SUMMARY.md](PILOT_1C_SUMMARY.md) | Executive summary + final decision |
| [STRENGTH_TAXONOMY_V2.md](STRENGTH_TAXONOMY_V2.md) | Candidate 7-level taxonomy |
| [STRENGTH_PROFILE_MODEL.md](STRENGTH_PROFILE_MODEL.md) | Profile dimensions |
| [STRENGTH_EVIDENCE_MODEL.md](STRENGTH_EVIDENCE_MODEL.md) | Canonical evidence schema |
| [STRENGTH_BOUNDARY_MODEL.md](STRENGTH_BOUNDARY_MODEL.md) | Boundary / conflict handling |
| [STRENGTH_CONFIDENCE_MODEL.md](STRENGTH_CONFIDENCE_MODEL.md) | Confidence bands |
| [EXPERT_CALIBRATION_PROTOCOL.md](EXPERT_CALIBRATION_PROTOCOL.md) | Repeatable expert review |
| [EXPERT_AGREEMENT_MATRIX.md](EXPERT_AGREEMENT_MATRIX.md) | Agreement categories on 7 cases |
| [CASE_0001_EXPERT_REVIEW.md](CASE_0001_EXPERT_REVIEW.md) | Priority weight review |
| CASE_0002…0007_CALIBRATION.md | Per-case calibration notes |
| [GOLDEN_DATASET_EXPANSION_PLAN.md](GOLDEN_DATASET_EXPANSION_PLAN.md) | Future case categories |
| [BACKWARD_COMPATIBILITY.md](BACKWARD_COMPATIBILITY.md) | v1↔v2 coexistence |
| [IMPLEMENTATION_READINESS.md](IMPLEMENTATION_READINESS.md) | Readiness gate |
| [RECOMMENDED_NEXT_ACTION.md](RECOMMENDED_NEXT_ACTION.md) | P0–P4 recommendations |
| [VALIDATION.md](VALIDATION.md) | Freeze confirmation |

## Final decision (preview)

**CALIBRATION_READY** — design + protocol complete; n=7 insufficient for IMPLEMENTATION_READY.
