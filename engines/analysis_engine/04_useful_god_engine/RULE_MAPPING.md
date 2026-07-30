# Useful God Engine Rule Mapping

**Module:** `engines/analysis_engine/04_useful_god_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Integration Specification)

---

# 1. Purpose

This document defines how the Useful God Engine consumes the Useful God Rule Database Knowledge Module.

The engine never embeds business rules in source code.

Business Useful God knowledge remains exclusively in the Useful God Rule Database.

---

# 2. Knowledge Dependency

## Useful God Rule Database

| Field | Value |
|-------|-------|
| Status | Planned |
| Dependency Type | Knowledge Module |
| Availability | Future Analysis Knowledge Package |

Description:

The Useful God Engine depends on a dedicated Useful God Rule Database.

The Rule Database is not yet part of the repository.

The engine architecture is intentionally decoupled from the physical storage location of the rule database.

The actual repository path will be defined when the Useful God Knowledge Module is implemented.

The engine shall depend only on the abstract Knowledge Module.

No hard-coded repository path is part of this contract.

The engine documentation shall not duplicate Useful God Rule content. It defines only the mapping between rule categories and engine components.

---

# 3. Rule Categories

The Useful God Engine consumes the following conceptual categories:

- Yong Shen
- Xi Shen
- Ji Shen
- Xian Shen
- Primary Candidate
- Secondary Candidate
- Alternative Candidate
- Candidate Priority
- Conflict Resolution
- Confidence Evaluation

Supporting operational categories may include:

- Strength Balance Rules
- Climate Balance Rules
- Pattern Requirement Rules
- Equilibrium Rules
- Relation Rules
- Adjustment Priority Rules
- Weight Rules

---

# 4. Rule Lifecycle

```text
Useful God Rule Database
(Knowledge Module — Planned)

↓

Rule Loader

↓

Rule Registry

↓

Rule Adapter

↓

Analyzer / Candidate / Determination Layer

↓

Matched Rule

↓

UsefulGodResult
```

---

# 5. Rule-to-Component Mapping

Each analyzer, resolver, or determiner is responsible only for its own rule category.

| Engine Component | Rule Category |
|------------------|---------------|
| Strength Balance Analyzer | Strength Balance Rules |
| Climate Balance Analyzer | Climate Balance Rules |
| Pattern Requirement Analyzer | Pattern Requirement Rules |
| Equilibrium Analyzer | Equilibrium Rules |
| Relation Analyzer | Relation Rules |
| Adjustment Priority Analyzer | Adjustment Priority Rules |
| Candidate Generator | Primary / Secondary / Alternative Candidate Rules |
| Candidate Evaluator | Candidate Evaluation Rules |
| Conflict Resolver | Conflict Resolution Rules |
| Priority Resolver | Candidate Priority Rules |
| Yong Shen Determiner | Yong Shen Rules |
| Xi Shen Determiner | Xi Shen Rules |
| Ji Shen Determiner | Ji Shen Rules |
| Xian Shen Determiner | Xian Shen Rules |
| Confidence Evaluator | Confidence Evaluation Rules |

No component may evaluate another category.

---

# 6. Rule Matching

Matching proceeds by category:

Yong Shen Determiner

↓

Yong Shen Rules

Xi Shen Determiner

↓

Xi Shen Rules

Ji Shen Determiner

↓

Ji Shen Rules

Xian Shen Determiner

↓

Xian Shen Rules

Conflict Resolver

↓

Conflict Resolution Rules

Priority Resolver

↓

Candidate Priority Rules

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
- Analyzer, Resolver, or Determiner
- Score Contribution
- Evidence

Rejected candidates shall reference the conflict or priority rules that excluded them.

---

# 9. Rule Constraints

The engine shall never:

- modify rules
- reorder rule priority outside Candidate Priority and Conflict Resolution Rules
- generate new rules
- ignore mandatory rules
- use Strength, Temperature, or Pattern Rules as Useful God Rules
- embed Useful God business knowledge in source code
- duplicate Useful God Rule definitions inside documentation
- hard-code a physical repository path to the Rule Database

Rule governance belongs to the Useful God Rule Database Knowledge Module.

---

# 10. Extensibility

Additional Useful God categories may be introduced in the Useful God Rule Database Knowledge Module without changing the Useful God Engine public API within Version 1.x.

New categories require corresponding component mapping updates only when necessary for execution.
