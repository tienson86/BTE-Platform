# BTE Knowledge Reasoning Framework

| Field | Value |
|-------|-------|
| **Framework version** | 1.0.0 |
| **Sprint** | KX-1C |
| **Status** | Canonical |
| **Scope** | Specification only — no runtime engine |

Reasoning sits between Evidence and Interpretation:

```
Knowledge → Evidence → Reasoning → Interpretation → Report
```

This folder is **platform-wide**. Strength Core is the first package that implements instance graphs under `knowledge/packages/strength/core/reasoning/`.

---

## Contents

| File | Role |
|------|------|
| `REASONING_FRAMEWORK.md` | Canonical framework |
| `reasoning_graph.schema.json` | Graph envelope |
| `reasoning_node.schema.json` | Node |
| `reasoning_edge.schema.json` | Edge |
| `reasoning_chain.schema.json` | Inference chain |
| `reasoning_trace.schema.json` | Trace |
| `reasoning_confidence.schema.json` | Confidence propagation contract |
| `reasoning_validation.md` | Validation spec (no runtime) |
| `templates/` | Copy-paste templates |
| `examples/` | Pointers to Strength example graphs |
| `documentation/` | Philosophy and model notes |

Architecture summary: `knowledge/docs/architecture/KNOWLEDGE_REASONING_FRAMEWORK.md`
