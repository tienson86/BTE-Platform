# Synthetic Strength Stress Dataset — PILOT-1G

**Dataset type:** `SYNTHETIC_STRENGTH_STRESS`  
**Status:** Engine testing only — **not** calibration evidence.

## Purpose

Deliberately constructed BaZi pillar structures (21 cases) covering seven candidate Strength taxonomy levels. Used to stress the existing Strength Engine and diagnose taxonomy/score gaps.

## Non-goals

- Not real-person calibration
- Not Golden Dataset material
- Not production Expected
- Does not implement Taxonomy v2
- Does not modify Strength Engine / rules / thresholds

## Layout

```text
synthetic_strength/
  datasets/SYN-STR-*.json
  results/SYN-STR-*.json
  harness/          # test-only adapter + replay
  tests/
  validation/
  *.md reports
```

## Identifiers

Use `SYN-STR-000001` … `SYN-STR-000021` only.  
Do **not** create `CAL-*` ids in this sprint.

## Language rule

Machine-readable pillar tokens are ASCII Vietnamese BTE names (`binh_ngo`, `quy_ti`, …).  
No Han / Japanese / Korean characters in fixtures.

## How to replay

```text
PYTHONPATH=. python -m knowledge.pilot.replay.synthetic_strength.harness.replay
PYTHONPATH=. python knowledge/pilot/replay/synthetic_strength/generate_reports.py
python -m pytest knowledge/pilot/replay/synthetic_strength/tests -q
```

## Eligibility flags (all cases)

| Flag | Value |
|---|---|
| calibration_eligible | false |
| golden_eligible | false |
| expert_calibration_eligible | false |
| production_expected | false |
| synthetic_pillars | true |
| calendar_verified | false |
