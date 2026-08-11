# PROFILE_MAPPING_REPORT

## Coverage

- Total mapped: **23**
- REAL_CALIBRATION: **2** (CAL-000001, CAL-000006)
- SYNTHETIC_STRESS: **21**

## Field classes

DIRECT=14 PARTIAL=5 DERIVED=5 NOT_AVAILABLE=10 UNKNOWN=0

## Diagnostic answers

1. **How much of the Profile can be populated?** Useful core (score, buckets, season/root labels, support/pressure/drain labels, saturation) — many structural/loci fields remain unavailable.
2. **Direct fields?** day_master, scores, v1 band, buckets, month_status, root_level/count, season/phase, matched_rules.
3. **Require derivation?** saturation flag, conflicts from opposing signs, completeness/confidence qualitative factors, evidence records from buckets/ledger.
4. **Unavailable?** root loci, clash/punishment/harm/destruction, follow, seasonal_strength_state enum (not inferred).
5. **Permanently lost at current engine boundary?** sitting hidden pressure; per-branch root distribution; native conflict objects.
6. **Enough for a useful Profile?** YES for diagnostic Profile / information-loss analysis; NO for complete multidimensional Profile.
7. **Future engine outputs needed?** root loci, structural interaction facts, explicit evidence items with scopes, optional unclamped score publication.
8. **Raw score preserved?** YES when present in source.
9. **Saturation preserved?** YES as observational metadata (7 upper_clamp cases observed).
10. **Independent of future taxonomy?** YES — no taxonomy_v2 / T1-T6 fields.

## Population differences

- CAL cases include ledger + optional TemperatureEngine dual source + expert external reference.
- SYN cases include context+buckets+matched_rules; no ledger; synthetic flags required.
