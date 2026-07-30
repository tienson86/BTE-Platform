# ShenSha Engine Rule Mapping

**Module:** `engines/analysis_engine/07_shensha_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Mapping Specification)

---

# 1. Purpose

This document maps ShenSha Engine analytical concerns to Knowledge Asset categories accessed through Knowledge SDK.

---

# 2. Mapping Principle

```text
Engine concern  →  Knowledge Asset family  →  SDK access  →  Evidence in ShenShaResult
```

No hard-coded repository paths are part of this contract.

Logical module identity:

```text
shensha_knowledge
```

---

# 3. Concern → Asset Mapping

| Engine Concern | Primary Knowledge Assets |
|----------------|--------------------------|
| Auspicious ShenSha | Rules, Lookup Tables, Terminology |
| Inauspicious ShenSha | Rules, Lookup Tables, Terminology |
| Calculation References | Reference Tables, Rules |
| Lookup Tables | Lookup Tables |
| Mapping Tables | Mapping Tables |
| Priority Concepts | Priority Tables, Rules |
| Interaction Rules | Rules, Decision Tables |
| Compatibility | Rules, Mapping Tables, Decision Tables |
| Exceptions | Rules, Decision Tables |
| Confidence Concepts | Formula Library, Rules |

---

# 4. Upstream Evidence Mapping

| Upstream Result | Engine Usage |
|-----------------|--------------|
| StrengthResult | Optional qualifying evidence where knowledge declares |
| TemperatureResult | Optional qualifying evidence where knowledge declares |
| PatternResult | Optional qualifying evidence where knowledge declares |
| UsefulGodResult | Optional qualifying evidence where knowledge declares |
| TenGodsResult | Optional qualifying evidence where knowledge declares |
| CombinationResult | Optional qualifying evidence where knowledge declares |

Upstream fields are evidence, not knowledge ownership.

---

# 5. Output Evidence Mapping

Matched assets must project into ShenShaResult as:

- KnowledgeReferences
- RuleEvidence / explanation slots
- rejected-alternative records where applicable

---

# 6. Non-Mapping Rules

The engine must not:

- map concerns to upstream analytical Knowledge Modules for recomputation
- map narrative sentence libraries as ShenSha analytical rules
- map report templates as analytical assets

---

# 7. Acceptance Criteria

Rule Mapping is accepted when concern-to-asset coverage, upstream evidence mapping, and non-mapping rules are complete.
