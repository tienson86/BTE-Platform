# Freeze Policy — V1.0

| Field | Value |
|-------|-------|
| Document | FREEZE_POLICY |
| Standard | Knowledge QA V1.0 |

---

# 1. Purpose

Define when a Knowledge Unit may become **Frozen** — immutable for a catalog version and safe for production Reasoning consumption.

---

# 2. Unit freeze prerequisites

A unit may move **Validated → Frozen** only when **all** are true:

| # | Condition |
|---|-----------|
| 1 | Status is **Validated** |
| 2 | QA record archived (phase review or unit review) |
| 3 | Verdict was PASS at last QA (no open REVIEW/FAIL) |
| 4 | QA_CHECKLIST signed for that unit |
| 5 | `source_document` unchanged since validation |
| 6 | Catalog version incremented for freeze event |
| 7 | Governance sign-off |

---

# 3. Pack freeze prerequisites

A pack catalog may freeze when:

| # | Condition |
|---|-----------|
| 1 | All production-scope units Validated |
| 2 | No open FAIL in any topic phase |
| 3 | REVIEW items tracked with owner or waived by governance |
| 4 | Duplicate clusters declared for known overlaps |
| 5 | Golden references (if any) pinned and consistent |
| 6 | CHANGELOG updated |
| 7 | Governance freeze approval |

---

# 4. After freeze

| Rule | Detail |
|------|--------|
| No silent edit | Frozen units change only via new version |
| Re-QA | Any claim change → Draft → full QA path |
| Deprecation | Supersede with new id; never reuse old id |
| Reasoning | Consumes Frozen units only in production |

---

# 5. What freeze is not

- Not approval of Reasoning Engine code
- Not approval of Composer output quality
- Not waiver of Interpretation Standard compliance

---

# 6. Emergency unfreeze

Requires:

1. Governance record with customer impact assessment
2. Catalog version bump
3. Re-validation of affected units
4. Reasoning regression if golden affected

---

END
