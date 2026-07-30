# Ten Gods Engine Rule Mapping

**Module:** `engines/analysis_engine/05_ten_gods_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Mapping Specification)

---

# 1. Purpose

This document maps Ten Gods Engine analytical concerns to Knowledge Asset categories accessed through Knowledge SDK.

---

# 2. Mapping Principle

```text
Engine concern  →  Knowledge Asset family  →  SDK access  →  Evidence in TenGodsResult
```

No hard-coded repository paths are part of this contract.

Logical module identity:

```text
ten_gods_knowledge
```

---

# 3. Concern → Asset Mapping

| Engine Concern | Primary Knowledge Assets |
|----------------|--------------------------|
| Ten Gods Definitions / Presence | Rules, Terminology, Reference Tables, Mapping Tables |
| Relationship Models | Rules, Decision Tables, Mapping Tables |
| Strength Interaction | Rules, Mapping Tables, Reference Tables |
| Temperature Interaction | Rules, Mapping Tables, Reference Tables |
| Pattern Interaction | Rules, Mapping Tables, Reference Tables |
| Useful God Interaction | Rules, Mapping Tables, Reference Tables |
| Favorability | Rules, Decision Tables, Terminology |
| Personality Concepts | Rules, Decision Tables, Terminology |
| Career Concepts | Rules, Decision Tables, Terminology |
| Wealth Concepts | Rules, Decision Tables, Terminology |
| Marriage Concepts | Rules, Decision Tables, Terminology |
| Health Concepts | Rules, Decision Tables, Terminology |
| Priority Concepts | Priority Tables, Rules |
| Confidence Concepts | Formula Library, Rules |

---

# 4. Upstream Evidence Mapping

| Upstream Result Field Family | Engine Usage |
|------------------------------|--------------|
| StrengthResult classifications | Strength Interaction inputs |
| TemperatureResult classifications | Temperature Interaction inputs |
| PatternResult identities | Pattern Interaction inputs |
| UsefulGodResult roles | Useful God Interaction inputs |

Upstream fields are evidence, not knowledge ownership.

---

# 5. Output Evidence Mapping

Matched assets must project into TenGodsResult as:

- KnowledgeReferences
- RuleEvidence / explanation slots
- rejected-alternative records where applicable

---

# 6. Non-Mapping Rules

The engine must not:

- map concerns to Strength/Temperature/Pattern/Useful God Knowledge for recomputation
- map narrative sentence libraries as Ten Gods analytical rules
- map report templates as analytical assets

---

# 7. Acceptance Criteria

Rule Mapping is accepted when concern-to-asset coverage, upstream evidence mapping, and non-mapping rules are complete.
