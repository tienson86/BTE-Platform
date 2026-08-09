# Knowledge Health Score

Scores are 0–100 governance indices from KX-6D read-only inspection. Not engine KPIs.

## Scores

| Index | Score | Band |
| --- | --- | --- |
| Coverage | 76 | Good |
| Consistency | 86 | Strong |
| Contract | 74 | Good |
| Maintainability | 84 | Strong |
| Governance | 91 | Strong |
| Risk (lower is better) | 29 | Moderate-low |
| **Overall health** | **81** | **B+ / RM-reviewable** |

## Coverage score — 76

+ Analytical spine bz_01–bz_08 + bz_10–bz_15 populated.
+ 2 849 rules with 1:1 evidence.
− 11 / 34 taxonomy domains have a primary package.
− Luck foundation has 0 production rules.
− No Calendar / Four Pillars / Shen Sha / Interpretation / Report packages.

## Consistency score — 86

+ Zero cycles; optional-only deps; unique output names.
+ Schema / knowledge / compatibility aligned.
− bz_01 SemVer 1.2.0 vs peers 1.0.0.
− bz_01 quality_target unset.
− Combination vs Transformation both model “hợp” at different layers (intentional but easy to confuse).

## Contract score — 74

+ Explicit contracts on bz_05–bz_15.
+ Downstream consumers stay on published names.
− Implicit season/strength/temperature scores (no publish assets on bz_01–bz_03).
− Large unused diagnostic/reasoning tails (OK for future Interpretation).
− bz_09 uses raw pillar fields (different contract family).

## Maintainability score — 84

+ Checksums, manifests, tests, immutable RELEASE records.
+ Wave 1 score-band rules avoid chart rewrite.
− Early packages thinner docs/reasoning (3 chains).
− Advanced packs are large sealed blobs (300–400 rules) — future SemVer cost.

## Governance score — 91

+ AF-1 freeze respected in this sprint (docs only).
+ PVP-RELEASE on all 15; 0 validation errors.
+ Independently deployable optional dependency policy.

## Risk score — 29

Drivers: Golden Dataset N/A; Analysis Engine unwired; luck isolated; UGO and HSA have no in-ecosystem consumer; implicit foundation contracts; Wave 1 does not match raw stems/branches.

## Overall recommendation

**Accept Wave 1 knowledge ecosystem for Release Manager review.** Do not block on Interpretation or engine wiring. Track contract-asset backfill and luck analytical package as next SemVer work — **without mutating sealed 1.0.0/1.2.0 packages in this sprint.**
