# Pattern Engine Rule Mapping

**Module:** `engines/analysis_engine/03_pattern_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Integration Specification)

---

# 1. Purpose

This document defines how the Pattern Engine consumes the Rule Database.

The engine never embeds business rules in source code.

---

# 2. Rule Source

All rules originate from:

```text
knowledge/rule_database/03_pattern_rules/
```

No alternative source is permitted.

---

# 3. Rule Categories

The Pattern Engine consumes the following categories:

- Structure Rules
- Standard Pattern Rules
- Special Pattern Rules
- Candidate Resolution Rules
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

PatternResult
```

---

# 5. Rule Matching

Each analyzer is responsible only for its own rule category.

Example:

Structure Analyzer

↓

Structure Rules

Standard Pattern Analyzer

↓

Standard Pattern Rules

Special Pattern Analyzer

↓

Special Pattern Rules

Candidate Resolver

↓

Candidate Resolution Rules

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
- use Strength or Temperature Rules as Pattern Rules
- embed pattern business knowledge in source code

Rule governance belongs to the Rule Database.
