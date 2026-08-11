# MISMATCH_ANALYSIS

**Sprint:** PILOT-1G  
**Policy:** Do not patch production Strength behavior from synthetic mismatches.

Total mismatches: **5** / 21

## By category

| mismatch_category | count | cases |
|---|---:|---|
| TAXONOMY_RESOLUTION_GAP | 3 | SYN-STR-000008, SYN-STR-000009, SYN-STR-000015 |
| SEASONAL_WEIGHTING_GAP | 1 | SYN-STR-000004 |
| SUPPORT_PRESSURE_GAP | 1 | SYN-STR-000007 |

## Case notes

### SYN-STR-000004

- synthetic_expected_taxonomy: `weak`
- projected expected v1: `weak`
- runtime v1: `balanced` score=`0.420`
- category: `SEASONAL_WEIGHTING_GAP`
- evidence_profile: weak moc with limited rooting
- note: Projected expected v1=weak vs runtime v1=balanced for synthetic_expected_taxonomy=weak.
- likely reason: diagnostic disagreement between synthetic stress intent and current v1 score/band projection; not proven production defect.

### SYN-STR-000007

- synthetic_expected_taxonomy: `slightly_weak`
- projected expected v1: `weak`
- runtime v1: `strong` score=`0.870`
- category: `SUPPORT_PRESSURE_GAP`
- evidence_profile: kim has support but faces moc/hoa pressure
- note: Projected expected v1=weak vs runtime v1=strong for synthetic_expected_taxonomy=slightly_weak.
- likely reason: diagnostic disagreement between synthetic stress intent and current v1 score/band projection; not proven production defect.

### SYN-STR-000008

- synthetic_expected_taxonomy: `slightly_weak`
- projected expected v1: `weak`
- runtime v1: `balanced` score=`0.390`
- category: `TAXONOMY_RESOLUTION_GAP`
- evidence_profile: thuy has limited support under hoa/tho pressure
- note: Projected expected v1=weak vs runtime v1=balanced for synthetic_expected_taxonomy=slightly_weak.
- likely reason: diagnostic disagreement between synthetic stress intent and current v1 score/band projection; not proven production defect.

### SYN-STR-000009

- synthetic_expected_taxonomy: `slightly_weak`
- projected expected v1: `weak`
- runtime v1: `strong` score=`0.670`
- category: `TAXONOMY_RESOLUTION_GAP`
- evidence_profile: kim has direct root but faces strong hoa pressure
- note: Projected expected v1=weak vs runtime v1=strong for synthetic_expected_taxonomy=slightly_weak.
- likely reason: diagnostic disagreement between synthetic stress intent and current v1 score/band projection; not proven production defect.

### SYN-STR-000015

- synthetic_expected_taxonomy: `slightly_strong`
- projected expected v1: `strong`
- runtime v1: `weak` score=`0.310`
- category: `TAXONOMY_RESOLUTION_GAP`
- evidence_profile: moc pressure exists but tho retains rooting and fire support
- note: Projected expected v1=strong vs runtime v1=weak for synthetic_expected_taxonomy=slightly_strong.
- likely reason: diagnostic disagreement between synthetic stress intent and current v1 score/band projection; not proven production defect.

## Recommendation

- Keep mismatches as taxonomy-v2 / profile-design evidence.
- Do not modify Strength Engine, rules, or thresholds in this sprint.
- Prefer real dual-reviewed calibration charts before any production change.
