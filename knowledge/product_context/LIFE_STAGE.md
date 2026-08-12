# LIFE_STAGE

## Canonical stages

| Stage | Age (completed years) |
|-------|------------------------|
| CHILD | 0–12 |
| TEEN | 13–17 |
| YOUNG_ADULT | 18–24 |
| ADULT | 25–44 |
| MID_CAREER | 45–59 |
| SENIOR | 60+ |

## Entry rules

1. Explicit `life_stage` on input wins when provided.  
2. Else compute age from birth date vs `as_of` (default today).  
3. If age unknown → **ADULT** (safe commercial default for golden adult cases).  
4. CHILD with `reader_role=UNKNOWN` promotes audience to **PARENT**.
