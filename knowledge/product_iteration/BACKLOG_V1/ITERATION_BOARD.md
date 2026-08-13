# ITERATION_BOARD

| Field | Value |
|-------|-------|
| States | Backlog → Ready → In Progress → Validation → Regression → Done |
| In Progress | **Max 1** |

---

## Board (2026-08-13)

```text
BACKLOG          READY           IN PROGRESS      VALIDATION       REGRESSION        DONE
PB-006           PB-005          —                —                —                 ITERATION_001
PB-007           (next: 003)                                                          ITERATION_002
PB-008                                                                                PB-001…004
PB-009                                                                                PB-013
PB-010                                                                                PB-D01…D06
PB-011
────────────────
DEFERRED         PB-012
REJECTED         PB-R01 R02 R03
```

---

## State rules

| State | Meaning |
|-------|---------|
| Backlog | Evidenced; not sequenced |
| Ready | ROI + layer + regression set filled; may enter next iteration |
| In Progress | One iteration is implementing |
| Validation | Target chart rescored |
| Regression | CASE_0001 (+ named holds) run |
| Done | Observed ROI written · checklist closed |

Deferred ≠ Done. Rejected ≠ Backlog.

---

## Current iteration

| Field | Value |
|-------|-------|
| Closed | **ITERATION_001** — analytics foundation |
| Closed | **ITERATION_002** — Narrative Quality (PB-001+002+003) |
| Next | **ITERATION_003** ← **PB-005** (Ready) |
| Must not | Start a second In Progress beside 003 |

---

END
