# BTE Platform — Knowledge Changelog

All notable changes to BTE Platform **knowledge assets** (rules, sentences, templates, editorial content) are documented in this file.

Format inspired by [Keep a Changelog](https://keepachangelog.com/).  
Versioning follows [KNOWLEDGE_VERSIONING.md](KNOWLEDGE_VERSIONING.md).

Platform software releases: `docs/project/CHANGELOG.md`.

---

## [1.0.0] — 2026-07-27

**Knowledge baseline** aligned with BTE Platform **1.0.0 Production Stable**.

### Summary

Initial governed knowledge baseline for production pipeline V1.0. Executable rules in `database/` drive Pattern, Score, and Interpretation engines. Sentence libraries and report templates exist under `engines/interpretation_engine/knowledge/` for authoring and legacy export paths. Editorial feng shui knowledge in `knowledge_base/08_feng_shui/` with validators and quality checklist.

### Added

- **Knowledge governance** — `knowledge/docs/` official documentation set (architecture, versioning, authoring, quality, review)
- **Rule Database structure** — numbered `database/` domains: calendar, bazi, pattern, score (`13_score_engine`, `15_score_engine`), interpretation (`interpretation_rules/`)
- **Interpretation rule families** — career, wealth, health, marriage, luck, day master, five elements, feng shui, bazi basic, ten gods, useful god, etc.
- **Score engine rule trees** — strength, wuxing, ten gods, pattern, useful god, shensha, luck, final score grading
- **Sentence library schema** — `07_sentence_library/sentence_schema.json` v1.0.0 with 14 module folders
- **Report template schema** — `06_report_templates/template_schema.json` with 10 commercial modules
- **Editorial feng shui** — gua JSON (`01_gua/*.json`), `style_guide.md`, `editorial_rules.md`, `quality_checklist.md`, validators
- **Validation harness** — `knowledge_base/qa_validate.py`, `08_feng_shui/validate_all.py`
- **Production smoke alignment** — 105-case suite validates knowledge output on wire (no internal leaks)

### Changed

- Knowledge authoring centralized under governance (previously scattered READMEs only)
- Interpretation commercial output path: rules → `InterpretationResult` → `portal_view` → API (documented SSOT)

### Improved

- Cross-references between `docs/project/KNOWLEDGE_BASE_GUIDE.md` and `knowledge/docs/`
- Rule priority documented per score submodule READMEs
- Critical reference case 1987-01-21 validated in smoke and bazi regression tests

### Deprecated

- None at knowledge version 1.0.0 baseline (legacy narrative/report paths documented as non-production, not removed)

### Removed

- None — baseline preservation release

### Known gaps (tracked for V1.1+)

| Gap | Target |
|-----|--------|
| Golden dataset CI (`jsonschema`) | V1.1 |
| Calendar knowledge SSOT (`CalendarView`) | V1.1 |
| Sentence library on production hot path | V1.2 narrative |
| Report templates on production hot path | V1.3 PDF |
| Timezone-aware calendar knowledge | V1.1 (BUG-PROD-001) |

---

## [Unreleased]

Planned knowledge work — see `docs/project/PRODUCT_ROADMAP.md`:

- V1.0.x — patch rule prose, additive rules, coverage expansion
- V1.1 — golden dataset integration, calendar SSOT data, legacy cleanup
- V1.2 — sentence optimization, narrative enhancement data
- V1.3 — report template branding for PDF export

---

## Version index

| Knowledge version | Platform version | Date | Notes |
|-------------------|------------------|------|-------|
| 1.0.0 | 1.0.0 | 2026-07-27 | Initial governed baseline |

---

**Maintainers:** Update this file on every knowledge release. Link PR and domain reviewer.
