# Luck Engine Rule Mapping

**Module:** `engines/analysis_engine/08_luck_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Mapping Specification)

---

# 1. Purpose

This document maps Luck Engine analytical concerns to Knowledge Asset categories accessed through Knowledge SDK.

---

# 2. Mapping Principle

```text
Engine concern  →  Knowledge Asset family  →  SDK access  →  Evidence in LuckResult
```

No hard-coded repository paths are part of this contract.

Logical module identity:

```text
luck_knowledge
```

---

# 3. Concern → Asset Mapping

| Engine Concern | Primary Knowledge Assets |
|----------------|--------------------------|
| Da Yun | Rules, Reference Tables, Terminology |
| Liu Nian | Rules, Reference Tables, Terminology |
| Liu Yue | Rules, Reference Tables, Terminology |
| Liu Ri | Rules, Reference Tables, Terminology |
| Liu Shi | Rules, Reference Tables, Terminology |
| Luck Interaction | Rules, Decision Tables, Mapping Tables |
| Timing Principles | Rules, Formula Library, Reference Tables |
| Activation Rules | Rules, Decision Tables |
| Favorability Concepts | Rules, Decision Tables, Terminology |
| Priority Concepts | Priority Tables, Rules |
| Confidence Concepts | Formula Library, Rules |

---

# 4. Upstream Evidence Mapping

| Upstream Result | Engine Usage |
|-----------------|--------------|
| StrengthResult | Luck–natal interaction evidence |
| TemperatureResult | Luck–natal interaction evidence |
| PatternResult | Luck–natal interaction evidence |
| UsefulGodResult | Luck–natal interaction evidence |
| TenGodsResult | Luck–natal interaction evidence |
| CombinationResult | Luck–natal interaction evidence |
| ShenShaResult | Luck–natal interaction evidence |

Upstream fields are evidence, not knowledge ownership.

---

# 5. Output Evidence Mapping

Matched assets must project into LuckResult as:

- KnowledgeReferences
- RuleEvidence / explanation slots
- rejected-alternative records where applicable

---

# 6. Non-Mapping Rules

The engine must not:

- map concerns to upstream analytical Knowledge Modules for recomputation
- map narrative sentence libraries as Luck analytical rules
- map report templates as analytical assets

---

# 7. Acceptance Criteria

Rule Mapping is accepted when concern-to-asset coverage, upstream evidence mapping, and non-mapping rules are complete.
