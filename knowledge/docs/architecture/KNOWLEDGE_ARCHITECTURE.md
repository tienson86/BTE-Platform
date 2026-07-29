# BTE Platform — Knowledge Architecture

| Field | Value |
|-------|-------|
| **Governance version** | 1.0 |
| **Platform version** | 1.0.0 |
| **Last updated** | 2026-07-27 |
| **Status** | Official reference |

---

## Purpose

This document defines how all knowledge assets in BTE Platform are organized, how they relate to the production pipeline, and how they evolve over time. Knowledge is **data** — engines read it; they do not author it at runtime.

**Architecture V1.0 is frozen.** Knowledge governance may expand content and schemas additively without changing pipeline order or API contracts.

---

## Knowledge hierarchy

```
                    ┌─────────────────────────────┐
                    │   Editorial & reference     │
                    │   knowledge_base/           │
                    └──────────────┬──────────────┘
                                   │ reference / style
                    ┌──────────────▼──────────────┐
                    │   Executable Rule Database  │
                    │   database/                 │
                    └──────────────┬──────────────┘
                                   │ match / score / interpret
          ┌────────────────────────┼────────────────────────┐
          │                        │                        │
┌─────────▼─────────┐   ┌──────────▼──────────┐   ┌────────▼────────┐
│ Sentence Library  │   │ Report Templates    │   │ Phrase /        │
│ 07_sentence_*     │   │ 06_report_templates │   │ transition libs │
└─────────┬─────────┘   └──────────┬──────────┘   └────────┬────────┘
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   Engines (read-only)       │
                    │   Pattern / Score /         │
                    │   Interpretation / Report   │
                    └──────────────┬──────────────┘
                                   │
                    ┌──────────────▼──────────────┐
                    │   AnalysisResult → API      │
                    │   → Portal (render only)    │
                    └─────────────────────────────┘
```

### Tier summary

| Tier | Location | Role in production 1.0.0 |
|------|----------|---------------------------|
| **T1 — Rule Database** | `database/` | **Primary** — drives pattern, score, interpretation |
| **T2 — Engine knowledge** | `engines/*/knowledge/` | Templates, sentence libraries — partial / legacy paths |
| **T3 — Editorial** | `knowledge_base/` | Reference, style, feng shui gua — validation & authoring |
| **T4 — Root knowledge** | `knowledge/` | Shared templates if present — verify loader paths |

---

## Rule Database (`database/`)

**Purpose:** Authoritative executable rules for engines.

**Format:** CSV first (JSON/YAML only when schema-approved).

**Structure:** Numbered folders by domain:

| Domain | Examples | Consumer engine |
|--------|----------|-----------------|
| Calendar / lunar | `01_calendar/` | Calendar |
| Bazi | `02_bazi/`, `09_hidden_stems/` | Bazi |
| Analysis sections | `05_phan_tich/` | Interpretation (reference) |
| Pattern | `14_pattern/` | Pattern |
| Score | `13_score_engine/`, `15_score_engine/` | Score |
| Interpretation | `interpretation_rules/` | Interpretation |

**Access:** Engine **Loaders** only — no direct CSV reads in business logic.

**Keys:** `rule_id` is the primary identifier across rule families where defined.

---

## Phrase library

**Purpose:** Short phrases, labels, and transition text for narrative polish.

| Location | Status (1.0.0) |
|----------|----------------|
| `engines/narrative_engine/` sentence loaders | Legacy — not production orchestrator path |
| `engines/interpretation_engine/knowledge/07_sentence_library/` | Schema + examples; supports interpretation authoring |

**Production path:** Commercial prose in 1.0.0 comes primarily from **interpretation rules** → `portal_view` sanitization → report markdown.

Phrase libraries support **V1.2 narrative enhancement** — see `docs/project/PRODUCT_ROADMAP.md`.

---

## Dictionary

**Purpose:** Canonical term definitions — elements, ten gods, patterns, shensha, nap am.

| Source | Role |
|--------|------|
| `database/` enum / lookup CSVs | Engine resolution |
| `knowledge_base/` style guides | Authoring consistency |
| Portal `STEM_META`, label maps | Display only — not SSOT |

**Rule:** API sends canonical Vietnamese commercial labels; dictionary CSVs define engine truth.

---

## Sentence library (`07_sentence_library`)

**Location:** `engines/interpretation_engine/knowledge/07_sentence_library/`

**Schema:** `sentence_schema.json` — `sentence_id`, `module`, `category`, `priority`, `tone`, `text`, etc.

**Modules:** Numbered folders (`01_intro` … `14_conclusion`) aligned with interpretation sections.

**Files per module:**

- `metadata.json` — module identity
- `sentence_index.json` — catalog
- `sentence_labels.json` — display labels
- `sentence_examples.json` — example sentences (authoring)

**Consumer:** Interpretation sentence generation / future narrative layers.

---

## Report templates (`06_report_templates`)

**Location:** `engines/interpretation_engine/knowledge/06_report_templates/`

**Schema:** `template_schema.json`

**Modules:** `01_summary`, `02_personality`, `03_career`, … `10_yearly_fortune`

**Consumer:** `ReportService.build()` / `ReportBuilder` — **legacy full ReportModel path**

**Production 1.0.0:** API report JSON from `ReportEngine.portal_view` (interpretation sections) — templates not on hot path.

**Future:** PDF export (V1.3) may reactivate template-driven layout.

---

## Terminology

| Layer | Convention |
|-------|------------|
| File names | Vietnamese concept, **no diacritics**, `snake_case` |
| `rule_id` | Prefix + number (e.g. `CA001`, `FPR012`) — family-specific |
| `sentence_id` | `module_snake_###` per `sentence_schema.json` |
| Commercial text | Vietnamese with diacritics in CSV/JSON content |
| Internal keys | English `snake_case` in conditions where engine expects |

**Editorial authority:** `knowledge_base/08_feng_shui/style_guide.md`, `editorial_rules.md`, `quality_checklist.md`

---

## Priority rules

When multiple rules or sentences match:

| Asset type | Priority mechanism |
|------------|-------------------|
| Interpretation CSV | `priority` column + engine priority resolution |
| Score CSV | `*_priority.csv` files per submodule |
| Pattern | `priority` on `PatternResult` / pattern priority tables |
| Sentence library | `priority` field in schema — higher wins |

**Forbidden:** File load order as implicit priority.

**Documentation:** Each folder `README.md` must state priority column meaning and scale (e.g. 0–100).

---

## Knowledge dependencies

```
RuleContext signals (from Pattern)
        ↓
Score rules (read bazi, pattern, strength signals)
        ↓
Interpretation rules (read score, pattern, bazi sections)
        ↓
InterpretationResult.sentences
        ↓
Report portal_view (sections → markdown/html)
```

| Dependency | Rule |
|------------|------|
| Score → Pattern | Score reads RuleContext; does not rebuild pattern |
| Interpretation → Score | Conditions reference score signals in RuleContext |
| Report → Interpretation | Report reads `AnalysisResult.interpretation` only |
| Editorial → Rules | Style guides inform authoring; not runtime unless wired |

**Cross-reference integrity:** Foreign keys in CSV (enum values, rule_id refs) must resolve — see `DATA_QUALITY_STANDARD.md`.

---

## Knowledge lifecycle

```
Propose → Draft → Validate → Technical review → Domain review
    → Approve → Release (version bump) → Monitor → Retire
```

| Stage | Owner | Artifact |
|-------|-------|----------|
| **Propose** | Domain / product | Issue, rationale |
| **Draft** | Rule author | Branch, CSV/JSON edits |
| **Validate** | Engineering | Loader tests, schema validators |
| **Technical review** | Engineer | PR — schema, no loader break |
| **Domain review** | Bát tự expert | Correctness of prose and logic |
| **Approve** | Knowledge lead | Sign-off on `KNOWLEDGE_REVIEW_PROCESS.md` |
| **Release** | Release engineer | `KNOWLEDGE_CHANGELOG.md`, platform patch if needed |
| **Monitor** | QA | Smoke, golden dataset, coverage reports |
| **Retire** | Knowledge lead | Deprecate rule_id; do not delete without migration |

Retired rules: mark `status=deprecated` in metadata or remove from active CSV with changelog entry — never silent delete.

---

## Production vs non-production knowledge paths

| Path | Production 1.0.0 |
|------|------------------|
| `database/interpretation_rules/*.csv` | **Yes** |
| `database/15_score_engine/**` | **Yes** |
| `database/14_pattern/**` | **Yes** |
| `interpretation_engine/portal_view.py` | **Yes** (code, not knowledge) |
| `07_sentence_library` examples | Authoring / future |
| `06_report_templates` | Legacy ReportModel build |
| `knowledge_base/08_feng_shui/*.json` | Reference; Feng Shui engine if wired |

---

## Related documents

| Document | Topic |
|----------|-------|
| [KNOWLEDGE_VERSIONING.md](KNOWLEDGE_VERSIONING.md) | Version bumps |
| [RULE_AUTHORING_STANDARD.md](RULE_AUTHORING_STANDARD.md) | Writing rules |
| [DATA_QUALITY_STANDARD.md](DATA_QUALITY_STANDARD.md) | Quality gates |
| [KNOWLEDGE_REVIEW_PROCESS.md](KNOWLEDGE_REVIEW_PROCESS.md) | Review workflow |
| [../docs/project/KNOWLEDGE_BASE_GUIDE.md](../../docs/project/KNOWLEDGE_BASE_GUIDE.md) | Platform-level guide |

---

**BTE Knowledge Architecture — Governance 1.0 — 2026-07-27**
