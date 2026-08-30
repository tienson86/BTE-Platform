# N-IMP-06 SUMMARY BUILDER REPORT

Sprint: N-IMP-06
Module: engines/narrative_v2/summary
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Summary Builder produces `OverviewSummary` from `CommercialRewriteContext` only.
It does not invent meaning, concatenate all domains, publish Presentation, or switch Dashboard.

---

## 2. Summary architecture

```
CommercialRewriteContext
        ↓
SummarySelector (one primary insight)
        ↓
Summary assembly (headline + body from rewrite units)
        ↓
SummaryValidator
        ↓
OverviewSummary
```

Logic lives in `engines/narrative_v2/summary/`.
Runtime only calls `build_summary`.

---

## 3. Files created

```
engines/narrative_v2/summary/__init__.py
engines/narrative_v2/summary/summary_builder.py
engines/narrative_v2/summary/summary_context.py
engines/narrative_v2/summary/summary_model.py
engines/narrative_v2/summary/summary_selector.py
engines/narrative_v2/summary/summary_formula.py
engines/narrative_v2/summary/summary_validator.py
engines/narrative_v2/summary/summary_errors.py
tests/narrative_v2/test_summary_builder.py
tests/narrative_v2/test_summary_model.py
tests/narrative_v2/test_summary_formula.py
tests/narrative_v2/test_summary_selector.py
tests/narrative_v2/test_summary_validator.py
tests/narrative_v2/test_summary_runtime_integration.py
tests/narrative_v2/test_summary_semantics.py
implementation/narrative_v2/n_imp_06/case0001_summary_review.md
implementation/narrative_v2/n_imp_06/case0001_summary_trace.json
implementation/narrative_v2/n_imp_06/summary_contract_gaps.md
implementation/narrative_v2/N_IMP_06_REPORT.md
```

---

## 4. Files modified

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
tests/narrative_v2/test_runtime_skeleton.py
tests/narrative_v2/test_evidence_runtime_integration.py
tests/narrative_v2/test_reasoning_runtime_integration.py
tests/narrative_v2/test_knowledge_runtime_integration.py
tests/narrative_v2/test_rewrite_runtime_integration.py
```

Later-stage skip lists now execute `build_summary` before remaining `NotImplemented` stages.

---

## 5. Builder input

`CommercialRewriteContext` only.

Rejected: CanonicalAnalysis, EvidenceContext, ReasoningContext, KnowledgeContext, Pack05, Portal, Dashboard, Report prose.

---

## 6. OverviewSummary contract

Public fields:

- headline
- summary
- identity
- balance
- conclusion
- references
- metadata
- status

No extra public fields.

Status values: `complete` | `partial` | `insufficient` | `invalid`.

---

## 7. Executive Summary Formula

Implemented as:

```
Rewrite Units
        ↓
Insight Selection
        ↓
Summary Assembly
        ↓
OverviewSummary
```

Evidence / Insight / Meaning / Rewrite already exist upstream. This sprint does not re-run them.

Join rule: whitespace between already-complete rewrite sentences. No invented domain meaning. No “Bạn có nội lực tốt” unless present in RewriteContext.

---

## 8. Insight selection

Deterministic order:

1. registered `CORE_SEMANTIC_PRIORITY` (`core.pattern_context` first)
2. registered `DOMAIN_PRIORITY` (`pattern` before `strength`)
3. `rewrite_id` as tie-break
4. no core rewrite unit → `insufficient`

ShenSha (`boundary.approved_rule_unavailable`) is never primary.
Ten gods are not concatenated into the overview.

Exactly one primary rewrite unit. At most one supporting unit on the same semantic key.

---

## 9. Headline generation

First sentence of the primary rewrite unit, if ≤ 25 words.

Otherwise `headline = None`. No invented headline library.

CASE-0001: `Bạn có chỗ dưỡng, chịu được việc cần nền.`

---

## 10. Summary assembly

Remaining primary sentences + first sentence of the supporting unit.

Target 2–4 sentences. No Action. No ten-gods/shensha dump.

CASE-0001 body: pattern remainder + strength first sentence.

---

## 11. Identity handling

`identity = None`.

No dedicated customer-safe identity rewrite. Not rebuilt from UI-04 badges. Not copied from the primary insight (would duplicate).

---

## 12. Balance handling

`balance = None`.

Useful God and Temperature remain unresolved from N-IMP-05. Not mapped locally.

---

## 13. Conclusion handling

`conclusion = None`.

No unused approved sentence that could synthesize without duplication or new recommendation.

---

## 14. Sentence Library handling

Runtime gap unchanged. No local sentence library invented.

Connectors: sentence split + space join only.

---

## 15. Duplicate handling

Identical full-field wording is rejected by the validator.

Headline is removed from the summary body when it is the first primary sentence.

Empty supporting fields are preferred over duplicated copy.

---

## 16. Validation

`SummaryValidator` checks:

- exactly one primary insight (unless insufficient)
- source traceability to rewrite ids
- customer-safe language
- no raw technical ids / JSON
- no prediction / Action / forbidden claims
- length bounds
- no identical field wording

Invalid contract → `SummaryValidationError`.

---

## 17. Traceability

Each populated field traces:

```
rewrite_id → knowledge_id → reasoning_id → evidence_id
```

CASE-0001: `implementation/narrative_v2/n_imp_06/case0001_summary_trace.json`

---

## 18. Runtime integration

```
initialize
↓
build_evidence = IMPLEMENTED
↓
build_reasoning = IMPLEMENTED
↓
resolve_knowledge = IMPLEMENTED
↓
commercial_rewrite = IMPLEMENTED
↓
build_summary = IMPLEMENTED
↓
build_interpretation = NotImplemented
↓
build_action = NotImplemented
↓
build_commercial = NotImplemented
↓
validate
↓
publish
```

`NarrativeRuntimeResult.presentation` remains `None`.
`OverviewSummary` is stored on `NarrativeRuntimeContext.summary` only.

---

## 19. CASE-0001 Summary

status: `partial`

headline: Bạn có chỗ dưỡng, chịu được việc cần nền.

summary: Hữu ích khi cần ủ và học có khung. Bạn có nền lực để chịu tải, hoàn thành việc dài, giữ nhịp khi môi trường đòi hỏi sức bền.

identity: none

balance: none

conclusion: none

Not a Strength + Pattern + Ten Gods + ShenSha concatenation.

---

## 20. CASE-0001 primary insight

`rewrite.pattern.chinh_an.001` (`core.pattern_context`).

Supporting: `rewrite.strength.strong.001`.

---

## 21. CASE-0001 source trace

headline → `rewrite.pattern.chinh_an.001` → `knowledge.pattern.chinh_an` → `reasoning.observation/relation.core.pattern_context` → `evidence.strength.level`, `evidence.pattern.primary`, `evidence.pattern.cach_cuc`

summary → those plus `rewrite.strength.strong.001` / `knowledge.strength.strong`

---

## 22. Contract gaps

`implementation/narrative_v2/n_imp_06/summary_contract_gaps.md`

Tracked: sentence library, headline assets, identity semantics, balance semantics, useful god, temperature, luck.

---

## 23. Tests

```
py -m pytest tests/narrative_v2 -q
181 passed
```

S1–S20 covered. Negative tests: raw bypass terms and forbidden generated claims.

---

## 24. Determinism verification

Same `CommercialRewriteContext` → same `OverviewSummary`.

Selector result is independent of input array order.

---

## 25. Shadow mode verification

```
SHADOW_MODE = True
replaces_pack05 = False
portal_connected = False
presentation = None
```

Dashboard still reads current production sources.

---

## 26. Out-of-scope confirmation

No Interpretation Builder implemented: YES
No Action Builder implemented: YES
No Presentation Contract published: YES
No Portal integration: YES
No Pack05 replacement: YES
No astrology engine modified: YES
No new approved knowledge invented: YES
No direct UI prose reused: YES

---

## 27. Verdict

READY FOR PRODUCT OWNER REVIEW
