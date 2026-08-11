# V1_TO_V2_PROJECTION_ANALYSIS

**Sprint:** PILOT-1H  
**Conceptual only — not implemented**

## Coarse projection (design compatibility)

| v2 candidate | -> v1 |
|---|---|
| very_weak | weak |
| weak | weak |
| slightly_weak | weak |
| balanced | balanced |
| slightly_strong | strong |
| strong | strong |
| very_strong | strong |

## Distinctions impossible under current 3-band contract

1. very_weak vs weak  
2. weak vs slightly_weak  
3. slightly_weak vs balanced (tilt)  
4. balanced vs slightly_strong (tilt)  
5. slightly_strong vs strong  
6. strong vs very_strong  

## Additional impossibility from score clamp

Even a future v2 mapper cannot recover STRONG vs VERY_STRONG from published `strength_score` alone once both are 1.000 — needs raw_total, unclamped score, or profile intensity.

## Implication

v1 remains coarse API compatibility. v2 requires additive fields + profile, not a silent remap of `strength_level`.
