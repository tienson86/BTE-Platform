# N-IMP-05 COMMERCIAL REWRITE ENGINE REPORT

Sprint: N-IMP-05
Module: engines/narrative_v2/rewrite
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Commercial Rewrite produces customer-language **units** from approved
source meaning. It does not invent meaning, assemble Narrative, or
publish Presentation.

---

## 2. Rewrite source audit

Used:

- `knowledge/narrative_v2/09_LANGUAGE_STANDARD.md`
- `knowledge/narrative_v2/13_COMMERCIAL_REWRITE_ENGINE.md` strategy matrix
- Approved `positive_meaning` on traced interpretation domain JSON
  (`metadata.status = approved`)

Not used: Pack05, Portal, Dashboard copy, package sentence meta-texts,
CanonicalAnalysis.

---

## 3. Sentence library runtime audit

`implementation/narrative_v2/n_imp_05/sentence_library_runtime_audit.md`

**SENTENCE LIBRARY RUNTIME GAP**

Selector interface exists. `select()` returns None. No library invented.

---

## 4. Rewrite architecture

```
NarrativeKnowledgeContext
        ↓
RewriteEngine
        ↓
CommercialRewriteContext
```

Logic lives in `engines/narrative_v2/rewrite/`.
Runtime only calls `commercial_rewrite`.

---

## 5. Files created

```
engines/narrative_v2/rewrite/__init__.py
engines/narrative_v2/rewrite/rewrite_engine.py
engines/narrative_v2/rewrite/rewrite_context.py
engines/narrative_v2/rewrite/rewrite_item.py
engines/narrative_v2/rewrite/rewrite_strategy.py
engines/narrative_v2/rewrite/rewrite_registry.py
engines/narrative_v2/rewrite/rewrite_selector.py
engines/narrative_v2/rewrite/rewrite_validator.py
engines/narrative_v2/rewrite/rewrite_errors.py
engines/narrative_v2/rewrite/language_profile.py
engines/narrative_v2/rewrite/sentence_selector.py
tests/narrative_v2/test_rewrite_engine.py
tests/narrative_v2/test_rewrite_context.py
tests/narrative_v2/test_rewrite_validator.py
tests/narrative_v2/test_rewrite_language.py
tests/narrative_v2/test_rewrite_semantics.py
tests/narrative_v2/test_rewrite_runtime_integration.py
tests/narrative_v2/test_rewrite_determinism.py
implementation/narrative_v2/n_imp_05/sentence_library_runtime_audit.md
implementation/narrative_v2/n_imp_05/case0001_rewrite_trace.json
implementation/narrative_v2/n_imp_05/rewrite_contract_gaps.md
implementation/narrative_v2/N_IMP_05_REPORT.md
```

---

## 6. Files modified

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
tests/narrative_v2/test_runtime_skeleton.py
tests/narrative_v2/test_evidence_runtime_integration.py
tests/narrative_v2/test_reasoning_runtime_integration.py
tests/narrative_v2/test_knowledge_runtime_integration.py
```

Knowledge sources, Pack05, Portal, and astrology engines were not modified.

---

## 7. Rewrite item contract

```
RewriteItem
  rewrite_id
  semantic_key
  domain
  source_knowledge_ids
  source_reasoning_ids
  source_evidence_ids
  source_meaning
  normalized_meaning
  customer_language
  strategy
  style
  status
  references
  metadata
```

`customer_language` is a rewrite unit, not a final paragraph.

---

## 8. Rewrite context contract

```
CommercialRewriteContext
  items
  unresolved
  references
  metadata
  status
  contract_gaps
```

Not included: overview, interpretation, action_plan, presentation.

---

## 9. Supported strategies

simplification, clarification, contextualization,
professionalization, action_orientation

CASE-0001 applies **clarification** (add customer address `Bạn`).
`action_orientation` is registered and not applied.

---

## 10. Language profile

audience=customer, address=Bạn, locale=vi, voice=professional,
style=consultant.

Forbidden: đương số, mệnh chủ, fortune absolutes, fear language.

---

## 11. Meaning preservation

Source priority:

1. `customer_meaning_candidate` (empty on CASE-0001)
2. approved `positive_meaning` from traced source file
3. technical meaning only if already customer-safe
4. UNRESOLVED

Normalization is address wrap + terminal period only.

---

## 12. Semantic escalation protection

Validator rejects added certainty, prediction, fear, and tokens such as
màu đỏ / tình duyên chắc chắn when absent from source.

---

## 13. Terminology handling

Entity slug stored in metadata (`terminology`). Customer language is
the approved `positive_meaning`, not a requirement that the customer
already know Chính Ấn / Dụng thần.

Unsafe jargon sources are unresolved rather than leaked.

---

## 14. Sentence selection strategy

`SentenceSelector.select` → None.

No random variants. No network. No language-model calls.

---

## 15. Grammar/template boundary

Not assembled. Recorded as contract gaps. Unit rewrite only.

---

## 16. Validation

Approved knowledge trace, stable ids, ordering, no escalation, no fear,
no JSON/debug, no rule/engine leak, no new action/prediction,
deterministic output.

---

## 17. Runtime integration

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
build_summary = NotImplemented
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

Presentation remains None.

---

## 18. CASE-0001 rewrite summary

Real pipeline. Not hardcoded. Status: **partial**.

10 rewritten units. 3 unresolved.

Trace: `implementation/narrative_v2/n_imp_05/case0001_rewrite_trace.json`

---

## 19. Rewritten semantic keys

| Rewrite id | Semantic key | Strategy |
|------------|--------------|----------|
| rewrite.pattern.chinh_an.001 | core.pattern_context | clarification |
| rewrite.strength.strong.001 | core.pattern_context | clarification |
| rewrite.ten_gods.{kiep_tai,nhat_chu,that_sat,thien_an}.001 | core.pattern_ten_gods_relation | clarification |
| rewrite.shensha.{hong_loan,thien_at_quy_nhan,thien_duc_quy_nhan,nguyet_duc_quy_nhan}.001 | boundary.approved_rule_unavailable | clarification |

---

## 20. Passthrough semantic keys

None on CASE-0001. No source already opened with `Bạn`.

---

## 21. Unresolved semantic keys

| Semantic key | Reason |
|--------------|--------|
| core.temperature_balancing_context | knowledge_unresolved |
| core.luck_temporal_context | knowledge_unresolved |
| core.useful_god_context | source_not_customer_safe (`Dụng thần` in positive_meaning) |

---

## 22. Contract gaps

See `implementation/narrative_v2/n_imp_05/rewrite_contract_gaps.md`.

Principal: sentence library runtime gap; grammar/template not assembled;
useful god jargon not rewritten; temperature/luck still missing knowledge.

---

## 23. Tests

```
py -m pytest tests/narrative_v2 -q
145 passed
```

Coverage: RW1–RW20 and language negatives.
Remaining failures: none.

---

## 24. Determinism verification

Same KnowledgeContext produces identical items and unresolved rows
on two rewrites. Ids and order are stable.

---

## 25. Shadow mode verification

- SHADOW_MODE = True
- replaces_pack05 = False
- portal_connected = False
- presentation = None
- Rewrite package does not import Pack05 or Portal

---

## 26. Out-of-scope confirmation

No Summary Builder implemented: YES
No Interpretation Builder implemented: YES
No Action Builder implemented: YES
No final Narrative generated: YES
No Presentation published: YES
No Portal integration: YES
No Pack05 replacement: YES
No astrology engine modified: YES
No LLM/network rewrite: YES
No new approved knowledge invented: YES

---

## 27. Verdict

READY FOR PRODUCT OWNER REVIEW

STOP.

Do not start N-IMP-06.
