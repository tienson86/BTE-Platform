# Knowledge Compliance Report

| Item | Value |
|------|-------|
| Document | KNOWLEDGE_COMPLIANCE_REPORT.md |
| Project | BTE Platform V1.0 |
| Audit Type | Knowledge Compliance (READ-ONLY) |
| Primary executable root | `engines/interpretation_engine/knowledge/` |
| Governance root | `knowledge/` (docs only) |
| Date | 2026-07-28 |
| Constraints | No code / JSON / rename / patch |

---

## Executive Summary

The audited “Knowledge Root” named `knowledge/` contains **governance documentation only** (`docs/`, README). The **executable Knowledge Base** used by engines lives at:

`engines/interpretation_engine/knowledge/`

Against the requested module checklist (`01`–`08`), the tree is **structurally divergent**:

| Requested module | Actual status |
|------------------|---------------|
| 01_phrase_library | Present — **never loaded by runtime** |
| 02_dictionary | Present — legacy Style loader only |
| 03_terminology | Present — legacy Style loader only |
| 04_sentence_library | **Missing** (folder is `04_system_terms`) |
| 05_rule_database | Present — **production Interpretation path** |
| 06_report_templates | Present — **not used by production Report** |
| 07_examples | **Missing** (folder is `07_sentence_library`) |
| 08_metadata | **Missing** as top-level module |

**Production runtime** (Orchestrator → Interpretation → `render_from_analysis`) consumes primarily **`05_rule_database`** (495 matchable rules). Phrase, dictionary, terminology, sentence library, and report templates are largely **dead or legacy-path-only** relative to the commercial pipeline.

| Metric | Score |
|-------:|------|
| **Knowledge Health Score** | **42%** |

---

## Knowledge Health Score

| Dimension | Weight | Score | Notes |
|-----------|-------:|------:|-------|
| Folder integrity vs checklist | 15% | 40 | 3/8 names mismatch or missing |
| Version / schema presence | 10% | 70 | sentence + template schema 1.0.0; no global KB version file |
| Naming convention | 10% | 75 | Numbered folders OK inside engine knowledge |
| Loader reachability | 25% | 25 | Only rule DB on production path |
| Rule utilization (loaded→matched) | 20% | 22 | ~94/495 matched in 3-case spot check; historically ~22% on 10 cases |
| Asset quality (dup/broken JSON) | 10% | 65 | 1 broken dictionary JSON; 104 duplicate rule IDs |
| Template / sentence production use | 10% | 15 | Schemas exist; production Report bypasses templates |

**Composite Knowledge Health Score ≈ 42%**

---

## Folder Statistics

### A. Root `knowledge/` (requested root)

| Entry | Type | Role |
|-------|------|------|
| `docs/` | Directory | Architecture, versioning, authoring standards |
| `README.md` | File | Placeholder (`#knowledge`) |

**Executable modules under `knowledge/01…08`: 0**

Per `knowledge/docs/KNOWLEDGE_ARCHITECTURE.md`, root `knowledge/` is **T4 — verify loader paths**; production assets are under engine knowledge / `database/`.

### B. Executable tree `engines/interpretation_engine/knowledge/`

| Module | JSON files | Approx records | Unique IDs | Dup IDs | Parse errors |
|--------|----------:|---------------:|-----------:|--------:|-------------:|
| 01_phrase_library | 12 | 40–73* | 40+ | text dups ~9 | 0 |
| 02_dictionary | 25 | ~57–122* | 57 | 0 | **1** (`na_yin.json`) |
| 03_terminology | 6 | 319 | 317 | 2 | 0 |
| 04_system_terms | 1 | 0 countable | 0 | 0 | 0 |
| 05_rule_database | 48 | **2,526** | 2,375 | **104** | 0 (multi-JSON OK for KnowledgeRuleLoader) |
| 06_report_templates | 41 | 160 | 160 | 0 | 0 |
| 07_sentence_library | 57 | 196 | 196 | 0 | 0 |
| docs | — | — | — | — | — |
| **TOTAL** | **~190** | **~3,300+** | — | — | **1 hard** |

\* Counts vary by whether nested dict values are treated as records.

### C. Checklist integrity

| Check | Result |
|-------|--------|
| `04_sentence_library` | FAIL — actual `04_system_terms` |
| `07_examples` | FAIL — actual `07_sentence_library` |
| `08_metadata` | FAIL — no top-level module; per-module `metadata.json` inside sentence/template folders |
| Numbered `01…08` under rule DB | PASS (`01_strength` … `08_priority`) |
| Report template modules 01–10 | PASS (10 commercial modules) |
| Sentence modules 01–14 | PASS (14 modules + schema) |

---

## Coverage

### Runtime usage matrix

| Module | Loaded by runtime? | Which loader / path | Production Orchestrator? |
|--------|--------------------|---------------------|--------------------------|
| 01_phrase_library | **Never** | No Python reference found | No |
| 02_dictionary | **Legacy only** | `StyleKnowledgeLoader` (`report_engine/content/03_style`) | No |
| 03_terminology | **Legacy only** | same Style loader | No |
| 04_system_terms | **Never / empty** | No consumer found | No |
| 05_rule_database | **Yes** | `KnowledgeRuleLoader` via `InterpretationEngine` | **Yes** |
| 05 / 08_priority_rules | **Partial** | Conditions enter KnowledgeRuleLoader; PriorityRuleLoader unused on production (`for_matched_rules`) | Partial |
| 06_report_templates | **Legacy / WP6 build** | `KnowledgeTemplateLoader` → `ReportService.build_full` | **No** (`render_from_analysis`) |
| 07_sentence_library | **Legacy / Narrative** | `SentenceLibraryLoader`, Style loader labels | **No** |
| Root `knowledge/docs` | N/A | Human governance | N/A |

### Rule database funnel (spot check + prior 10-case audit)

| Stage | Count | Notes |
|-------|------:|-------|
| Disk records (all kinds) | 2,526 | rules/conditions/actions/labels/examples/priority |
| Matchable loaded | 495 | KnowledgeRuleLoader filter |
| Matched (union, 3-case spot) | 94 | Never matched ≈ 401 of loaded |
| Matched (union, prior 10-case) | 107 | ~21.6% of loaded |
| Resolved (prior 10-case) | 53 | Priority resolver discards ~half |
| Labels / examples skipped by design | 10 files | Soft-dead for matcher |
| Files with records but no conditions | 19 | Hard-dead for matcher |

### Rule family coverage (disk vs loaded)

| Family | Disk (approx) | Loaded (folder map) | Coverage note |
|--------|--------------:|--------------------:|---------------|
| 01 Strength | 162 rules | 12 | Most files lack matchable conditions |
| 02 Season | 147 | 15 | Same |
| 03 Temperature | 263 + labels/ex | 76 | cold_hot/humidity not matchable |
| 04 Pattern | 50 + aux | 55 | Strong relative load |
| 05 Special case | 230 + aux | 100 | Mostly conditions |
| 06 Follow | 600 | 97 | Actions/conditions/priority unused |
| 07 Combination | 500 | 100 | Conditions/priority unused |
| 08 Priority | 200 | 40 | conditions only; PR* loader broken/unused |

---

## Dead Knowledge

Knowledge that exists on disk but is **unreachable from production pipeline**:

| Asset | Why dead |
|-------|----------|
| Entire `01_phrase_library` | No importer |
| `04_system_terms/engine_terms.json` | No consumer; 0 countable records |
| `06_report_templates` on production Report | Orchestrator uses `render_from_analysis`, not template builder |
| `07_sentence_library` examples (`is_real_content: false`) | Schema illustrations; Narrative path not in Orchestrator |
| Root `knowledge/` (non-docs) | Empty of modules |
| `follow_pattern_actions.json` | No action executor |
| Strength/season JSON without conditions | Loader rejects (no_cond) |
| `humidity_rules.json`, `cold_hot_rules.json` as matcher input | No conditions; TEMP scores hardcoded in RuleContextBuilder instead |
| Priority `priority_rules.json` / order / labels via PriorityRuleLoader | Multi-JSON parse failure + production bypass |

**Estimated dead share (production lens):**  
~80% of engine-knowledge disk records never enter the production matcher; of the 495 that do, ~78% never match in sample cases.

---

## Unused Knowledge

| Category | Status |
|----------|--------|
| Unused phrases | **100%** of phrase library (never loaded) |
| Unused dictionaries | Loaded only if Style layer invoked — **unused on production Report** |
| Unused terminology | Same as dictionaries |
| Unused sentences | Examples explicitly non-real; selection path not on Orchestrator |
| Unused templates | 10 modules unused on production Report path |
| Unused rules (loaded but never matched) | ~388–401 / 495 |
| Unused metadata | Per-module `metadata.json` in sentence/template folders — not read by Interpretation production |
| Unused Priority examples/labels | Soft-skipped / Priority loader unused |

---

## Broken References

| Issue | Severity | Detail |
|-------|----------|--------|
| `02_dictionary/na_yin.json` | **High** | Invalid JSON (`Expecting ',' delimiter` ~line 161) |
| Checklist vs disk naming | **High** | `04_sentence_library`, `07_examples`, `08_metadata` not present |
| PriorityRuleLoader ↔ `priority_rules.json` | **High** | Extra data / multi-document JSON breaks strict `json.load` |
| Template `content_ref` → Interpretation fields | **Medium** | WP6 binding unused in production; risk latent if re-enabled |
| Sentence `schema_ref` paths | **Low** | Present; examples are illustrations only |
| Placeholder tokens in sentence examples | **Low** | Spot check found **0** `{{...}}` in aggregated example texts (examples are schema demos, not live templates) |
| Cross-rule ID orphans (ID-like refs) | **Low** | Prior audit: 0 orphan ID-like refs in scanned set; **104** duplicate IDs across KB |

---

## Priority Problems

| Priority issue | Impact |
|----------------|--------|
| Production uses `PriorityService.for_matched_rules()` | Does **not** load `08_priority_rules` Priority KB |
| `PriorityRuleLoader` fails on multi-JSON `priority_rules.json` | Blocks full Priority pipeline even if wired |
| Module `*_priority.json` (follow/combination/special) | Mostly no conditions → not loaded as matcher rules |
| Conflict resolution ≠ Priority Rule Database | Section/confidence capping only — contract divergence |

---

## Phrase Library

| Check | Result |
|-------|--------|
| Files | 12 JSON (opening, closing, transition, …) |
| Records | ~40 structured / ~73 including nested opening entries |
| Duplicate texts | ~9 duplicate text strings |
| Used at runtime | **0** — no code references |
| Conflicting | Not evaluable at runtime (never loaded) |
| Verdict | **Dead knowledge (authoring asset only)** |

---

## Sentence Library

| Check | Result |
|-------|--------|
| Location | `07_sentence_library` (not `04_sentence_library`) |
| Schema | `sentence_schema.json` v**1.0.0** |
| Modules | 14 (`01_intro` … `14_conclusion`) |
| Example records | 196 (many marked `is_real_content: false`) |
| Reachable on production Orchestrator | **No** |
| Reachable on Narrative / Style legacy | **Yes** (loader exists) |
| Never selected (production) | **All** |
| Duplicated IDs | 0 in inventory |
| Broken / missing placeholders | No `{{placeholders}}` found in example corpus; real selection path inactive |
| Verdict | **Schema-ready, production-unused** |

---

## Report Templates

| Check | Result |
|-------|--------|
| Location | `06_report_templates` |
| Schema | `template_schema.json` v**1.0.0** |
| Modules | 10 commercial modules |
| Referenced by | `KnowledgeTemplateLoader`, `ReportService.build_full`, coverage tools |
| Used by production Orchestrator | **No** (`ReportEngine.render_from_analysis`) |
| Unused (production) | **All 10 modules** |
| Broken references | Latent only (path unused); no live bind failures on production path |
| Verdict | **WP6-ready, production-bypassed** |

---

## Rule Database Detail

| Metric | Value |
|--------|------:|
| Total disk records | 2,526 |
| Matchable loaded | 495 |
| Matched (sample union) | 94–107 |
| Unused loaded | ~388–401 |
| Duplicate IDs (disk) | 104 |
| Conflicting rules | Resolved at runtime by MatchedRuleResolver (~50% discard); **not** by 08 Priority KB |

Family-level unused drivers: missing conditions, False combination/luck facts, humidity unused, follow actions never executed.

---

## Version

| Asset | Version signal |
|-------|----------------|
| Governance docs | Knowledge governance **1.0** / Platform **1.0.0** (`KNOWLEDGE_VERSIONING.md`) |
| Sentence schema | 1.0.0 |
| Template schema | 1.0.0 |
| Global `knowledge_version` file under executable KB | **Absent** |
| Per-rule `phien_ban` / examples_version | Present in some JSON families |

---

## Naming Convention

| Pattern | Compliance |
|---------|------------|
| `NN_name` folders under engine knowledge | Pass (01–07 + docs) |
| `NN_*_rules` under rule DB | Pass |
| Requested `04_sentence_library` / `07_examples` / `08_metadata` | **Fail** vs actual names |
| `snake_case` JSON filenames | Mostly pass |
| Multi-document concatenated JSON | Common; OK for KnowledgeRuleLoader; **breaks** PriorityRuleLoader |

---

## Recommendations

Recommendations only — **no implementation**.

1. **Clarify Knowledge Root SSOT**  
   Document that executable KB is `engines/interpretation_engine/knowledge/`, while `knowledge/` is governance — or relocate modules to match the checklist.

2. **Reconcile checklist naming**  
   Either rename folders to `04_sentence_library` / `07_examples` / `08_metadata`, or update architecture docs to the actual layout (`04_system_terms`, `07_sentence_library`).

3. **Decide fate of dead libraries**  
   Phrase / unused templates / unused sentences: wire into production, move to editorial (`knowledge_base/`), or mark explicitly as V1.2 deferred assets.

4. **Fix broken `na_yin.json`**  
   Dictionary integrity blocker.

5. **Align Report path with templates or deprecate WP6 on Orchestrator**  
   Avoid dual Report architectures (`render_from_analysis` vs `build_full`).

6. **Increase rule matchability**  
   Add conditions to strength/season tables **or** stop counting them as Interpretation matcher rules.

7. **Resolve Priority strategy**  
   Fix multi-JSON loader and wire 08 KB, or formally adopt MatchedRuleResolver as V1 Priority contract.

8. **Publish a single Knowledge version stamp**  
   e.g. `knowledge_version: 1.0.0` at executable root for release traceability.

9. **Do not expand Report Binding onto unused template/sentence layers** until ownership and loader paths are frozen.

---

## Final Assessment

| Question | Answer |
|----------|--------|
| Is Knowledge structure checklist-compliant? | **No** (naming + missing 07_examples / 08_metadata) |
| Is production Knowledge healthy? | **Partial** — rule DB works; most libraries idle |
| Knowledge Health Score | **42%** |
| Ready for Knowledge Freeze? | **PARTIALLY READY** |

Freeze recommendation: freeze **governance docs + rule DB schema intent**, but do **not** claim full module checklist compliance until structure alignment and dead-asset policy are decided.

---

*End of Knowledge Compliance Report*  
*READ-ONLY — no source or JSON was modified.*
