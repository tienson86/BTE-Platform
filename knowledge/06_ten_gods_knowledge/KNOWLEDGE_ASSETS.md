# Ten Gods Knowledge Assets

**Module:** Ten Gods Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Inventory)

---

# 1. Purpose

This document defines the complete Knowledge Asset inventory required by Ten Gods Knowledge.

---

# 2. Declared Asset Families

| Asset Type | Role |
|------------|------|
| Rule Asset | Ten Gods quality, interaction, and priority rules |
| Decision Table | Compact Ten Gods determination outcomes |
| Mapping Table | Identity / favorability / life-area mappings |
| Formula Library | Declarative confidence and interaction models |
| Priority Table | Conflict and priority ordering |
| Terminology | Ten Gods domain vocabulary |
| Reference Table | Shared Ten Gods reference lookups |
| Metadata | Module and asset metadata |
| Manifest | Published inventory |
| Example Asset | Illustrative Ten Gods cases |
| Validation Dataset | Integrity and consistency checks |
| Golden Dataset | Deterministic expected knowledge outcomes |
| Documentation | Module documentation set |
| Version Information | SemVer and compatibility matrix |
| Configuration | Optional evaluation profiles |

---

# 3. Asset Coverage by Domain Concern

| Concern | Primary Assets |
|---------|----------------|
| Ten Gods Definitions | Rules, Terminology, Reference Tables |
| Relationship Models | Rules, Mapping Tables, Decision Tables |
| Strength Interaction | Rules, Mapping Tables, Reference Tables |
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

# 4. Dependency on Fundamental Knowledge

Ten Gods Knowledge references, and does not redefine:

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Ten Gods relationship identities
- Season / Climate definition frames where fundamental

---

# 5. Upstream Analytical Dependencies

Ten Gods Knowledge may declare interaction concepts on published:

- Strength classifications
- Pattern identities
- Useful God role assignments

These are evidence dependencies, not ownership of those domains.

TemperatureResult may appear in AnalysisContext for pipeline continuity but is not a primary V1.0 Ten Gods Knowledge ownership dependency.

---

# 6. Consumption

Ten Gods Engine consumes declared assets through abstract interfaces only.

---

# 7. Completeness Rule

All declared families required for V1.0 Ten Gods evaluation shall be complete before Published status.
