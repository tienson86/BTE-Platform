# RELATION_MODEL — Frozen RelationType enum

| Type | Meaning |
|------|---------|
| AGREEMENT | Same direction, comparable scope |
| REINFORCEMENT | Different domains amplify each other |
| CONDITIONAL_NUANCE | Both valid under conditions |
| DIFFERENT_SCOPE | Not the same concept |
| DEPENDENCY_OVERRIDE | Special classification recontextualizes ordinary read (does not delete publish) |
| TRUE_CONFLICT | Same-scope contradiction needing arbitration |
| UNRESOLVED | Cannot decide — blocker required |
| NOT_COMPARABLE | No overlapping comparable pair |

Engine: `cross_domain/relation_engine.detect_relations`.

Customer Mode must **not** show enum names; composers emit safe Vietnamese states.
