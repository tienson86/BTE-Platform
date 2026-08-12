# Lifecycle — V1.0

| Field | Value |
|-------|-------|
| Document | LIFECYCLE |
| Version | 1.0.0 |

---

# 1. Unit lifecycle (frozen)

Aligns with Knowledge QA Standard V1.0:

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

| State | Factory stage entered | Factory stage exit |
|-------|----------------------|-------------------|
| **Draft** | Catalog created | QA PASS + Domain Reviewer |
| **Reviewed** | Review (QG4 start) | Validation pass |
| **Validated** | Validation (QG5) | Freeze (QG6) |
| **Frozen** | Freeze | Deprecation only |
| **Deprecated** | Change pipeline | Terminal |

Detail: `knowledge/knowledge_qa/STANDARD/UNIT_LIFECYCLE.md`

---

# 2. Library lifecycle (prose)

| State | Meaning |
|-------|---------|
| **Draft** | Chapters in progress |
| **Reviewed** | Domain Reviewer read complete |
| **Approved** | QG1 pass; catalog may proceed |
| **Superseded** | New library version replaces |

Library does not use Frozen — Catalog owns machine immutability.

---

# 3. Pack lifecycle

```text
Chartered (QG0)
  ↓
Library approved (QG1)
  ↓
Catalog authoring
  ↓
QA in progress
  ↓
Review complete (all topics)
  ↓
Validated (pack)
  ↓
Frozen (pack)
  ↓
In Production
  ↓
Released
  ↓
Maintained (change pipeline)
  ↓
Superseded (new major version)
```

---

# 4. Lifecycle × gate matrix

| Gate | Minimum unit status after |
|------|---------------------------|
| QG2 | Draft |
| QG3 | Draft (QA recorded) |
| QG4 | Reviewed (PASS units) |
| QG5 | Validated |
| QG6 | Frozen |
| QG7 | Frozen (in production) |

---

# 5. Rollback

| From | To | Approval |
|------|-----|----------|
| Reviewed | Draft | Domain Reviewer |
| Validated | Reviewed | Domain Reviewer + note |
| Frozen | — | New version only |
| Production | Prior Frozen | Production Owner |
| Released | Prior release | Release Manager |

---

# 6. PACK-01 current lifecycle state

| Layer | State |
|-------|-------|
| Library | Approved (authored) |
| Catalog | 339 Draft units |
| QA | 78 units reviewed (3 phases); remainder pending |
| Review | Not started (status still Draft) |
| Validation | Not started |
| Freeze | Not started |
| Production | Not loaded |
| Release | Not released |

---

END
