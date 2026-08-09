# Reasoning Framework Validation Specification

**Status:** Specification only  
**Framework version:** 1.0.0  
**Runtime:** None

---

## Checks

| ID | Check | Fail if |
|----|--------|---------|
| RG-001 | graph integrity | Graph missing required ids; `deterministic` ≠ true |
| RG-002 | missing nodes | `node_ids` / chain / edge endpoints not found on disk |
| RG-003 | orphan nodes | Node not referenced by any edge or chain stage |
| RG-004 | invalid edges | Unknown relationship; missing source/target; self-loop on derives/requires |
| RG-005 | circular reasoning | Cycle in subgraph of `derives` ∪ `requires` ∪ `extends` |
| RG-006 | missing rule references | `source_rule` set but id not in package `rules/` |
| RG-007 | missing evidence references | `source_evidence` set but file/bundle missing |
| RG-008 | chain completeness | Chain lacks the five mandatory stages |
| RG-009 | trace alignment | Trace `activated_rules` not ⊆ chain `rule_ids` |
| RG-010 | confidence modes | Node confidence.mode not in allowed enum |

Severity: all `error` except RG-003 `warning` when the node is explicitly typed `alternative` or `contradiction` and listed on the chain.

`contradicts` / `invalidates` edges MAY form opposing pairs; they are excluded from the cycle check in RG-005.

No executable validator is introduced in KX-1C.
