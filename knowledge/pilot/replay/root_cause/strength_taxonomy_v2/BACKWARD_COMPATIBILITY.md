# Backward Compatibility — Taxonomy v1 ↔ v2

**Status:** CONCEPTUAL DESIGN — not implemented  

## Versions

| Version | Levels |
|---|---|
| v1 (production today) | weak / balanced / strong |
| v2 (candidate) | VERY_WEAK … VERY_STRONG |

## Conceptual mapping (example only)

| v2 | → v1 |
|---|---|
| VERY_WEAK | WEAK |
| WEAK | WEAK |
| SLIGHTLY_WEAK | WEAK |
| BALANCED | BALANCED |
| SLIGHTLY_STRONG | STRONG |
| STRONG | STRONG |
| VERY_STRONG | STRONG |

## Evaluation of this mapping

| Pros | Cons |
|---|---|
| Stable for coarse API consumers | Loses tilt/intensity (the reason v2 exists) |
| Easy migration | SLIGHTLY_STRONG→STRONG repeats v1 cliff pain |
| | SLIGHTLY_WEAK→WEAK may overstate weakness |

**Acceptable** only as **compatibility projection**, never as the sole published truth once v2 ships.

## Preferred coexistence

```text
strength_score              # unchanged continuous SSOT
strength_level_v1           # mapped or legacy scorer
strength_level_v2           # fine taxonomy when ready
strength_profile            # explanation
strength_confidence         # certainty
taxonomy_version            # "v1" | "v2"
```

## Migration strategy (future)

1. Ship profile + confidence without changing v1 labels  
2. Add v2 behind flag / dual publish  
3. Golden Expected gains optional `strength_level_v2` without deleting v1  
4. Deprecate v1-only clients on contract version bump  

## API / display / Golden

| Surface | Compatibility rule |
|---|---|
| API | Additive fields; no silent rename of `strength_level` without version |
| UI | Show v2 when contract says v2; keep v1 badge during transition |
| Golden Dataset | Dual columns during migration; no Expected wipe |

## Do not implement in PILOT-1C
