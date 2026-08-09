# Evidence Layer Validation Specification

**Status:** Specification only  
**Sprint:** KX-1B  
**Runtime:** None

---

## Checks

| ID | Check | Fail if |
|----|--------|---------|
| EV-001 | every rule has evidence | A `SKC-*` in `rules/` has no `evidence/bundles/{id}.json` |
| EV-002 | explanation exists | `explanation.why`, `when`, `when_not`, `summary` empty |
| EV-003 | confidence exists | `confidence_level` missing or not in allowed enum |
| EV-004 | confidence reason exists | `confidence_reason` empty |
| EV-005 | references valid | Reference id not in `evidence/references/sources.json` or package `references/references.json` |
| EV-006 | example links valid | Example `rule_id` ≠ bundle `rule_id`, or `<1` positive/negative |
| EV-007 | related/conflicting IDs valid | Target id not in package rule set, or self-link |
| EV-008 | related graph acyclic | Directed `related_rules` contains a cycle |
| EV-009 | exclusive conflict symmetry | Exclusive-group peers missing from `conflicting_rules` |
| EV-010 | traceability complete | Missing originating package, versions, author, review status, last_reviewed |

Severity: all `error` except EV-009 `warning` if group declared but incomplete.

Allowed `confidence_level`: `experimental`, `low`, `medium`, `high`, `canonical`.

No executable validator is introduced in KX-1B. Future tools MUST implement these checks in this order.
