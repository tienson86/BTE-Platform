# Pattern Knowledge Assets

**Module:** Pattern Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Inventory)

---

# 1. Purpose

This document defines the complete Knowledge Asset inventory required by Pattern Knowledge.

---

# 2. Declared Asset Families

| Asset Type | Role |
|------------|------|
| Rule Asset | Pattern decision rules |
| Decision Table | Compact pattern determination outcomes |
| Mapping Table | Pattern/category/condition mappings |
| Formula Library | Declarative confidence and ranking models |
| Priority Table | Conflict and priority ordering |
| Terminology | Pattern domain vocabulary |
| Reference Table | Shared pattern reference lookups |
| Metadata | Module and asset metadata |
| Manifest | Published inventory |
| Example Asset | Illustrative pattern cases |
| Validation Dataset | Integrity and consistency checks |
| Golden Dataset | Deterministic expected knowledge outcomes |
| Documentation | Module documentation set |
| Version Information | SemVer and compatibility matrix |
| Configuration | Optional evaluation profiles |

---

# 3. Asset Coverage by Domain Concern

| Concern | Primary Assets |
|---------|----------------|
| Standard Patterns | Rules, Decision Tables, Mappings, Terminology |
| Special Patterns | Rules, Decision Tables, Priority Tables |
| Follow Patterns | Rules, Mappings, Terminology |
| Transformation Patterns | Rules, Decision Tables, Mappings |
| Pattern Conditions | Rules, Mapping Tables, Reference Tables |
| Pattern Priority | Priority Tables, Rules |
| Pattern Compatibility | Mapping Tables, Reference Tables, Rules |
| Pattern Exceptions | Rules, Priority Tables |
| Pattern Confidence | Formula Library, Rules |
| Decision Concepts | Decision Tables, Rules |
| Formula Concepts | Formula Library |
| Validation Concepts | Validation Datasets, Golden Datasets |

---

# 4. Dependency on Fundamental Knowledge

Pattern Knowledge references, and does not redefine:

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Ten Gods relationship identities
- shared relationship taxonomies where fundamental

---

# 5. Consumption

Pattern Engine consumes declared assets through abstract interfaces only.

---

# 6. Completeness Rule

All declared families required for V1.0 pattern evaluation shall be complete before Published status.
