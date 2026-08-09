# Change Impact Guide

How to evolve knowledge after AF-1 freeze without breaking KX-6D findings.

## Allowed without touching sealed packages

- New packages (`bz_16+`)
- New review / release / engine-adapter docs
- Engine / pipeline **wrappers** that *read* published contracts
- Golden Datasets stored outside sealed package checksum scope (RM policy)

## Requires SemVer + RM (do not silent-edit)

| Change | Impact fan-out |
| --- | --- |
| Rename a published output | All downstream `published_inputs` + engines + Interpretation |
| Add required dependency | Breaks independent deploy; avoid |
| Change score_target or condition field set | Rule + evidence + reasoning + tests |
| Split bz_12 by taxonomy | New packages; keep bz_12 1.0.0 as compatibility wrapper |
| Backfill bz_01–bz_04 publish assets | Patch/minor on those IDs only; consumers already assume names |

## High blast radius outputs

Treat as frozen names:

`strength_score`, `season_score`, `temperature_score`, `pattern_score`, `pattern_quality`, `pattern_confidence`, `pattern_integrity`, `pattern_stability`, `resolved_useful_god`, `decision_priority`, `resolution_confidence`, `follow_pattern`, `follow_pattern_score`, `transformation_score`, `interaction_score`, `ten_gods_profile`, `growth_profile`, `growth_score`.

## Low blast radius (no in-ecosystem consumer yet)

`final_useful_god`, `override_*`, all `hidden_stems_*`, most `*_diagnostics` / `*_reasoning` tails, bz_09 timeline outputs.

## Forbidden (this freeze)

- Editing Foundation / Architecture / sealed package bytes to “make review greener”
- Recalculating charts inside a later analytical package
- Generating interpretation text inside analytical packages
- Required circular dependencies

## Impact checklist before any future package SemVer

1. Producer matrix: who publishes the name?
2. Consumer matrix: who lists it in inputs?
3. Runtime graph: order still valid?
4. Evidence + reasoning IDs still 1:1?
5. Checksum reseal + PVP-RELEASE?
6. Update this `knowledge/review/` folder additively (new dated note or 1.1 review pack) — do not rewrite history silently.
