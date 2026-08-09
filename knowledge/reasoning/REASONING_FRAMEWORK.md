# BTE Knowledge Reasoning Framework

| Field | Value |
|-------|-------|
| **Document** | REASONING_FRAMEWORK |
| **Version** | 1.0.0 |
| **Sprint** | KX-1C |
| **Status** | Canonical |
| **Runtime** | None |

---

## 1. Reasoning philosophy

Reasoning is the **declared path** from observed chart facts to an analytical conclusion.

It is not the Rule Engine matcher. It is not Interpretation prose. It records *how knowledge justifies a conclusion* so humans, reports, and future AI can replay the same path deterministically.

Principles:

1. **Knowledge first** — every inference node cites a rule id that already exists.
2. **Evidence second** — nodes that apply rules point at Evidence Bundles (KX-1B).
3. **Deterministic graphs** — same nodes + edges + sort always yield the same chain order.
4. **Explainable** — Observation → Evidence → Inference → Intermediate → Final is mandatory on every chain.
5. **Honest alternatives** — unused branches and contradictions are first-class, not deleted.
6. **Package independent** — a package ships its own `reasoning/` folder; the framework schemas stay global.
7. **No silent scoring** — confidence propagation is declared, not computed by undocumented code.

---

## 2. Graph model

A **Reasoning Graph** (`RG-*`) is a directed graph:

- **Nodes** (`RN-*`) — observations, evidence applications, inferences, conclusions, alternatives, contradictions
- **Edges** (`RE-*`) — supports, requires, contradicts, extends, derives, confirms, invalidates
- **Chains** (`RC-*`) — one ordered decision/explanation path through the graph
- **Traces** (`RT-*`) — activated rules, evidence, confidence movement, package version

Capabilities the graph MUST be able to express:

| Capability | How |
|------------|-----|
| Reasoning nodes | `node_type` catalog |
| Reasoning edges | typed `relationship` |
| Inference chains | `stages[]` on `RC-*` |
| Decision paths | `trace.decision_path` |
| Explanation paths | same chain, reader-facing titles |
| Alternative branches | `node_type=alternative` + unused list |
| Contradiction branches | `node_type=contradiction` + `contradicts` edges |
| Confidence propagation | per-node `mode` + chain trace |

Determinism: node_id / edge_id ascending, locale `C`. No random layout data in the spec.

---

## 3. Node model

Required fields: `node_id`, `node_type`, `title`, `description`, `source_rule`, `source_evidence`, `inputs`, `outputs`, `confidence`, `metadata`.

| Type | Typical source_rule |
|------|---------------------|
| observation | null (chart facts) |
| evidence | rule whose bundle is cited |
| inference | activating rule |
| intermediate_conclusion | tendency / composite rule |
| final_conclusion | level / classification rule |
| alternative | rule that *could* apply but did not |
| contradiction | rule that would oppose the final conclusion |

---

## 4. Edge model

Required: `source`, `target`, `relationship`, `weight` (0–1 declarative), `direction`, `condition`.

| Relationship | Meaning |
|--------------|---------|
| supports | Source makes target more plausible |
| requires | Target cannot stand without source |
| contradicts | Source and target cannot both be taken |
| extends | Target adds detail without replacing source |
| derives | Target is inferred from source |
| confirms | Target independently agrees with source |
| invalidates | Source removes target from the taken path |

Default `direction` is `forward`. Cycles on `derives` / `requires` are forbidden (see validation).

---

## 5. Chain model

Every chain documents:

```
Observation → Evidence → Inference → Intermediate conclusion → Final conclusion
```

`rule_ids` MUST exist in the implementing package. Multiple inference nodes may appear between evidence and intermediate.

---

## 6. Traceability model

A trace records, without executing engines:

- activated rules
- activated evidence bundle paths
- confidence propagation steps
- decision path node ids
- `package_id` + `package_version` + `framework_version`

Traces are authored artifacts, not runtime logs.

---

## 7. Confidence model

Levels (same as Evidence Layer): experimental < low < medium < high < canonical.

Modes:

| Mode | Meaning |
|------|---------|
| declared | Taken from the evidence/rule confidence as-is |
| inherited | Same level as the required predecessor |
| reduced | Weaker than predecessors (alternative, distant support) |
| conflicting | Opposing branch exists; both levels retained |
| combined | Conservative meet of supporting predecessors (min rank) |

No numeric scoring algorithm is specified or implemented in this sprint.

Full contract: `reasoning_confidence.schema.json` and `documentation/confidence_model.md`.

---

## 8. Future AI integration

AI tools SHOULD:

1. Walk `decision_path` instead of inventing a new story.
2. Surface alternative and contradiction nodes to the consultant.
3. Quote explanation text from Evidence Bundles, not from hidden model weights.
4. Propose new nodes as `draft`; humans own Domain Review (KD-4).
5. Emit traces that validate against these schemas for report generation and interactive debugging.

---

## 9. First implementation

`knowledge/packages/strength/core/reasoning/` — Strong / Weak / Balanced Day Master graphs using existing `SKC-*` rules only.
