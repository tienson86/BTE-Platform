# Pattern Engine Rule Mapping

**Module:** `engines/analysis_engine/03_pattern_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Integration Specification)

---

# 1. Purpose

This document defines how the Pattern Engine consumes the Rule Database.

The engine never embeds business rules in source code.

Business pattern knowledge remains exclusively in the Pattern Rule Database.

---

# 2. Rule Source

All rules originate from:

```text
knowledge/rule_database/04_pattern_rules/
```

No alternative source is permitted.

The engine documentation shall not duplicate Pattern Rule content. It defines only the mapping between rule categories and engine components.

---

# 3. Rule Categories

The Pattern Engine consumes the following conceptual categories:

- Standard Patterns
- Special Patterns
- Follow Patterns
- Transformation Patterns
- Mixed Patterns
- Exceptional Patterns
- Conflict Resolution
- Priority Resolution

Supporting operational categories may include:

- Structure Rules
- Day Master Relation Rules
- Weight Rules

---

# 4. Rule Lifecycle

```text
Rule Database
knowledge/rule_database/04_pattern_rules/

↓

Rule Loader

↓

Rule Registry

↓

Rule Adapter

↓

Analyzer / Candidate Layer

↓

Matched Rule

↓

PatternResult
```

---

# 5. Rule-to-Component Mapping

Each analyzer or resolver is responsible only for its own rule category.

| Engine Component | Rule Category |
|------------------|---------------|
| Structure Analyzer | Structure Rules |
| Day Master Relation Analyzer | Day Master Relation Rules |
| Standard Pattern Analyzer | Standard Pattern Rules |
| Transformation Pattern Analyzer | Transformation Pattern Rules |
| Special Pattern Analyzer | Special Pattern Rules |
| Follow Pattern Analyzer | Follow Pattern Rules |
| Mixed / Exceptional Analyzer | Mixed Pattern Rules / Exceptional Pattern Rules |
| Conflict Resolver | Conflict Resolution Rules |
| Priority Resolver | Priority Resolution Rules |

No analyzer may evaluate another category.

---

# 6. Rule Matching

Matching proceeds by category:

Standard Pattern Analyzer

↓

Standard Pattern Rules

Special Pattern Analyzer

↓

Special Pattern Rules

Follow Pattern Analyzer

↓

Follow Pattern Rules

Transformation Pattern Analyzer

↓

Transformation Pattern Rules

Conflict Resolver

↓

Conflict Resolution Rules

Priority Resolver

↓

Priority Resolution Rules

---

# 7. Rule Versioning

Rules shall include:

- Rule ID
- Version
- Status
- Category
- Priority
- Effective Date

The engine shall reject unsupported rule versions.

---

# 8. Traceability

Every matched rule shall be recorded with:

- Rule ID
- Rule Version
- Analyzer or Resolver
- Score Contribution
- Evidence

Rejected candidates shall reference the conflict or priority rules that excluded them.

---

# 9. Rule Constraints

The engine shall never:

- modify rules
- reorder rule priority outside Priority Resolution Rules
- generate new rules
- ignore mandatory rules
- use Strength or Temperature Rules as Pattern Rules
- embed pattern business knowledge in source code
- duplicate Pattern Rule definitions inside documentation

Rule governance belongs to the Rule Database.

---

# 10. Extensibility

Additional pattern categories may be introduced in the Rule Database without changing the Pattern Engine public API within Version 1.x.

New categories require corresponding analyzer or resolver mapping updates only when necessary for execution.
