# BTE Platform — Knowledge Base Guide

**Version:** 1.0.0  
**Last updated:** 2026-07-27

This guide describes how BTE Platform knowledge assets are organized, validated, versioned, and approved. Engines consume knowledge **read-only**; business rules are data, not Python `if/else` chains.

---

## Knowledge architecture overview

```
database/              — Primary rule CSVs (engines load at runtime)
knowledge/             — Report templates, sentence libraries (WP6/WP7)
knowledge_base/        — Editorial knowledge (e.g. feng shui gua JSON, style guides)
```

| Layer | Purpose | Consumers |
|-------|---------|-----------|
| **Rule Database** | Executable rules (match, score, interpret) | Pattern, Score, Interpretation engines |
| **Phrase / Sentence Library** | Narrative transitions, tone (legacy WP7) | Narrative engine (off production path in 1.0.0) |
| **Report templates** | Section structure, module titles | Report Engine template path (legacy full build) |
| **Editorial knowledge** | Reference content, style, QA | Authors, validators — not direct engine input unless wired |

**Principle:** If a rule affects customer-facing output, it should live in **database** or approved knowledge files — not hard-coded in Python.

---

## Rule Database (`database/`)

### Structure

Numbered folders reflect pipeline domains:

| Area | Typical path | Engine |
|------|--------------|--------|
| Calendar / lunar | `01_calendar/`, related | Calendar |
| Bazi | `02_bazi/`, `09_hidden_stems/` | Bazi |
| Pattern | `14_pattern/` | Pattern |
| Score | `13_score_engine/`, `15_score_engine/` | Score |
| Interpretation | `interpretation_rules/`, `07_rule_database/` | Interpretation |

### File rules

- **CSV first** — preferred format for rules
- **Vietnamese naming** — snake_case, no diacritics in filenames
- **One file, one purpose** — e.g. strength rules separate from pattern rules
- **Stable schema** — add columns; do not rename/remove columns without migration
- **No duplicate rules** — reference existing keys

See `.cursor/rules/database.mdc`.

### Rule priority

When multiple rules apply:

1. Use **priority** column in CSV — not file read order
2. Higher priority wins per engine matcher design
3. Document new priority columns in folder `README.md`

Engines must not invent priority in code.

---

## Phrase library & sentence library

| Location | Role |
|----------|------|
| `knowledge/` sentence modules | WP7 narrative transitions |
| Interpretation output | Primary commercial prose in 1.0.0 |

**Production path (1.0.0):** Interpretation sentences from rule database; report/narrative markdown from interpretation sections via Report Engine `portal_view`.

Sentence libraries are for **future narrative enhancement (V1.2)** — not production SSOT today.

---

## Dictionary & terminology

- Domain terms use **Vietnamese** commercial labels in Portal (e.g. Thập thần, Nap âm)
- Internal keys may be English snake_case in CSV
- `knowledge_base/` style guides define editorial terminology:
  - `knowledge_base/08_feng_shui/style_guide.md`
  - `knowledge_base/08_feng_shui/editorial_rules.md`

**Portal label maps** (e.g. `PATTERN_LABELS` in JS) are display only — API sends canonical fields.

---

## Report templates (`knowledge/06_report_templates`)

- Define report module order and titles
- Used by `ReportService.build()` / `ReportBuilder` (legacy full ReportModel path)
- Production API uses `portal_view` from interpretation — templates not on hot path in 1.0.0

Changes here affect export/PDF path (V1.3) more than live Portal analyze.

---

## Editorial knowledge (`knowledge_base/`)

Example: `knowledge_base/08_feng_shui/01_gua/*.json`

| Content | Validation |
|---------|------------|
| Gua definitions | `knowledge_base/08_feng_shui/validator.py` |
| Quality checklist | `quality_checklist.md` |
| Schema | `schema.json` |

Run validation:

```powershell
py -3.13 knowledge_base/08_feng_shui/validate_all.py
```

---

## Validation workflow

### Before committing knowledge changes

1. **Schema / CSV validation** — run folder validator or loader tests
2. **No duplicate keys** — check CSV uniqueness
3. **Reference integrity** — foreign keys exist
4. **Module regression** — engine tests for affected domain
5. **Smoke** — if interpretation/score output changes materially

### Golden Dataset

- Do **not** edit golden expected files to match new rules without domain approval
- Golden Dataset is QA gate — not auto-updated

### Production smoke

- Critical reference case `1987-01-21` must remain PASS after calendar/bazi changes
- Add new edge cases to `validation/production_smoke_runner.py` when fixing boundary bugs

---

## Review workflow

| Step | Owner | Action |
|------|-------|--------|
| 1. Author | Domain expert | Propose CSV/JSON change with rationale |
| 2. Technical review | Engineer | Loader compatibility, no schema break |
| 3. Domain review | Bát tự reviewer | Correctness of rules/phrases |
| 4. QA | Smoke / regression | Automated checks green |
| 5. Approval | Product / lead | Merge per CONTRIBUTING.md |

**Documentation:** Note knowledge changes in `CHANGELOG.md` (patch release).

---

## Versioning of knowledge

| Change type | Version bump | Example |
|-------------|--------------|---------|
| Typo in phrase | Patch | 1.0.1 |
| New rules (additive) | Patch | 1.0.2 |
| Rule logic change (same schema) | Patch + regression | 1.0.3 |
| CSV schema change (new columns) | Minor if API unaffected | 1.1.0 |
| Breaking schema rename | Major or migration | 2.0.0 |

Track `database_version` in project docs when large rule sets ship together.

---

## Approval process

### Standard knowledge PR

- [ ] CSV/schema validation pass
- [ ] Engine loader reads without error
- [ ] Module tests pass
- [ ] Domain reviewer sign-off (for rule content)
- [ ] CHANGELOG entry

### Emergency rule fix (production wrong interpretation)

- `hotfix/*` branch
- Minimal CSV change
- Smoke + interpretation module tests
- Patch release per `VERSION_POLICY.md`

---

## Quality requirements

| Requirement | Standard |
|-------------|----------|
| Commercial prose | No internal rule IDs on wire (`FPR`, `PSC`, etc.) |
| Sanitization | Interpretation `portal_view` strips debug text |
| Completeness | Required CSV columns populated |
| Consistency | Terminology matches style guide |
| Priority | Documented and stable |

See `knowledge_base/08_feng_shui/quality_checklist.md` for editorial QA patterns.

---

## Forbidden

- Hard-coding rule text in Python instead of database
- Engines writing/updating CSV at runtime
- Changing Golden Dataset expected output without approval
- Removing rule files without deprecation path

---

## Related documents

| Document | Topic |
|----------|-------|
| `.cursor/rules/database.mdc` | Database rules for AI/engine dev |
| `docs/project/VERSION_POLICY.md` | Release when knowledge ships |
| `docs/project/CODING_STANDARDS.md` | No hard-coded rules |
| `database/README.md` | Database root |

---

**BTE Platform Knowledge Base Guide — 1.0.0 — 2026-07-27**
