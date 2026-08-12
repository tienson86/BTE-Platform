# Quality Gates — V1.0

| Field | Value |
|-------|-------|
| Document | QUALITY_GATES |
| Version | 1.0.0 |
| Section | 3 — Quality Gates |

---

# 3.1 Rule

**No stage may continue without passing its gate.**

Waivers require Chief Reviewer written record with customer impact assessment.

---

# 3.2 Gate summary

| Gate | Name | Stage exit | Approver |
|------|------|------------|----------|
| **QG0** | Charter Gate | Idea → Draft | Chief Reviewer |
| **QG1** | Library Gate | Draft → Catalog | Domain Reviewer |
| **QG2** | Catalog Gate | Catalog → QA | Domain Reviewer |
| **QG3** | QA Gate | QA → Review | QA complete (human accepts) |
| **QG4** | Review Gate | Review → Validation | Domain Reviewer |
| **QG5** | Validation Gate | Validation → Freeze | Domain Reviewer + Reasoning gov |
| **QG6** | Freeze Gate | Freeze → Production | Chief Reviewer |
| **QG7** | Release Gate | Production → Release | Release Manager + Production Owner |

---

# 3.3 QG0 — Charter Gate

| Check | Pass condition |
|-------|----------------|
| Domain scope defined | Pack domain documented |
| Fact boundaries | Rule Database scope identified |
| Interpretation Standard alignment | Modes and bans acknowledged |
| Topic list frozen | Chapter list approved |
| No engine scope creep | Pack is knowledge only |

**Blocks:** Authoring without charter.

---

# 3.3 QG1 — Library Gate

| Check | Pass condition |
|-------|----------------|
| All chapters present | Per pack topic list |
| Professional review | Domain Reviewer read complete library |
| No rule dump | No scores, rule ids, algorithms |
| Source index | KNOWLEDGE_INDEX complete |
| Version set | Library version incremented |

**Blocks:** Catalog conversion for unapproved library.

Checklist: [CHECKLISTS.md](CHECKLISTS.md) § Author (Library).

---

# 3.4 QG2 — Catalog Gate

| Check | Pass condition |
|-------|----------------|
| Schema compliance | Every unit matches CATALOG_SCHEMA |
| Source trace | Every unit has `source_document` |
| Id policy | Stable `knowledge_id` per pack |
| Duplicate clusters declared | Known overlaps registered |
| All units Draft | No premature Validated/Frozen |
| Index complete | CATALOG_INDEX matches file count |

**Blocks:** QA phase for incomplete catalog topic.

Checklist: [CHECKLISTS.md](CHECKLISTS.md) § Author (Catalog).

---

# 3.5 QG3 — QA Gate

| Check | Pass condition |
|-------|----------------|
| Topic phase complete | All units in scope scored |
| Twelve criteria scored | Per QA Standard |
| Verdicts assigned | PASS / REVIEW / FAIL |
| FAIL count | Zero FAIL (or waived by Chief Reviewer) |
| Phase review archived | Under `knowledge_qa/PACK_XX/` |
| No catalog edit in QA task | Review-only integrity |

**Blocks:** Review promotion for FAIL units.

Reference: `knowledge/knowledge_qa/STANDARD/QA_CHECKLIST.md`

---

# 3.6 QG4 — Review Gate

| Check | Pass condition |
|-------|----------------|
| Domain Reviewer sign-off | On phase review |
| PASS units → Reviewed | Status updated |
| REVIEW items | Resolved or governance-waived |
| Borderline resolved | Human decision recorded |
| Cursor not sole approver | Human name on sign-off |

**Blocks:** Validation for unreviewed units.

Checklist: [CHECKLISTS.md](CHECKLISTS.md) § Review.

---

# 3.7 QG5 — Validation Gate

| Check | Pass condition |
|-------|----------------|
| Golden cases defined | Reasoning FREEZE exists for pack |
| Pinned units Validated | Golden ids pass validation |
| Evidence gates align | Catalog facts match Reasoning policy |
| No golden conflict | REVIEW/FAIL on pinned units resolved |
| Validation record archived | Per pack |

**Blocks:** Freeze for pack.

Checklist: [CHECKLISTS.md](CHECKLISTS.md) § Validation.

---

# 3.8 QG6 — Freeze Gate

| Check | Pass condition |
|-------|----------------|
| All production units Validated | 100% in scope |
| No open FAIL | Any topic |
| Catalog version bumped | VERSIONING rules |
| FREEZE_POLICY satisfied | QA Standard |
| Chief Reviewer sign-off | Pack freeze approval |
| CHANGELOG updated | Catalog + factory |

**Blocks:** Production load of catalog.

Checklist: [CHECKLISTS.md](CHECKLISTS.md) § Freeze.

---

# 3.9 QG7 — Release Gate

| Check | Pass condition |
|-------|----------------|
| Production smoke | Reasoning selects Frozen units on golden cases |
| Release version tagged | Per VERSIONING |
| Rollback plan | Prior Frozen version identified |
| Release notes | Customer-facing summary |
| Production Owner sign-off | Live config verified |
| Release Manager sign-off | Business release |

**Blocks:** Customer-visible announcement.

Checklist: [CHECKLISTS.md](CHECKLISTS.md) § Release.

---

# 3.10 Gate failure handling

| Failure | Action |
|---------|--------|
| QG1 fail | Return to Authoring |
| QG2 fail | Fix catalog; re-run QG2 |
| QG3 FAIL units | Authoring fix → re-QA |
| QG4 hold | Stay Draft/Reviewed |
| QG5 golden conflict | Reasoning or catalog fix |
| QG6 incomplete | Complete validation first |
| QG7 production fail | Rollback; do not release |

---

END
