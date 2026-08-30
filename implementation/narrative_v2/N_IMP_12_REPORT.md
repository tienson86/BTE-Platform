# N-IMP-12 GOLDEN DATASET REPORT

Sprint: N-IMP-12
Module: `engines.narrative_v2.golden`
Mode: Shadow only
Status: READY FOR PRODUCT OWNER REVIEW

STOP. N-IMP-13 was not started.

---

## 1. Status

PASS

The official Narrative V2 Golden Dataset is a collection of CERTIFIED Presentation baselines. CASE-0001 is FROZEN as version 1. Golden never bypasses Certification. Production Portal, Pack05, Narrative, Knowledge, and the existing Pack05 Golden Dataset were not modified.

---

## 2. Architecture

```
Certification == CERTIFIED
  → GoldenDataset.promote()
       → hashes
       → freeze file (append-only version)
       → registry row
  → regression compare against frozen Presentation
```

Location: `engines/narrative_v2/golden/`

| File | Role |
| --- | --- |
| `golden_dataset.py` | Promote, get, registry, compare |
| `golden_case.py` | Immutable `GoldenCase` |
| `golden_registry.py` | Append-only version index |
| `golden_validator.py` | Eligibility + regression diffs |
| `golden_serializer.py` | Canonical JSON + SHA-256 hashes |
| `golden_history.py` | Freeze files; never overwrite |
| `golden_errors.py` | Eligibility / immutability errors |

Store: `implementation/narrative_v2/golden/`

---

## 3. Golden Model

`GoldenCase` (`bte.golden.v1`)

- `case_id`
- `presentation` (certified copy)
- `certification` (CERTIFIED record)
- `canonical_hash` / `presentation_hash` / `review_hash` / `certification_hash` / `narrative_hash`
- `status` = FROZEN
- `version`
- `created` / `reviewer`
- `metadata` (shadow_mode, replaces_pack05, versions)

Cases are frozen dataclasses with immutable nested mappings. New promotions append `v2`, `v3`, … Existing freeze files are never rewritten.

---

## 4. Eligibility

Only `certification.status == CERTIFIED` may be promoted.

Rejected: DRAFT, REVIEW, REJECTED, REVOKED, missing reviewer, `golden_eligible == false`, Presentation not `bte.presentation.v2.1`.

Certification is not skipped. Testing is not used as a substitute for Certification.

---

## 5. Registry

Append-only `registry.json`:

| case_id | version | status | created | reviewer |
| --- | --- | --- | --- | --- |
| CASE-0001 | 1 | FROZEN | 2026-08-30T07:00:00+00:00 | product-owner |

Latest Golden Case for a case id is the highest version. Prior versions remain on disk.

---

## 6. Hashes

SHA-256 of canonical JSON. Used for regression.

| Hash | CASE-0001 |
| --- | --- |
| canonical_hash | e1b55071af8576b6f75c1565872ed481e13c4c12b89f3ce72b1cb091a688505f |
| presentation_hash | 398ab3f5d069ef435bcf1baa017d80b200070376d8cbecbc955ce02921c7585d |
| review_hash | ed0140306b6e86bec0b0d8cf2de32b01758e9425f51604f2731caeb8d00fe421 |
| certification_hash | e7e4862b02009ebc3702171e62e690dd313f541ee89aa1cea347802a156e3638 |
| narrative_hash | fd8ed828fd2b69f79da038fbf5e8397e3c3dd13d93539ebb487ece11e993f794 |

Canonical identity is CASE-0001 birth input + stage `luck` (not invented Narrative text).

---

## 7. Regression

`GoldenDataset.compare(case_id, presentation)` diffs a current Presentation against the frozen Golden Case.

CASE-0001 vs certified n_imp_09a freeze: matched YES, 0 diffs.

This Golden Case is the baseline for future Narrative regression.

---

## 8. CASE-0001 Promotion

Promoted. No hardcoded Narrative.

Sources:

- Presentation: `implementation/narrative_v2/n_imp_09a/case0001_presentation_v2_1.json`
- Certification: `implementation/narrative_v2/n_imp_11a/certification_history.json` (CERTIFIED, product-owner)

Result: FROZEN v1, Golden eligible because Certification was CERTIFIED.

---

## 9. Tests

`tests/narrative_v2/test_golden_dataset.py` — **8 passed**

- Eligibility
- Promotion
- Freeze / no overwrite
- Hashes
- Registry
- Versioning
- Regression compare
- No mutation of Presentation, Knowledge, Pack05 Golden, Portal

---

## 10. Artifacts

`implementation/narrative_v2/n_imp_12/`

- `case0001_golden.json`
- `golden_registry.json`
- `golden_diff.md`
- `hash_report.md`

Official store: `implementation/narrative_v2/golden/cases/CASE-0001/v1.json`

---

## 11. Out-of-scope

| Item | Honored |
| --- | --- |
| No Production Switch | YES |
| No Pack05 Removal | YES |
| No Narrative rewrite | YES |
| N-IMP-13 not started | YES |

---

## 12. Verdict

READY FOR PRODUCT OWNER REVIEW

STOP.
