# Pilot Replay Summary

**Run date:** 2026-08-10 (UTC)  
**Entrypoint:** `OrchestratorService.analyze`  
**Engine/Knowledge/API/UI modified:** No  

## Verdict totals

| Verdict | Count | Cases |
|---|---:|---|
| PASS | 2 | CASE-0004, CASE-0007 |
| DISCREPANCY | 4 | CASE-0001, CASE-0002, CASE-0005, CASE-0006 |
| BOUNDARY | 1 | CASE-0003 |
| BLOCKED | 1 | CASE-0009 |
| REFERENCE_ONLY | 1 | CASE-0008 |

## What actually runs today

Public pipeline from orchestrator:

```text
calendar → bazi → pattern → score → interpretation → report → narrative
```

Also produced on public payload (truth views):

- strength
- temperature
- useful_god

Internal but stripped from public payload:

- luck (`_INTERNAL_PAYLOAD_KEYS`)
- rule_context / knowledge / matching / priority / feng_shui

Not wired into OrchestratorService:

- DecisionEngine
- transformation_* producers (combination ≠ transformation)

Portal DOM replay: not started → BLOCKED for portal layer.

## Headline findings

1. **Calendar/BaZi is mostly solid** for expert birth datetimes — 6/7 runnable expert cases match confirmed four pillars. CASE-0006 fails month pillar (expected Đinh Tỵ, actual Mậu Ngọ).
2. **Strength taxonomy is too coarse** (strong / balanced / weak only). Expert labels like “trung bình thiên nhược/vượng” and “rất vượng” cannot be expressed → systematic DISCREPANCY / granularity gap.
3. **Strength polarity can oppose expert** (CASE-0001: expert thiên nhược vs actual Thân vượng 0.87).
4. **Follow detection runs** (CASE-0003 Tòng Nhi, CASE-0007 Tòng Tài) but CASE-0008 Follow Wealth reference could not be replayed (no birth datetime).
5. **Transformation is not produced** on production public path → CASE-0009 blocked on missing reference data and systemic producer gap.
6. **Interpretation/Report execute** but have no expert expected content in this round → marked EXECUTED, not PASS.

## Runtime coverage

| Layer | Covered? | Notes |
|---|---|---|
| Input / Validation | Yes | |
| Calendar / BaZi | Yes | CASE-0006 month mismatch |
| Strength | Yes | 3-level taxonomy |
| Temperature | Yes | |
| Pattern / Follow | Partial | Follow heuristic present; many cases negative |
| Transformation | No | NOT_PRODUCED |
| Decision | No | Not in orchestrator |
| Luck (public) | No | INTERNAL_ONLY |
| Interpretation | Yes (execute) | No expert expected |
| Report / Narrative | Yes (execute) | No expert expected |
| Portal DOM | No | BLOCKED |

## Recommended next action

1. Triage CASE-0006 month-pillar divergence (Calendar/BaZi input or solar-term boundary) without changing Expected.
2. Decide whether Strength V1 taxonomy must expand beyond 3 bands before Pilot expert acceptance.
3. Supply birth datetime for CASE-0008 and a verified transformation reference chart for CASE-0009 before claiming Follow/Transform coverage.
4. Expose or separately snapshot Luck/Decision only after product contract decision — do not invent publishers in Pilot Replay.
