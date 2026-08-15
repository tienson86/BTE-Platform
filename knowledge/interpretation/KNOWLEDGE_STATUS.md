# Knowledge Status — Interpretation Layer

## Entity lifecycle

| Status | Meaning |
|---|---|
| draft | Authoring in progress — not for production narrative |
| review | Peer review — may be used in pilot |
| approved | Production-ready expert meaning |
| deprecated | Retained for traceability — do not use in new narrative |

## Sprint K2 / K2.1 inventory — Useful God V1

| Domain | Entities | Status |
|---|---|---|
| UsefulGod | 20 (10 stem + 10 role) | approved |
| Strength | 3 (`strong`, `balanced`, `weak`) | approved |
| Pattern | 26 (10 main + 5 special + 6 follow + 5 combination) | approved |
| Temperature | 0 | — |
| TenGods | 11 (10 roles + Nhật Chủ) | approved |
| ShenSha | 0 | — |
| Luck | 0 | — |
| FiveElements | 0 | — |
| FengShui | 0 | — |
| Calendar | 0 | — |
| ExecutiveSummary | 0 | — |
| Recommendations | 0 | — |

Coverage index: `knowledge/interpretation/domains/useful_god/COVERAGE.md`

## Sprint K3 inventory — Strength V1 (state domain)

Engine inventory (Strength Engine V2 level rules): `strong` | `balanced` | `weak`.

`very_strong` and `very_weak` are not emitted by the engine and are not populated.

Coverage index: `knowledge/interpretation/domains/strength/COVERAGE.md`

## Sprint R1 — Relationship Reasoning Framework

Generic graph contracts only. Pattern is the first domain to consume the framework (K4).

## Sprint K4 — Pattern Domain V1

Complete domain: facts + relationship assessment + knowledge + interpretation + narrative mapping.

Engine inventory: 26 codes from `database/14_pattern/`.

Coverage index: `knowledge/interpretation/domains/pattern/COVERAGE.md`

## Sprint K5 — Ten Gods Domain V1

Complete domain: facts + relationship assessment + knowledge + interpretation + narrative mapping.

Engine inventory: 10 classic labels from `TEN_GOD_LABELS` plus `Nhật Chủ` (`god_id=day_master`).

Coverage index: `knowledge/interpretation/domains/ten_gods/COVERAGE.md`

