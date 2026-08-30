# N-IMP-04 KNOWLEDGE RESOLVER REPORT

Sprint: N-IMP-04
Module: engines/narrative_v2/knowledge
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Knowledge Resolver binds approved interpretation entities to reasoning
semantics. It does not rewrite customer language, invent knowledge, or
build an Action Plan.

---

## 2. Knowledge source audit

Audit file:

`implementation/narrative_v2/n_imp_04/knowledge_source_audit.md`

Used: `knowledge/interpretation/domains/{strength,pattern,useful_god,ten_gods,shensha}/*.json`
with explicit `metadata.status = approved`.

Not used: Pack05 prose, Portal, commercial Dashboard, CK-01 action catalog,
concept files without exact keys, Temperature/Luck domain trees (empty).

---

## 3. Resolver architecture

```
NarrativeReasoningContext
        (+ NarrativeEvidenceContext for entity-key matching)
        ↓
KnowledgeResolver
        ↓
NarrativeKnowledgeContext
```

Logic lives in `engines/narrative_v2/knowledge/`.
Runtime only calls `resolve_knowledge`.

---

## 4. Files created

```
engines/narrative_v2/knowledge/__init__.py
engines/narrative_v2/knowledge/knowledge_resolver.py
engines/narrative_v2/knowledge/knowledge_context.py
engines/narrative_v2/knowledge/knowledge_item.py
engines/narrative_v2/knowledge/knowledge_reference.py
engines/narrative_v2/knowledge/knowledge_registry.py
engines/narrative_v2/knowledge/knowledge_index.py
engines/narrative_v2/knowledge/knowledge_loader.py
engines/narrative_v2/knowledge/knowledge_validator.py
engines/narrative_v2/knowledge/knowledge_errors.py
engines/narrative_v2/knowledge/knowledge_status.py
tests/narrative_v2/test_knowledge_resolver.py
tests/narrative_v2/test_knowledge_context.py
tests/narrative_v2/test_knowledge_loader.py
tests/narrative_v2/test_knowledge_index.py
tests/narrative_v2/test_knowledge_validator.py
tests/narrative_v2/test_knowledge_runtime_integration.py
tests/narrative_v2/test_knowledge_approval.py
implementation/narrative_v2/n_imp_04/knowledge_source_audit.md
implementation/narrative_v2/n_imp_04/case0001_knowledge_trace.json
implementation/narrative_v2/n_imp_04/knowledge_contract_gaps.md
implementation/narrative_v2/N_IMP_04_REPORT.md
```

---

## 5. Files modified

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
tests/narrative_v2/test_runtime_skeleton.py
tests/narrative_v2/test_evidence_runtime_integration.py
tests/narrative_v2/test_reasoning_runtime_integration.py
```

Pack05, Portal, astrology engines, and `knowledge/` sources were not modified.
No new approved knowledge files were created.

---

## 6. Knowledge item contract

```
KnowledgeItem
  knowledge_id
  domain
  semantic_key
  knowledge_type
  status
  technical_meaning
  customer_meaning_candidate
  boundaries
  recommendations
  references
  source_path
  version
  metadata
```

`customer_meaning_candidate` is source copy only. Interpretation entities
do not publish that field, so CASE-0001 values are None.

---

## 7. Knowledge context contract

```
NarrativeKnowledgeContext
  items
  matches
  unresolved
  references
  metadata
  status
  contract_gaps
```

Not included: final_summary, final_interpretation, final_action_plan,
presentation.

---

## 8. Approval policy

Eligible only when `metadata.status` is exactly `approved`.

Draft, review, deprecated, Expert Ready (quality label), and directory
name alone are not approval.

---

## 9. Matching strategy

```
exact semantic_key
↓
approved alias (same-record id suffix ↔ key)
↓
documented parent/related entity (evidence value → domain+key)
↓
UNRESOLVED
```

No fuzzy matching. No embeddings. No LLM.

---

## 10. Alias strategy

Documented aliases are only the `id` suffix of an approved record when it
differs from `key` (example: `chinh_quan` ↔ `Chính Quan` on
`knowledge.useful_god.chinh_quan`).

No invented Vietnamese↔romanization table beyond that.

---

## 11. Supported knowledge types

meaning, boundary, recommendation, warning, domain_context,
terminology, supporting_explanation

This sprint emits `meaning` items. Recommendation strings are source
copies on the item, not an Action Plan.

---

## 12. Knowledge index

Loader reads approved domain JSON once, sorts by `knowledge_id`, and
indexes `(domain, key)`, `(domain, id)`, and documented aliases.

Static cache is read-only and version-aware. CanonicalAnalysis is not cached.

---

## 13. Version strategy

`KnowledgeItem.version` copied from `metadata.version`.
Context metadata includes `resolver_version=nimp04.1.0` and observed
`knowledge_version` values.

No false versions. Missing version would be recorded as None plus a
contract gap. CASE-0001 sources publish `1.0.0`.

---

## 14. Boundary preservation

N-IMP-03 ShenSha `approved_rule_unavailable` is not dropped.

Approved ShenSha names resolve to domain entities. The boundary semantic
key remains on the match rows. Unmatched names would stay unresolved.

---

## 15. Unresolved strategy

Explicit `KnowledgeUnresolved` rows with:

semantic_key, reason, required_source, reasoning_ids, evidence_ids

Reasons used: `no_approved_knowledge` (temperature, luck).

---

## 16. Validation

`KnowledgeValidator` checks approved status, stable ids, known
semantic_key, reasoning/evidence traces, no duplicate ids/matches,
no draft, no debug objects, no final narrative fields, no rewrite markers.

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
commercial_rewrite = NotImplemented
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

## 18. CASE-0001 resolution summary

Real Evidence → Reasoning → Knowledge. Not hardcoded.

Status: **partial**

11 items, 13 matches, 2 unresolved.

Trace: `implementation/narrative_v2/n_imp_04/case0001_knowledge_trace.json`

---

## 19. Resolved semantic keys

| Semantic key | Resolution | Knowledge ids |
|--------------|------------|---------------|
| core.pattern_context | RESOLVED | knowledge.pattern.chinh_an, knowledge.strength.strong |
| core.useful_god_context | RESOLVED | knowledge.useful_god.chinh_quan, knowledge.strength.strong |
| core.pattern_ten_gods_relation | RESOLVED | knowledge.pattern.chinh_an, ten_gods.{that_sat,kiep_tai,nhat_chu,thien_an} |
| boundary.approved_rule_unavailable | RESOLVED | shensha hong_loan, thien_at_quy_nhan, thien_duc_quy_nhan, nguyet_duc_quy_nhan |

---

## 20. Unresolved semantic keys

| Semantic key | Reason |
|--------------|--------|
| core.temperature_balancing_context | no_approved_knowledge (temperature domain empty) |
| core.luck_temporal_context | no_approved_knowledge (luck domain empty) |

Honest UNRESOLVED. Not forced.

---

## 21. Contract gaps

See `implementation/narrative_v2/n_imp_04/knowledge_contract_gaps.md`.

Principal gaps: no Narrative V2 records keyed to reasoning semantic keys;
no Temperature/Luck domain entities; no `customer_meaning` field; CK-01
not eligible as item JSON; Hỏa element not an entity.

---

## 22. Tests

```
py -m pytest tests/narrative_v2 -q
121 passed
```

Coverage: K1–K20 and semantic negatives.
Remaining failures: none.

---

## 23. Determinism verification

Same ReasoningContext + EvidenceContext produces identical items, matches,
and unresolved rows on two resolves. Index load order is sorted by id.

---

## 24. Shadow mode verification

- SHADOW_MODE = True
- replaces_pack05 = False
- portal_connected = False
- presentation = None
- Knowledge package does not import Pack05 or Portal

---

## 25. Out-of-scope confirmation

No Commercial Rewrite implemented: YES
No Summary implemented: YES
No Interpretation implemented: YES
No Action implemented: YES
No final customer prose generated: YES
No Portal integration: YES
No Pack05 replacement: YES
No astrology engine modified: YES
No new approved knowledge invented: YES

---

## 26. Verdict

READY FOR PRODUCT OWNER REVIEW

STOP.

Do not start N-IMP-05.
