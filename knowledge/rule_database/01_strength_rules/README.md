# Strength Rule Database

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

`01_strength_rules/` is the JSON Rule Database module for **Day Master Strength** analysis in the BTE Knowledge Base.

It provides a canonical, framework-compliant representation of Strength Engine rules aligned with:

- `RULE_MODEL_SPEC.md`
- `RULE_SCHEMA_REFERENCE.md`
- `METADATA_STANDARD.md`
- Executable CSV source: `database/12_strength/`

---

# 2. Module Files

| File | Purpose |
|------|---------|
| `README.md` | Module documentation |
| `CHANGELOG.md` | Version history |
| `MANIFEST.json` | File catalog and taxonomy |
| `strength_rules.json` | Complete rule dataset (45 rules) |
| `strength_examples.json` | Golden examples for regression |
| `validation_report.json` | Level 1–5 validation report |

---

# 3. Taxonomy

| Category | Count | ID Range | Description |
|----------|-------|----------|-------------|
| season | 5 | STR-000001–005 | Month command phases |
| root | 5 | STR-000006–010 | Root strength levels |
| support | 7 | STR-000011–017 | Supportive influences |
| control | 6 | STR-000018–023 | Control and penalty |
| drain | 5 | STR-000024–028 | Drain and exhaustion |
| special | 4 | STR-000029–032 | Special case overrides |
| combination | 3 | STR-000033–035 | Multi-factor combinations |
| priority | 10 | STR-000036–045 | Group priority and level classification |

**ID prefix:** `STR` (per `NAMING_CONVENTIONS.md`)

---

# 4. Rule Model

Every rule follows the BTE Rule Model:

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

**Domain:** `strength`

**Target:** `day_master.strength_score`

---

# 5. Configuration

Normalization config in `strength_rules.json`:

| Key | Value | Description |
|-----|-------|-------------|
| baseline | 50 | Score baseline |
| scale | 100 | Normalization scale |
| strong_threshold | 0.65 | Strong classification threshold |
| weak_threshold | 0.35 | Weak classification threshold |

---

# 6. Engine Value Mapping

JSON condition values use English `snake_case` enums. Map to Strength Engine V2 Vietnamese runtime values:

| JSON Value | Engine Value |
|------------|--------------|
| prosperous | Đắc lệnh |
| peak | Tướng |
| rest | Hưu |
| imprisoned | Tù |
| dead | Tử |
| root_three_plus | Thông căn 3 chi trở lên |
| root_two | Thông căn 2 chi |
| root_one | Thông căn 1 chi |
| hidden_root | Thông căn tàng can |
| no_root | Vô căn |

---

# 7. Pipeline Position

```
Calendar → Bazi → Strength Engine → Temperature → Pattern → Useful God → Context
```

---

# 8. Governance

- Semantic Versioning: `1.0.0`
- Origin: `rule_database`
- Author: `BTE`
- Validation: Level 1–5 per `VALIDATION_STANDARD.md`
- Reference example: `knowledge/docs/reference_examples/rule/rule_complete_v1.json`

---

# 9. Related Documents

| Document | Role |
|----------|------|
| `database/12_strength/README.md` | Executable CSV database |
| `RULE_AUTHORING_GUIDE.md` | Authoring process |
| `VALIDATION_STANDARD.md` | Validation levels |
| `knowledge/ROADMAP.md` | Phase 2 Rule Database |

---

# 10. Conclusion

This module is the Knowledge Base JSON source for Strength Rules. It mirrors all supported Strength Engine V2 scenarios and serves as the canonical reference for authoring, validation, and AI generation.
