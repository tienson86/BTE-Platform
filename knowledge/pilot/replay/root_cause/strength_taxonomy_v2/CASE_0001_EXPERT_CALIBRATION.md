# CASE-0001 Expert Calibration (PILOT-1D)

**Calibration ID:** CAL-000001  
**Source:** CASE-0001 / EXISTING_PILOT  
**Expert reference:** balanced / slightly weak → candidate `SLIGHTLY_WEAK`  
**Runtime:** 0.87 / strong  
**Dual review:** PENDING  

## Hypotheses from PILOT-1C (no production weight change)

| Hypothesis | Evidence | Traditional rationale | Expert agreement | Confidence | Influence Strength? | Interpretation only? | Contextual? | Reject? |
|---|---|---|---|---|---|---|---|---|
| Sitting Ngọ fire under-scored | Day branch Ngọ vs Canh Kim; not in visible-stem control list | Day sitting 七杀/伤 is classical weaken | Reference expert weaker than runtime → consistent with gap | MEDIUM | **Yes (candidate general policy)** | No | Also contextual | No |
| Officer dedup ctl_001+ctl_006 | Same Thất Sát family double-counted | One restriction event | Neutral / modeling hygiene | HIGH | **Yes (general)** | No | No | No |
| Reduce sea_002 magnitude | +25 Tướng | 相 real; magnitude high for mid charts | Plausible | MEDIUM | Possible | No | Season contextual | No |
| Reduce spc_004 when season seal-aligned | +10 stacks with Tướng | Avoid double theme | Plausible | MEDIUM | Possible | No | Contextual | No |
| Inject TemperatureEngine into Strength now | cold context vs hot engine | Sources conflict | Uncertain | LOW | **Not until SSOT** | Possibly | Yes | **Reject as immediate scorer input** |
| Case-specific CASE-0001 multiplier | Would fit expert | Overfitting | Reject | HIGH | No | No | No | **Reject** |

## Calibration conclusion

- Keep CAL-000001 in conflict + low-confidence cohorts.  
- Do **not** special-case production rules.  
- General evidence policies (sitting branch, officer dedup) remain **calibration hypotheses** for a future design sprint after more cases.  
- Dual independent expert review still required before treating label as adjudicated.
