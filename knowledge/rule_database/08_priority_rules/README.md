# Priority Rule Database

> Module: Rule Database
>
> Version: 1.0.0
>
> Status: Active
>
> Document Type: Module README
>
> BTE Platform

---

# 1. Purpose

`08_priority_rules/` is the JSON Rule Database module for **Priority** resolution in the BTE Knowledge Base.

It defines module execution order, rule priority, override rules, conflict resolution, tie-breaking, fallback selection, weighted selection, score normalization, and final rule selection across all upstream modules.

---

# 2. Module Files

| File | Purpose |
|------|---------|
| `README.md` | Module documentation |
| `MODULE_SPEC.md` | Module specification |
| `PRIORITY_HIERARCHY.md` | Priority hierarchy and override order |
| `PRIORITY_DECISION_TREE.md` | Resolution decision flow |
| `DEPENDENCIES.json` | Pipeline dependencies and execution order |
| `CHANGELOG.md` | Version history |
| `MANIFEST.json` | File catalog and taxonomy |
| `RULE_INDEX.json` | Deterministic rule lookup index |
| `STATISTICS.json` | Aggregate statistics and coverage metrics |
| `priority_rules.json` | Complete rule dataset (69 rules) |
| `priority_examples.json` | Golden examples (6 scenarios) |
| `TEST_CASES.json` | Structured test cases |
| `validation_report.json` | Level 1–5 validation report |

---

# 3. Pipeline

```
Season → Strength → Temperature → Pattern → Special Case → Follow Pattern → Combination → Priority
```

Depends on: `01_strength_rules/` through `07_combination_rules/`

Used by: Useful God Engine, Score Engine

---

# 4. Taxonomy

| Category | Count |
|----------|-------|
| module_priority | 7 |
| rule_priority | 11 |
| override | 6 |
| conflict_resolution | 5 |
| tie_breaking | 4 |
| fallback | 3 |
| weighted_selection | 14 |
| score_normalization | 7 |
| execution_order | 8 |
| final_selection | 4 |

**ID prefix:** `PRI` | **Range:** PRI-000001 to PRI-000069

---

# 5. Rule Model

Every rule follows BTE Rule Model v1.0.0:

```
Rule
├── Identity (id, code, name)
├── Classification (domain, category, family, type)
├── Source
├── Target
├── Conditions
├── Evaluation
├── Priority
├── Lifecycle
├── Documentation
└── Metadata
```

**Domain:** `priority`

**Target:** `rule_set.priority_resolution`

---

# 6. Configuration

| Key | Value |
|-----|-------|
| baseline | 50 |
| scale | 100 |
| confidence_threshold | 0.65 |
| pipeline_stages | 8 |

---

# 7. Data Sources

- `database/14_pattern/05_priority_rules.csv`
- `database/13_useful_god/05_priority_rules.csv`
- `database/12_strength/06_priority_rules.csv`
- `database/15_score_engine/09_final_score/04_dimension_weight.csv`
- `database/15_score_engine/08_luck/05_luck_priority.csv`

---

# 8. Governance

- Version: `1.0.0`
- Origin: `rule_database`
- Reference: `01_strength_rules/` through `07_combination_rules/`
- Spec: `MODULE_SPEC.md`
- Validation: Level 1–5 per `VALIDATION_STANDARD.md`
- Reference example: `knowledge/docs/reference_examples/rule/rule_complete_v1.json`

---

# 9. Related Documents

| Document | Role |
|----------|------|
| `PRIORITY_HIERARCHY.md` | Override and module hierarchy |
| `PRIORITY_DECISION_TREE.md` | Resolution flow |
| `DEPENDENCIES.json` | Upstream/downstream modules |
| `VALIDATION_STANDARD.md` | Validation levels |
| `knowledge/ROADMAP.md` | Phase 2 Rule Database |

---

# 10. Conclusion

This module is the **final resolution layer** in the BTE analysis pipeline. It consumes outputs from modules 01–07 and produces `priority_resolution` for downstream Score and Useful God engines.
