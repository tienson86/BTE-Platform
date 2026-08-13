# ITERATION_BOARD

| Field | Value |
|-------|-------|
| States | Backlog → Ready → In Progress → Validation → Regression → Done |
| In Progress | **Max 1** |

---

## Board (2026-08-13)

```text
BACKLOG          READY           IN PROGRESS      VALIDATION       REGRESSION        DONE
PB-002           PB-001          —                —                —                 ITERATION_001
PB-003           (next: 002)                                                          PB-D01…D06
PB-004
PB-005
PB-006
PB-007
PB-008
PB-009
PB-010
PB-011
PB-013
────────────────
DEFERRED         PB-012
REJECTED         PB-R01 R02 R03
```

---

## State rules

| State | Meaning |
|-------|---------|
| Backlog | Evidenced; not sequenced |
| Ready | ROI + layer + regression set filled; may enter 002 |
| In Progress | One iteration is implementing |
| Validation | Target chart rescored |
| Regression | CASE_0001 (+ named holds) run |
| Done | Observed ROI written · checklist closed |

Deferred ≠ Done. Rejected ≠ Backlog.

---

## Current iteration

| Field | Value |
|-------|-------|
| Open | **ITERATION_001** — analytics foundation |
| 001 state | **Done** |
| Next | **ITERATION_002** ← **PB-001** (Ready) |
| Must not | Start PB-002… in parallel |

---

END
