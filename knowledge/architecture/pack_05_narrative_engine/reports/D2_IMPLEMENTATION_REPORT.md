# D2 — Narrative Composer Implementation Report

Version: 1.0

Status: COMPLETE — Sprint D2

Pack: 05 (Narrative Engine)

Date: 2026-08-08

---

# 1. Scope

Transform **NarrativeTree → NarrativeResult**.

Input: NarrativeTree + Writing System constraints (Sprint C) + factual sources.

Output: **NarrativeResult**.

Does **not** start Report Engine.

Does **not** invent analytical facts.

---

# 2. Implemented Modules

Location: `engines/narrative_engine/composer/`

| Module | Responsibility |
|--------|----------------|
| `models.py` | Pack 05 NarrativeResult / Section / Paragraph / Recommendation / Summary |
| `constants.py` | Approved insufficient narrative + titles/tones |
| `source_bundle.py` / `source_factory.py` | Traceable SourceFact from Analysis / Interpretation |
| `language_rules.py` | Language Rule Engine (Sprint C forbidden wording) |
| `tone_resolver.py` | Tone Resolver |
| `sentence_composer.py` | Sentence Composer (source-only) |
| `paragraph_builder.py` | Pack05 Paragraph Builder |
| `section_composer.py` | Section Composer |
| `recommendation_composer.py` | Recommendation Composer |
| `executive_summary_composer.py` | Executive Summary Composer |
| `result_validator.py` | Narrative Validator (result) |
| `composer.py` | NarrativeResultComposer orchestration |

Public API:

- `NarrativeResultComposer.compose(tree, analysis=, interpretation=) -> NarrativeResult`
- `NarrativeEngine.compose_narrative_result(...)` (D1 tree + D2 result)

---

# 3. Traceability Contract

Every non-insufficient sentence traces through:

```
Interpretation / Evidence values
  → SourceFact (label/value/raw_text + rule_refs + knowledge_refs)
  → NarrativeParagraph / NarrativeRecommendation
```

Fields on output units:

- `evidence_refs`
- `interpretation_refs`
- `rule_refs`
- `knowledge_refs`

Technical Interpretation prose is rejected by commercial_ok + Language Rule Engine.

Insufficient nodes emit:

`Chưa đủ dữ liệu để đưa ra kết luận.`

---

# 4. Writing System Application

| Sprint C doc | Runtime application |
|--------------|---------------------|
| Writing Style Guide | Consultant framing prefixes only; no new claims |
| Tone of Voice | `ToneResolver` metadata per section |
| Sentence Structure | One primary paragraph / role; first-sentence truncation |
| Paragraph Structure | One role per paragraph |
| Wording Rules | `LanguageRuleEngine` forbidden patterns |

No free-form NLG templates. No invented conclusions.

---

# 5. Backward Compatibility

| Item | Status |
|------|--------|
| D1 NarrativeTree API | Unchanged |
| WP7 `compose` / NarrativeReport | Unchanged |
| WP7 `NarrativeParagraph` | Distinct from Pack05 paragraph model |

---

# 6. Tests

`pytest tests/narrative_engine -q` → **13 passed**

---

# 7. Stop

Sprint D2 complete. Report Engine not started.

---

END
