# SUPPORT_PRESSURE_DIAGNOSTIC

**Sprint:** PILOT-1H  
**Cases:** CAL-000001, CAL-000006, SYN-STR-000007, SYN-STR-000008

## Preservation checklist

| Property | Current score behavior |
|---|---|
| magnitude | PARTIAL — bucket sums only |
| direction | YES — signed contributions |
| source | LOST after aggregation (rules list helps; profile buckets coarse) |
| type | PARTIAL — single support_type / control_type winners |
| confidence | NOT preserved per factor (global confidence often 1.0) |

## Case contrasts

### CAL-000001 / SYN-STR-000007

Support mass (season/root/companion/special) outweighs officer pressure in the sum → `strong` @ 0.87.  
Experts (real) / synthetic expect slightly_weak. Score preserves net magnitude/direction of the *sum*, not the interpretive priority experts give to moc/hoa pressure / sitting fire.

### CAL-000006

Near cancellation: support+root ≈ season+control → balanced @ 0.50. Experts still SLIGHTLY_WEAK (tilt). Score loses tilt once net ≈ 0.

### SYN-STR-000008

Support present but season/control/drain keep net slightly negative → balanced @ 0.39. Synthetic slightly_weak wants weak-side naming.

## Conclusion

Support vs pressure are **present as signed buckets** but **source/type/confidence are compressed**. A profile layer should keep support_state and pressure_state as first-class vectors, not only net score.
