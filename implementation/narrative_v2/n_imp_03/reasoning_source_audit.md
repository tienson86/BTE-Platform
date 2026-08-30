# N-IMP-03 Reasoning Source Audit

Sprint: N-IMP-03
Module: engines/narrative_v2/reasoning
Mode: Shadow Mode

This audit classifies candidate reasoning sources before implementation.
Free-form prose is not used as a rule. Pack05 sentences are not reverse-engineered.

---

## Classification legend

| Status | Meaning |
|--------|---------|
| APPROVED | Published structural relationship usable as an internal semantic rule |
| LEGACY | Existing reasoning assets that produce or assume customer/technical prose |
| TECHNICAL | Schema, graph tooling, or input contracts — not relationship rules |
| UNSUITABLE | Customer meaning, action, or invented astrology |

---

## Sources considered

| Source | Status | Scope | Used | Reason |
|--------|--------|-------|------|--------|
| `knowledge/narrative_v2/00_ARCHITECTURE.md` §5.2 Reasoning Builder | APPROVED | Strength + Pattern + Useful God → ReasoningContext | YES | Canonical structural purpose: connect published evidence. Does not define customer meaning. |
| `knowledge/narrative_v2/03_PIPELINE.md` Stage 2 | APPROVED | EvidenceContext → ReasoningContext | YES | Confirms input/output boundary and forbids recommendation. |
| `knowledge/narrative_v2/08_RUNTIME_SEQUENCE.md` | APPROVED | Runtime order only | YES | Sequence only. No meaning rules. |
| `knowledge/narrative_v2/01_DATA_MODEL.md` ReasoningContext / ReasoningNode | APPROVED (structure) / UNSUITABLE (example prose) | Node/context field shapes | PARTIAL | Structure used. Example “Nội lực tốt / Chịu trách nhiệm tốt” is Meaning, not a rule. |
| `knowledge/narrative_v2/GLOSSARY.md` Reasoning vs Meaning | APPROVED | Layer boundary | YES | Reasoning answers “why related”; Meaning is customer language. |
| N-IMP-03 sprint contract relationships A–E | APPROVED | Minimal structural core | YES | Product-owner scoped initial graph. |
| `knowledge/reasoning_engine/CROSS_DOMAIN_V1_1/PRECEDENCE_POLICY.md` | APPROVED | Useful God conditional on strength; Ten Gods do not override Pattern | YES | Structural precedence only. “Do not invent metaphysical precedence.” |
| `knowledge/reasoning_engine/CROSS_DOMAIN_V1_1/INPUT_CONTRACT.md` | TECHNICAL | Cross-domain engine input shape | NO | Different engine. Would pull CanonicalAnalysis fields, not EvidenceContext. |
| `knowledge/interpretation/interaction/INTERACTION_FACTS.md` | APPROVED | Luck = period identity / temporal context; natal governors copied not restamped | YES | Luck rule E: temporal context only. No luck quality. |
| `knowledge/interpretation/interaction/INTERACTION_BOUNDARIES.md` | APPROVED | Must not reclassify strength, reselect pattern, interpret luck | YES | Confirms Reasoning must not recompute Evidence. |
| `knowledge/interpretation/domains/*/COVERAGE.md` | LEGACY / UNSUITABLE | Domain interpretation coverage | NO | Meaning catalogs. Belong to Knowledge Resolver. |
| `knowledge/packages/*/reasoning/*.json` | LEGACY | Pedagogical package graphs (`requires` / `derives` / `extends`) | NO | Different relation vocabulary. Example/trace assets, not Narrative V2 rules. |
| `knowledge/reasoning_engine/PACK_01_STRENGTH/*` | LEGACY | Strength customer-mode chain FACT→INTERPRETATION→IMPLICATION→ACTION | NO | Downstream meaning/action. Not Evidence relationship. |
| `knowledge/reasoning/documentation/graph_model.md` | TECHNICAL | Visualization of package graphs | NO | No approved Narrative V2 relations. |
| `engines/narrative_framework/strength/reasoning.py` | LEGACY | Vietnamese sentence blocks from strength evidence | NO | Customer/technical prose. Pack-adjacent narrative framework. |
| `engines/narrative_engine` (Pack05) | LEGACY / UNSUITABLE | Production customer narrative | NO | Forbidden to reverse-engineer sentences into rules. |
| `engines/knowledge_engine/reasoning_models.py` | TECHNICAL | Knowledge-engine models | NO | Wrong layer. Knowledge Resolver is N-IMP-04+. |
| Commercial consulting / sentence / explanation libraries | UNSUITABLE | Customer prose templates | NO | Meaning / Rewrite / Presentation. |
| Portal adapters / frontend models | UNSUITABLE | UI contracts | NO | Out of scope. Portal not connected. |
| `if strength == "strong": meaning = "independent"` style mappings | UNSUITABLE | Invented meaning | NO | Explicitly forbidden. Recorded as contract gap. |
| ShenSha → relationship/career/finance meaning | UNSUITABLE | Domain meaning | NO | No approved ShenSha relationship in this sprint. |
| Luck Ất Tỵ → “vận tốt” | UNSUITABLE | Luck quality | NO | Interaction Facts: identity only, not a luck reading. |
| Useful God Hỏa → “nên bổ Hỏa” | UNSUITABLE | Action | NO | Action Builder / Rewrite. |

---

## Rules actually registered

Only these five structural relationships are implemented:

| Rule id (internal) | Relationship | Relation type | Semantic key |
|--------------------|--------------|---------------|--------------|
| NR-REL-001 | Strength contextualizes Pattern | contextualizes | core.pattern_context |
| NR-REL-002 | Strength contextualizes Useful God | contextualizes | core.useful_god_context |
| NR-REL-003 | Temperature contextualizes balancing need | contextualizes | core.temperature_balancing_context |
| NR-REL-004 | Pattern relates to visible Ten Gods | qualifies (+ supports from ten gods) | core.pattern_ten_gods_relation |
| NR-REL-005 | Luck identifies temporal context only | contextualizes | core.luck_temporal_context |

Rule ids stay in node/edge metadata. They must not reach Presentation.

---

## Explicitly not used

- Pack05 sentence reverse-engineering
- Package pedagogical JSON graphs
- Commercial consulting prose
- Impact catalogs (`impact.structure_preference`)
- Identity meaning key `reasoning.identity.structured_self_direction`

If a relationship is not in the approved table above, the builder records
`REASONING CONTRACT GAP` and does not invent a rule.
