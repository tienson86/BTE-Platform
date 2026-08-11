# STRENGTH_PROFILE_REQUIREMENTS

**Sprint:** PILOT-1H  
**Status:** REQUIREMENTS ONLY — do not implement

## Conceptual stack

```text
Evidence -> Weighting -> Score -> Profile -> Taxonomy -> Confidence -> Contract
```

Score remains useful continuous measure. Profile explains composition/conflict. Taxonomy classifies. Confidence qualifies.

## Candidate dimensions

| Dimension | Purpose | Source | Value type | Available now | Currently lost | Why taxonomy may need it |
|---|---|---|---|---|---|---|
| season_state | month command / phase | month_status, season, season_phase | enum + optional phase | PARTIAL | branch identity | separates death-season cancellation from quiet mid |
| rooting_state | where/how rooted | root_level, root_count, branch loci | enum + count + loci | PARTIAL | loci | VERY_WEAK vs WEAK intensity |
| support_state | companion/resource mass | support_type, resource/companion lists | vector | PARTIAL | multi-source | tilt vs net |
| pressure_state | officer/wealth/output | control/drain lists | vector | PARTIAL | sitting hidden pressure | expert disagreements |
| drain_state | leakage detail | drain_type, counts | enum + count | PARTIAL | overlap with control | slightly_* edges |
| structural_state | special/combo/follow | special matches; Pattern later | flags | PARTIAL | follow not in strength | overrides |
| temperature_state | climate framing | context vs TemperatureEngine | enum + source tag | CONTEXT | dual sources | winter An special interactions |
| evidence_conflict | opposing large masses | bucket signs/magnitudes | bool/score | DERIVABLE | not published | balanced cancellation vs quiet |
| evidence_completeness | missing dimensions | builder coverage | enum/float | PARTIAL | not on contract | confidence |
| confidence | certainty of label | completeness, conflict, calendar, boundary | enum/float | WEAK (often 1.0) | non-discriminative | boundary publishing |

## Necessity verdict

**Profile layer REQUIRED** before Taxonomy v2 implementation. Score alone is NOT_SUFFICIENT (collisions, saturation, dual-reviewed disagreement).
