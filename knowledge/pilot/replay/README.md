# BTE Pilot Replay

**Sprint:** Post Beta-5 validation  
**Scope:** CASE-0001 → CASE-0009  
**Architecture Freeze:** AF-1 unchanged  

## Purpose

First real Pilot Replay of BTE v1.0 against expert/reference cases.

Goal is truth, not green results:

- how far the live runtime actually runs
- where actual diverges from expert/external expected
- what is missing (Decision, Transformation, public Luck, Portal)

## Canonical harness

```text
applications.api.services.orchestrator.OrchestratorService.analyze
```

Reused existing production orchestrator. No second engine/harness invented.

Replay runner (report-only, outside frozen engines):

```text
python knowledge/pilot/replay/run_pilot_replay.py
```

## Expected / Actual separation

| Field | Meaning |
|---|---|
| `expert_expected` | Expert strength / pillars |
| `external_expected` | Reference-only external labels (CASE-0008/0009) |
| `actual_result` | Live orchestrator output |

Expected is never overwritten by Actual.

## Verdict legend

| Verdict | Meaning |
|---|---|
| PASS | Runtime ran and matched expert expected at evaluated strength/pillar layers |
| DISCREPANCY | Runtime ran; first divergence found |
| BOUNDARY | Soft/boundary expert label; do not force engine |
| BLOCKED | Cannot run (missing data / not wired) |
| REFERENCE_ONLY | External reference recorded; not absolute ground truth |

Layer statuses may also be: `EXECUTED`, `EXECUTED_NEGATIVE`, `INTERNAL_ONLY`, `NOT_PRODUCED`.

`PASS` is never used for fixture/schema-only checks, or for Interpretation/Report without expert expected content.

## Layout

```text
knowledge/pilot/replay/
  README.md
  PILOT_REPLAY_SUMMARY.md
  CASE_MATRIX.md
  DISCREPANCY_REPORT.md
  BLOCKED_CASES.md
  ROOT_CAUSE_ANALYSIS.md
  REPLAY_VALIDATION.md
  run_pilot_replay.py
  fixtures/          # input + expected only
  results/           # per-case JSON + summary/matrix
  snapshots/         # canonical outputs + trace/audit/diagnostics
  cases/             # CASE-0001.md … CASE-0009.md
```

## Freeze compliance

Not modified:

- AF-1 / Foundation
- `engines/`
- `knowledge/packages/`
- `pipelines/`
- API contracts / Product UI / deployment / commercial
- frozen Pilot strategy documents under `knowledge/pilot/` (program docs)

Modified/created: Pilot Replay artifacts under `knowledge/pilot/replay/` only.
