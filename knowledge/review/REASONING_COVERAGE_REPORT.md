# Reasoning Coverage Report

## Totals

| Metric | Value |
| --- | --- |
| Chains | 73 |
| Nodes | 529 |
| Edges | 508 |
| Packages with reasoning | 14 / 15 |
| Packages with orphan (no) reasoning | bz_09_luck_foundation |

## Chains by package

| Package | Chains | Nodes | Edges |
| --- | --- | --- | --- |
| bz_01 | 3 | 39 | 38 |
| bz_02 | 3 | 21 | 24 |
| bz_03 | 3 | 21 | 24 |
| bz_04 | 3 | 21 | 24 |
| bz_05 | 3 | 21 | 24 |
| bz_06 | 3 | 21 | 24 |
| bz_07 | 5 | 35 | 40 |
| bz_08 | 5 | 35 | 40 |
| bz_09 | 0 | 0 | 0 |
| bz_10 | 6 | 42 | 36 |
| bz_11 | 7 | 49 | 42 |
| bz_12 | 8 | 56 | 48 |
| bz_13 | 8 | 56 | 48 |
| bz_14 | 8 | 56 | 48 |
| bz_15 | 8 | 56 | 48 |

## Coverage pattern (KX-5/6)

Required scenario families are present:

- Follow: true / false / border / contra / lowconf / mixed
- Transformation: success / failed / partial / conflict / border / lowconf / mixed
- Combination & Clash: pure combo / pure clash / mixed / priority / border / lowconf / conflict / cascade
- Ten Gods: balanced / dominant / weak / conflict / special / border / lowconf / mixed
- Twelve Growth: prosperous / declining / balanced / dominant / transition / border / lowconf / mixed
- Hidden Stems: strong roots / weak roots / balanced / dominant / special / border / lowconf / mixed

Upstream ID references on KX-5/6 chains (FPC/PAT/PEV/SKC/SEC/TEC/TRC/CBC/TGA/TGP) were verified by package tests at seal time. This review does not re-mutate those files.

## Orphan reasoning

| Kind | Finding |
| --- | --- |
| Package with no graphs | bz_09_luck_foundation |
| Broken chain → missing rule id | None detected in sealed KX-5/6 test gates |
| Nodes without edges | Alternative/conflict nodes are optionally edged (weight below 1) — by design, not orphans |

## Gaps

- Luck timeline has no RC/RN/RE artifacts.
- Interpretation narrative chains do not exist (no interpretation package).
- Early packages (bz_01–bz_06) have fewer scenario families (3 chains) than later Gold advanced packs (6–8).
