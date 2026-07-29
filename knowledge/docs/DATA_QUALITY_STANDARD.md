# BTE Platform — Data Quality Standard

| Field | Value |
|-------|-------|
| **Governance version** | 1.0 |
| **Last updated** | 2026-07-27 |

---

## Purpose

Defines measurable quality requirements for all knowledge assets: Rule Database CSVs, sentence libraries, report templates, and editorial JSON.

---

## Completeness

### Required completeness

| Asset | Requirement |
|-------|-------------|
| **rule_id** | 100% populated; unique per family |
| **condition** (executable rules) | 100% populated unless documented catch-all |
| **Commercial text fields** | No empty `recommendation` / `body` on active high-priority rules |
| **priority / score** | Populated where module uses resolution |
| **Foreign keys** | Enum values must exist in reference tables |
| **JSON schemas** | All `required: true` fields present per `sentence_schema.json` / `template_schema.json` |

### Module README

Every `database/` submodule with CSV files must have:

- Column list and meanings
- Priority scale explanation
- Example row
- Last review date

### Coverage targets (aspirational)

| Domain | Target (V1.x) |
|--------|----------------|
| Interpretation sections | Each Portal section has ≥1 active rule path |
| Score dimensions | All published dimensions have weight + priority files |
| Pattern codes | Main patterns in `14_pattern/` documented |
| Sentence library | Each module has `metadata.json` + index |

Gaps logged in knowledge backlog — not hidden.

---

## Consistency

### Terminology consistency

- Same concept → same Vietnamese label across files (e.g. Dụng thần, not mixed synonyms)
- Align with `knowledge_base/08_feng_shui/style_guide.md` and `editorial_rules.md`
- Ten god, nap am, element names match `database/` lookup tables

### Structural consistency

- Same column order within a file family across releases (append columns at end only)
- Same `rule_id` prefix conventions per file
- Section keys match `interpretation_engine/portal_view.py` `SECTION_ORDER` where applicable

### Cross-file consistency

- Score weights align with score rule outcomes
- Interpretation conditions reference signals that Score/Pattern actually produce
- No contradictory rules at same priority (see Conflict resolution)

---

## Duplicate detection

### Hard duplicates (reject)

| Type | Detection |
|------|-----------|
| Duplicate `rule_id` | Same file or cross-file within family |
| Duplicate `sentence_id` | Sentence index validation |
| Identical condition + identical prose | Hash or manual review |

### Soft duplicates (review)

| Type | Action |
|------|--------|
| Near-identical commercial prose | Merge or differentiate conditions |
| Overlapping conditions same priority | Lower one rule or narrow conditions |
| Same rule in two CSV files | Consolidate to single SSOT file |

**Tooling:** Folder validators, `knowledge_base/qa_validate.py`, manual PR review.

---

## Conflict resolution

When two rules match the same chart with incompatible messages:

| Step | Action |
|------|--------|
| 1 | Identify conflicting `rule_id` pair |
| 2 | Compare priority — higher wins per engine |
| 3 | If same priority, adjust priority or narrow conditions |
| 4 | Document resolution in PR and `KNOWLEDGE_CHANGELOG` |
| 5 | Add smoke or module test case if regression risk |

**Score conflicts:** Use submodule `*_priority.csv` and weight tables.

**Interpretation conflicts:** Interpretation engine priority resolution — authors must not rely on file order.

---

## Coverage targets

### Production smoke alignment

Critical reference cases must PASS after knowledge changes affecting calendar/bazi:

- `1987-01-21 03:30` — Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần

### Interpretation coverage

| Metric | Measurement |
|--------|-------------|
| Section coverage | `section_count` > 0 on smoke cases |
| Internal leak | No `FPR`, `matched_rule_count` on API wire |
| Empty sections | Flag if `sections[]` empty on full analyze |

### Score coverage

| Metric | Measurement |
|--------|-------------|
| `success: true` on smoke | Required |
| Grade populated | When rules active |

### Template / sentence coverage (non-production path)

- `template_coverage` in legacy ReportModel — reference only for V1.3 PDF work

---

## Review checklist

Use before approving any knowledge PR:

### CSV rules

- [ ] UTF-8 encoding verified
- [ ] `rule_id` unique
- [ ] No empty required columns
- [ ] Conditions syntactically valid
- [ ] No internal codes in customer-facing columns
- [ ] Priority documented if changed
- [ ] Folder README updated if schema changed
- [ ] Cross-references resolve (enums, signals)
- [ ] No duplicate prose (soft dup check)
- [ ] Domain reviewer approved prose

### JSON knowledge (sentence / template)

- [ ] Validates against `sentence_schema.json` / `template_schema.json`
- [ ] `sentence_id` / template id pattern match
- [ ] `module` matches folder `metadata.json`
- [ ] `status` field correct (`active` / `draft` / `deprecated`)

### Editorial (`knowledge_base/`)

- [ ] `knowledge_base/08_feng_shui/validator.py` or `validate_all.py` pass
- [ ] Quality checklist sections addressed
- [ ] No broken JSON schema

### Release gates

- [ ] Module pytest pass for affected engine
- [ ] `validation/production_smoke_runner.py` PASS (if output impact)
- [ ] `KNOWLEDGE_CHANGELOG.md` entry prepared
- [ ] Version bump per `KNOWLEDGE_VERSIONING.md`

---

## Quality metrics (reporting)

| Metric | Source |
|--------|--------|
| Smoke pass rate | `validation/production_smoke_raw.json` |
| Rule count per file | CSV line count |
| Deprecated rule count | Metadata / changelog |
| Open quality issues | Knowledge PR backlog |

Quarterly knowledge health review recommended for V1.1+.

---

## Related documents

- [RULE_AUTHORING_STANDARD.md](RULE_AUTHORING_STANDARD.md)
- [KNOWLEDGE_REVIEW_PROCESS.md](KNOWLEDGE_REVIEW_PROCESS.md)
- [KNOWLEDGE_VERSIONING.md](KNOWLEDGE_VERSIONING.md)
- `knowledge_base/08_feng_shui/quality_checklist.md`

---

**BTE Data Quality Standard — 1.0 — 2026-07-27**
