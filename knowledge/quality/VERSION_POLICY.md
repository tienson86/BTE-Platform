# VERSION_POLICY

| Field | Value |
|-------|-------|
| Document | VERSION_POLICY |
| System | Quality Gate System V1.0 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

---

## Names

| Name | Kind | Meaning |
|------|------|---------|
| Quality Gate System V1.0 | Governance package | This folder’s frozen rule set |
| Q0–Q4 | Quality level | Product quality maturity |
| RC0, RC1, RC2 | Release candidate stages | Not a commercial SKU |
| Commercial V1 | Commercial version | Adult ship set |
| Commercial V1.1 | Commercial version | Context-safe + coverage |
| GOLDEN_DATASET_V1 | Laboratory | Ground truth; separate versioning |

Do not reuse “V1.0” for engines, Knowledge packs, and commercial SKU as if they were one number.

---

## Freeze

| Object | Freeze rule |
|--------|-------------|
| This system (V1.0) | Policy files frozen. Amend only via [CHANGELOG.md](CHANGELOG.md) + Product + Dataset Steward. |
| Q definitions | Frozen. Do not rename Q1 to mean Q2. |
| Gate definitions | Frozen. New stages are new names (e.g. Commercial V1.2), not silent inserts. |
| Floors | Frozen. Never lowered to pass. |
| Scorecard snapshot | Dated. New cycle = new snapshot rows, not back-edit. |
| Golden Dataset | Independent freeze (`CHANGE_POLICY` there). **Do not modify from this package.** |

---

## Advancement

```text
Evidence updated
    ↓
Scorecard + board updated
    ↓
Checklist for target gate all [x]
    ↓
CHANGELOG row
    ↓
Version / stage name may be claimed
```

A stage name (RC2, Commercial V1) may appear in marketing or roadmap **only after** the checklist is PASS.

---

## Compatibility

| Change | Version action |
|--------|----------------|
| Clarify wording, no rule change | CHANGELOG note; stay V1.0 |
| Add a mandatory check | Bump system to V1.1; old RC PASS records stay valid only if still meeting new check or grandfathered in writing |
| Change floors | New system major (V2). Old commercial claims must be re-gated. |
| New commercial SKU class | New commercial version (V1.2+), still under this gate system |

---

## Relationship to other version labels

| Label elsewhere | This system |
|-----------------|-------------|
| Engine / Knowledge semver | Prerequisite evidence only |
| QC4 `BTE-RC-1.0.0` | Knowledge-infrastructure RC — **not** Commercial V1 |
| UI Sprint “Release Candidate” | Delivery track — **not** a gate pass |
| GOLDEN_DATASET_V1 RC1/RC2 | Evidence aligned to RC1/RC2 here; this system is the authority |

---

## Records

Every claimed stage change is a [CHANGELOG.md](CHANGELOG.md) row plus board update.

No silent promotion.

---

END
