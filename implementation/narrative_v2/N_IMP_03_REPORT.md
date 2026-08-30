# N-IMP-03 REASONING BUILDER REPORT

Sprint: N-IMP-03
Module: engines/narrative_v2/reasoning
Mode: Shadow Mode
Status: READY FOR PRODUCT OWNER REVIEW

---

## 1. Status

PASS

Reasoning Builder connects published Evidence into an internal semantic
graph. It does not recompute Evidence, invent meaning rules, or write
customer narrative.

---

## 2. Reasoning source audit

Audit file:

`implementation/narrative_v2/n_imp_03/reasoning_source_audit.md`

Used (APPROVED structural only):

- `knowledge/narrative_v2/00_ARCHITECTURE.md` §5.2
- `knowledge/narrative_v2/03_PIPELINE.md` Stage 2
- `knowledge/narrative_v2/GLOSSARY.md` Reasoning vs Meaning
- `knowledge/reasoning_engine/CROSS_DOMAIN_V1_1/PRECEDENCE_POLICY.md`
- `knowledge/interpretation/interaction/INTERACTION_FACTS.md`
- `knowledge/interpretation/interaction/INTERACTION_BOUNDARIES.md`
- N-IMP-03 relationships A–E

Not used: Pack05 sentences, package pedagogical graphs, commercial
prose, Portal adapters, invented `if strong → independent` mappings.

---

## 3. Reasoning architecture

```
CanonicalAnalysis
        ↓
EvidenceBuilder
        ↓
NarrativeEvidenceContext
        ↓
ReasoningBuilder
        ↓
NarrativeReasoningContext
```

Reasoning reads EvidenceContext only. Logic lives in
`engines/narrative_v2/reasoning/`. Runtime only invokes the builder at
`build_reasoning`.

---

## 4. Files created

```
engines/narrative_v2/reasoning/__init__.py
engines/narrative_v2/reasoning/reasoning_builder.py
engines/narrative_v2/reasoning/reasoning_context.py
engines/narrative_v2/reasoning/reasoning_node.py
engines/narrative_v2/reasoning/reasoning_edge.py
engines/narrative_v2/reasoning/reasoning_reference.py
engines/narrative_v2/reasoning/reasoning_registry.py
engines/narrative_v2/reasoning/reasoning_validator.py
engines/narrative_v2/reasoning/reasoning_errors.py
engines/narrative_v2/reasoning/reasoning_rules.py
tests/narrative_v2/test_reasoning_builder.py
tests/narrative_v2/test_reasoning_context.py
tests/narrative_v2/test_reasoning_validator.py
tests/narrative_v2/test_reasoning_runtime_integration.py
tests/narrative_v2/test_reasoning_contract_gaps.py
implementation/narrative_v2/n_imp_03/reasoning_source_audit.md
implementation/narrative_v2/n_imp_03/case0001_reasoning_trace.json
implementation/narrative_v2/N_IMP_03_REPORT.md
```

---

## 5. Files modified

```
engines/narrative_v2/runtime/runtime_pipeline.py
engines/narrative_v2/runtime/runtime_context.py
tests/narrative_v2/test_runtime_skeleton.py
tests/narrative_v2/test_evidence_runtime_integration.py
```

Pack05, Portal, API production path, astrology engines, and
`knowledge/narrative_v2/` were not modified.

Runtime tests were updated only so `build_reasoning` is no longer
asserted as NotImplemented, matching this sprint contract.

---

## 6. Reasoning node contract

```
ReasoningNode
  reasoning_id
  domain
  kind
  semantic_key
  evidence_ids
  relation
  priority
  status
  references
  metadata
```

Allowed kinds: observation, cause, relation, impact_candidate, boundary.

This sprint emits observation, relation, and boundary.
No recommendation, action, or customer_meaning fields.

---

## 7. Reasoning edge contract

```
ReasoningEdge
  edge_id
  source_ids
  target_id
  relation_type
  weight
  status
  references
  metadata
```

Weight is the constant `1.0`. It is not inferred from score magnitude.

---

## 8. Supported relation types

```
supports
constrains
qualifies
balances
amplifies
reduces
contextualizes
```

N-IMP-03 fires `contextualizes`, `qualifies`, and `supports`.
`constrains` is represented when both supports and constrains land on
the same target; both edges are kept.

---

## 9. Rule contract

```
ReasoningRule
  rule_id
  status
  required_evidence
  optional_evidence
  relation_type
  output_semantic_key
  priority
  references
```

Internal rule ids: NR-REL-001 … NR-REL-005.
They appear only in metadata. They must never reach Presentation.

Priority is the explicit rule priority. Fallback is registration order.

---

## 10. Observation candidates

Created when required evidence is available:

| Semantic key | Evidence |
|--------------|----------|
| core.pattern_context | strength.level + pattern.primary |
| core.useful_god_context | strength.level + useful_god.primary |
| core.temperature_balancing_context | temperature.climate_state + balancing_need |
| core.pattern_ten_gods_relation | pattern.primary + ten_gods.visible_labels |
| core.luck_temporal_context | luck.current_cycle |

No customer wording.

---

## 11. Impact candidates

None.

`impact.structure_preference` is a REASONING CONTRACT GAP.
No approved impact relationship catalog exists for this sprint.

---

## 12. Boundary handling

Boundaries recorded instead of guessing:

- required evidence missing → `evidence_insufficient`
- current luck missing → `temporal_context_unavailable`
- ShenSha names present with no approved rule → `approved_rule_unavailable`

---

## 13. Conflict handling

If incoming `supports` and `constrains` share a target:

- both edges are kept
- target status = `conflict`
- no arbitrary winner

Qualification (pattern qualifies ten gods; ten gods support the
relation) is preserved without collapsing either edge.

---

## 14. Priority strategy

1. Explicit `ReasoningRule.priority`
2. Stable registration order
3. `reasoning_id` for final sort

Not used: UI order, score magnitude, array position.

---

## 15. Validation

`ReasoningValidator` checks:

- all `evidence_ids` exist on EvidenceContext
- unique `reasoning.*` ids
- no customer prose
- no unsupported relation type
- no unknown rule_id
- no circular dependency
- deterministic node ordering
- traceability to Evidence (non-boundary nodes)
- no CanonicalAnalysis / customer-text fields on the context

---

## 16. Runtime integration

```
initialize
↓
build_evidence = IMPLEMENTED
↓
build_reasoning = IMPLEMENTED
↓
resolve_knowledge = NotImplemented
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

`NarrativeRuntimeResult.presentation` remains `None`.

---

## 17. CASE-0001 reasoning summary

Real CASE-0001 EvidenceContext (from Orchestrator `run_stage("luck")`).
Outcome is not hardcoded.

| Semantic key | Relation | Evidence |
|--------------|----------|----------|
| core.pattern_context | contextualizes | strength.level, pattern.primary, pattern.cach_cuc |
| core.useful_god_context | contextualizes | strength.level, useful_god.primary, useful_god.element |
| core.temperature_balancing_context | contextualizes | climate_state, balancing_need |
| core.pattern_ten_gods_relation | qualifies / supports | pattern.primary, ten_gods.visible_labels |
| core.luck_temporal_context | contextualizes | luck.current_cycle (+ available, direction) |

ShenSha names are present and recorded as
`boundary.approved_rule_unavailable`. No Hồng Loan meaning.

22 nodes, 6 edges, 16 observations, 0 impacts, 1 boundary.

Trace: `implementation/narrative_v2/n_imp_03/case0001_reasoning_trace.json`

No sentence such as “Bạn có nội lực tốt.” No action.

---

## 18. Contract gaps

REASONING CONTRACT GAP — not invented in this sprint:

| Field | Reason |
|-------|--------|
| reasoning.shensha.meaning | no approved ShenSha meaning relationship |
| reasoning.career | out of N-IMP-03 scope |
| reasoning.finance | out of N-IMP-03 scope |
| reasoning.relationship | out of N-IMP-03 scope |
| reasoning.luck.quality | luck quality interpretation is not approved |
| reasoning.impact.structure_preference | no approved impact catalog |
| reasoning.strength.customer_meaning | belongs to Rewrite |
| reasoning.pattern.customer_meaning | belongs to Rewrite |
| reasoning.useful_god.action | belongs to Action Builder |
| reasoning.identity.structured_self_direction | identity meaning key is not an approved rule |

---

## 19. Tests

```
py -m pytest tests/narrative_v2 -q
91 passed
```

Coverage: R1–R18 and semantic negatives
(strength / pattern / useful god / Hồng Loan / current luck).

---

## 20. Determinism verification

Same EvidenceContext produces identical ReasoningContext on two builds.
Ids, ordering, edges, and contract gaps are stable.

---

## 21. Shadow mode verification

- SHADOW_MODE = True
- replaces_pack05 = False
- portal_connected = False
- presentation = None
- Reasoning package does not import Pack05 or Portal
- Production still reads Pack05

---

## 22. Out-of-scope confirmation

No Knowledge Resolver implemented: YES
No Commercial Rewrite implemented: YES
No Summary implemented: YES
No Interpretation implemented: YES
No Action implemented: YES
No customer prose generated: YES
No Portal integration: YES
No Pack05 replacement: YES
No astrology engine modified: YES

---

## 23. Verdict

READY FOR PRODUCT OWNER REVIEW

STOP.

Do not start N-IMP-04.
