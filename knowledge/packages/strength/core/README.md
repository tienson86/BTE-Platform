# Strength Knowledge Package — Core Foundation

| Field | Value |
|-------|-------|
| **package_id** | `bz_01_strength_core` |
| **Version** | 1.2.0 |
| **Type** | analytical |
| **Domain** | `DOM-STRENGTH` |
| **Sprint** | KX-1A + KX-1B + KX-1C |
| **Status** | released |

Canonical Day Master strength (thân vượng / thân nhược) knowledge package for BTE Knowledge Database V2.

This package is independently versioned and deployable. It does **not** modify the Rule Engine, Analysis Engine, or `knowledge/rule_database/01_strength_rules/`. Existing V1 strength CSV/JSON remain authoritative for current engine execution until a future wiring sprint.

Repo path `knowledge/packages/strength/core/` is the domain-nested location (KX-1A). Distribution folder name is `bz_01_strength_core`.

---

## Purpose

Declare production-quality rules that evaluate Day Master strength from:

- seasonal / month-command influence (旺相休囚死)
- month branch relations
- root (thông căn)
- hidden-stem and visible-stem support
- five-element support and restriction
- strength-level tendencies and scoring policy

## Analytical scope

In scope: natal chart strength factors and score/level classification used by later Analysis Engine consumers.

Out of scope: Useful God selection, Pattern / Follow Pattern success, luck-cycle strength, interpretation prose, report layout.

## Language

Primary: `vi`. Identifiers and codes are language-neutral for multilingual expansion.

## Reasoning Layer

Deterministic graphs under `reasoning/` (framework v1.0.0). See `knowledge/reasoning/REASONING_FRAMEWORK.md`.

## Evidence Layer

Every rule has an Evidence Bundle under `evidence/bundles/`. See `documentation/evidence_model.md`.

## School

`bazi_default` (traditional BTE weights aligned with `database/12_strength` and `database/15_score_engine/03_strength`). Future school overlays SHOULD be separate override packages.
