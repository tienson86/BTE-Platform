# GENERALIZATION_REPORT

Fixture: `SYNTHETIC_REQUEST_B` (and CASE-0001 vs CASE-0002).

| Check | Result |
|-------|--------|
| same facts → same result | PASS — determinism test |
| different facts → different themes/body | PASS |
| no case branching | PASS — no CASE-0001/0002 ifs in reasoner |
| no master prose leakage | PASS — Sprint 4 / generic tests |
| no randomness | PASS |
