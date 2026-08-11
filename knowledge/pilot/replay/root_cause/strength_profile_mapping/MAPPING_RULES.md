# MAPPING_RULES

1. Map only observed fields.
2. If unavailable: `unknown` or `not_available`.
3. Do not infer categorical strength from numeric contribution.
4. Do not reconstruct raw score from published score.
5. Synthetic expected taxonomy and expert labels stay outside StrengthProfile taxonomy fields.
6. Preserve `current_v1_band` as runtime observation only.
7. Saturation metadata is observational (`raw>=50` and `published==1.0`).
