# Strength Confidence Model (Design)

**Status:** DESIGN — not implemented  
**Current production:** `min(1, n_rules/5) + 0.2` → saturates at 1.0 (PILOT-1B: all seven cases = 1.0)

## Purpose

Confidence answers: **How certain is the taxonomy classification?**  
It must not rewrite the score.

## Candidate ordinal levels

| Level | When to use |
|---|---|
| HIGH | Complete evidence; consistent directions; score far from Ti; no major producer conflicts |
| MEDIUM | Minor gaps OR near boundary OR mild opposing masses |
| LOW | Major gaps OR strong conflicts OR upstream uncertainty |
| VERY_LOW | Critical evidence missing (e.g. required interaction producer absent) |
| UNRESOLVED | Cannot responsibly publish a fine label; may publish score + profile only |

## Candidate inputs (design)

| Input | Role |
|---|---|
| evidence completeness | fraction of expected categories present |
| evidence consistency | agree vs oppose mass ratio |
| distance from taxonomy boundary | near Ti → lower confidence |
| source reliability | table vs astronomical vs heuristic |
| interaction complexity | combo/clash present/absent |
| upstream confidence | calendar / bazi certainty |
| calendar confidence | solar-term near-boundary births |
| pattern confidence | follow vs strength tension |
| hidden-stem confidence | rooting reliability |

## Mapping sketch (not a formula)

```text
start MEDIUM
if completeness high AND consistency high AND far from Ti → HIGH
if near Ti OR mild conflict → MEDIUM (cap)
if strong conflict OR incomplete critical evidence → LOW
if critical producer missing → VERY_LOW / UNRESOLVED
```

## Pilot requirement examples

| Case | Production conf | v2 expectation |
|---|---|---|
| 0003 | 1.0 | ≤ MEDIUM (boundary + conflict) |
| 0005 | 1.0 | ≤ MEDIUM (boundary) |
| 0001 | 1.0 | ≤ MEDIUM until sitting-branch evidence policy resolved |
| 0004 / 0007 | 1.0 | HIGH plausible if evidence complete |

## Non-goals this sprint

- No formula implementation  
- No production confidence change  
