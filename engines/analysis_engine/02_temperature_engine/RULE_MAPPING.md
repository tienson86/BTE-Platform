# Temperature Engine Rule Mapping

**Module:** `engines/analysis_engine/02_temperature_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Integration Specification)

---

# 1. Purpose

This document defines how the Temperature Engine consumes the Rule Database.

The engine never embeds business rules in source code.

---

# 2. Rule Source

All rules originate from:

```text
knowledge/rule_database/02_temperature_rules/
```

No alternative source is permitted.

---

# 3. Rule Categories

The Temperature Engine consumes the following categories:

- Seasonal Temperature Rules
- Warm / Cold Rules
- Dryness Rules
- Humidity Rules
- Equilibrium Rules
- Environmental Support Rules
- Adjustment Rules
- Weight Rules
- Priority Rules (if applicable)

---

# 4. Rule Lifecycle

```text
Rule Database

↓

Rule Loader

↓

Rule Registry

↓

Rule Adapter

↓

Analyzer

↓

Matched Rule

↓

TemperatureResult
```

---

# 5. Rule Matching

Each analyzer is responsible only for its own rule category.

Example:

Season Temperature Analyzer

↓

Seasonal Temperature Rules

Warm Cold Analyzer

↓

Warm / Cold Rules

Dryness Analyzer

↓

Dryness Rules

Humidity Analyzer

↓

Humidity Rules

Equilibrium Analyzer

↓

Equilibrium Rules

Environmental Support Analyzer

↓

Environmental Support Rules

Adjustment Analyzer

↓

Adjustment Rules

No analyzer may evaluate another category.

---

# 6. Rule Versioning

Rules shall include:

- Rule ID
- Version
- Status
- Priority
- Effective Date

The engine shall reject unsupported rule versions.

---

# 7. Traceability

Every matched rule shall be recorded with:

- Rule ID
- Rule Version
- Analyzer
- Score Contribution
- Evidence

---

# 8. Rule Constraints

The engine shall never:

- modify rules
- reorder rule priority
- generate new rules
- ignore mandatory rules
- use Strength Rules as Temperature Rules
- embed climate business knowledge in source code

Rule governance belongs to the Rule Database.
