# MODULE_SPEC.md — Temperature Rule Database

> Module: 03_temperature_rules
>
> Version: 1.0.0
>
> Status: Active
>
> BTE Platform

---

# 1. Purpose

Defines the Temperature Rule Database: seasonal temperature influence, climate correction, dry/humid balance, element adjustment, and cross-module interaction with Strength and Season modules.

---

# 2. Scope

| In scope | Out of scope |
|----------|--------------|
| Seasonal temperature influence | Pattern matching |
| Climate correction by month branch | Useful god selection logic |
| Dry/humid balance | Strength month command |
| Hot/cold balance and classification | Report formatting |
| Element temperature bias | |
| Cross-module Strength/Season interaction | |

---

# 3. Rule Taxonomy

| Family | Count |
|--------|-------|
| season_influence | 4 |
| season_phase_influence | 2 |
| climate_correction | 4 |
| branch_climate | 2 |
| dryness_score | 5 |
| humidity_score | 5 |
| hot_cold_balance | 5 |
| element_temperature | 5 |
| special_case | 4 |
| moisture_flow | 4 |
| cross_module | 5 |
| group_priority | 7 |
| level_classification | 4 |

**Total rules:** 56

---

# 4. Dependencies

See `DEPENDENCIES.json`:

- **depends_on:** `01_strength_rules`, `02_season_rules`
- **used_by:** `04_pattern_rules`, Useful God Engine
- **execution_order:** Season → Strength → Temperature → Pattern

---

# 5. Configuration

| Key | Value |
|-----|-------|
| baseline | 35 |
| scale | 100 |
| divisor | 3 |
| hot_threshold | 0.65 |
| cold_threshold | 0.35 |

---

# 6. Output

Temperature level: `cold` | `cool` | `warm` | `hot`

---

# 7. Validation

- 62 objects validated
- Golden examples: 6
- Test cases: 6
