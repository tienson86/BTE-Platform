# Combination Engine Rule Mapping

**Module:** `engines/analysis_engine/06_combination_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Mapping Specification)

---

# 1. Purpose

This document maps Combination Engine analytical concerns to Knowledge Asset categories accessed through Knowledge SDK.

---

# 2. Mapping Principle

```text
Engine concern  →  Knowledge Asset family  →  SDK access  →  Evidence in CombinationResult
```

No hard-coded repository paths are part of this contract.

Logical module identity:

```text
combination_knowledge
```

---

# 3. Concern → Asset Mapping

| Engine Concern | Primary Knowledge Assets |
|----------------|--------------------------|
| Heavenly Stem Combination | Rules, Mapping Tables, Terminology |
| Earthly Branch Combination | Rules, Mapping Tables, Terminology |
| Clash | Rules, Decision Tables, Mapping Tables |
| Harm | Rules, Decision Tables, Mapping Tables |
| Punishment | Rules, Decision Tables, Mapping Tables |
| Destruction | Rules, Decision Tables, Mapping Tables |
| Hidden Combination | Rules, Mapping Tables, Reference Tables |
| Transformation | Rules, Decision Tables, Formula Library |
| Priority Resolution | Priority Tables, Rules |
| Conflict Resolution | Priority Tables, Rules, Decision Tables |
| Formula Concepts | Formula Library |
| Confidence | Formula Library, Rules |

---

# 4. Upstream Evidence Mapping

| Upstream Result | Engine Usage |
|-----------------|--------------|
| StrengthResult | Optional qualifying evidence where knowledge declares |
| TemperatureResult | Optional qualifying evidence where knowledge declares |
| PatternResult | Optional qualifying evidence where knowledge declares |
| UsefulGodResult | Optional qualifying evidence where knowledge declares |
| TenGodsResult | Optional qualifying evidence where knowledge declares |

Upstream fields are evidence, not knowledge ownership.

---

# 5. Output Evidence Mapping

Matched assets must project into CombinationResult as:

- KnowledgeReferences
- RuleEvidence / explanation slots
- rejected-alternative records where applicable

---

# 6. Non-Mapping Rules

The engine must not:

- map concerns to upstream analytical Knowledge Modules for recomputation
- map narrative sentence libraries as Combination analytical rules
- map report templates as analytical assets

---

# 7. Acceptance Criteria

Rule Mapping is accepted when concern-to-asset coverage, upstream evidence mapping, and non-mapping rules are complete.
