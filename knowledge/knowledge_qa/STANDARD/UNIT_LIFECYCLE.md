# Unit Lifecycle — V1.0

| Field | Value |
|-------|-------|
| Document | UNIT_LIFECYCLE |
| Standard | Knowledge QA V1.0 |

---

# 1. Frozen states

```text
Draft
  ↓
Reviewed
  ↓
Validated
  ↓
Frozen
  ↓
Deprecated
```

| State | Meaning |
|-------|---------|
| **Draft** | Authored; not approved for production |
| **Reviewed** | QA PASS + Domain Reviewer accepted |
| **Validated** | QA_CHECKLIST complete; governance approved for pack release |
| **Frozen** | Immutable for catalog version; production consumption |
| **Deprecated** | Superseded, merged, or unsafe; never reuse id |

---

# 2. Entry and exit

## Draft

| | |
|---|---|
| **Entry** | Unit created in catalog from Interpretation Knowledge |
| **Exit** | QA PASS + Domain Reviewer → Reviewed |
| **Approval** | None required to exist |
| **Rollback** | Delete or edit freely |

## Reviewed

| | |
|---|---|
| **Entry** | QA PASS on unit; Domain Reviewer sign-off |
| **Exit** | QA_CHECKLIST pass → Validated |
| **Approval** | Domain Reviewer |
| **Rollback** | Revert to Draft with audit note; re-QA required |

## Validated

| | |
|---|---|
| **Entry** | All blocking QA closed; pack validation gate passed |
| **Exit** | Governance freeze event → Frozen |
| **Approval** | Domain Reviewer + Governance |
| **Rollback** | Revert to Reviewed only with governance record |

## Frozen

| | |
|---|---|
| **Entry** | FREEZE_POLICY satisfied |
| **Exit** | Deprecation only |
| **Approval** | Governance |
| **Rollback** | **Not allowed** without new catalog version and re-freeze |

## Deprecated

| | |
|---|---|
| **Entry** | Split, merge, duplicate resolution, safety, supersession |
| **Exit** | Terminal |
| **Approval** | Governance |
| **Rollback** | Never reuse `knowledge_id` |

---

# 3. Status vs QA verdict

| QA verdict | Allowed catalog status |
|------------|------------------------|
| FAIL | Draft only |
| REVIEW | Draft only |
| PASS (pending reviewer) | Draft |
| PASS (reviewer accepted) | Reviewed |
| Validated checklist | Validated |
| Freeze event | Frozen |

---

# 4. Parallel units

- Same topic may have many Draft units.
- Only **Validated/Frozen** units are production candidates.
- **Representative** selection happens at Reasoning runtime, not at lifecycle promotion.

---

# 5. Version coupling

When catalog `version` increments:

- New units start Draft
- Changed units re-QA from Draft
- Frozen units from prior version remain Frozen until explicitly deprecated or superseded

---

END
