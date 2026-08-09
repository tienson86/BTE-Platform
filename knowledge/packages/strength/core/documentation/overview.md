# Strength Core — Documentation

## Package purpose

Provide the canonical, package-deployable Strength knowledge used to judge whether the Day Master is strong, weak, or balanced.

## Analytical scope

| In scope | Out of scope |
|----------|----------------|
| Month command / 旺相休囚死 | Pattern naming (Cách Cục) |
| Month branch ten-god relation | Follow-pattern success/failure (only a tendency hint) |
| Thông căn and root quality | Useful / Favorable / Unfavorable God choice |
| Hidden and visible stem support | Luck pillar strength |
| Element support and restriction | Interpretation sentences / report blocks |
| Score baseline, stacks, level bands | Engine execution code |

## Assumptions

1. Chart pillars and ten gods are already computed upstream (Calendar / BaZi / Ten Gods domains).
2. `month_status` may be supplied by the engine or inferred by element×season rules in this package.
3. Weights follow BTE traditional tables (`database/12_strength`, `database/15_score_engine/03_strength`): prosperous 35, growing 25, rest 10, imprison −10, dead −25; root 30/22/12/6/−20; strong/weak thresholds 0.65 / 0.35.
4. Baseline score is 50/100.
5. One evidence pillar is not double-counted inside the same factor group.
6. School is `bazi_default`. Other schools ship as override packages (`OVR-PACKAGE`).

## Limitations

- Not a full 10 stems × 12 branches Chang Sheng matrix (only representative root-quality rules).
- Follow / fake-follow is not decided here.
- Special extreme structures (pure/mixed) are only partially covered via combinations already in V1; this core focuses on foundations.
- Multilingual display text beyond `vi` is not shipped; ids are stable for later language packs.
- This package does not execute inside the Analysis Engine until a future integration sprint.

## Future expansion roadmap

1. KX-1B — Chang Sheng × stem/branch strength table as an extension package.
2. School overlay packages (e.g. Ziping-strict vs modern weighted).
3. Language packs (`en`, `zh-Hans`) sharing the same `SKC-*` ids.
4. Engine adapter to dual-read this package beside V1 CSV.
5. Override package for project-specific thresholds without mutating 1.0.0 bytes.
