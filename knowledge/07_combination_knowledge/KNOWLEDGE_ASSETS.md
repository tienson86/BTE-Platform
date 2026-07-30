# Combination Knowledge Assets

**Module:** Combination Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Inventory)

---

# 1. Purpose

This document defines the complete Knowledge Asset inventory required by Combination Knowledge.

---

# 2. Declared Asset Families

| Asset Type | Role |
|------------|------|
| Rule Asset | Combination, clash, harm, punishment, destruction, transformation rules |
| Decision Table | Compact Combination determination outcomes |
| Mapping Table | Pair / triad / transformation / priority mappings |
| Formula Library | Declarative transformation and confidence models |
| Priority Table | Priority and conflict ordering |
| Terminology | Combination domain vocabulary |
| Reference Table | Shared Combination reference lookups |
| Metadata | Module and asset metadata |
| Manifest | Published inventory |
| Example Asset | Illustrative Combination cases |
| Validation Dataset | Integrity and consistency checks |
| Golden Dataset | Deterministic expected knowledge outcomes |
| Documentation | Module documentation set |
| Version Information | SemVer and compatibility matrix |
| Configuration | Optional evaluation profiles |

---

# 3. Asset Coverage by Domain Concern

| Concern | Primary Assets |
|---------|----------------|
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
| Mapping Tables | Mapping Tables |

---

# 4. Dependency on Fundamental Knowledge

Combination Knowledge references, and does not redefine:

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Season / Climate definition frames where fundamental

---

# 5. Upstream Analytical Dependencies

Combination Knowledge is primarily structure-oriented.

Where interaction with published analytical classifications is declared, those classifications are evidence dependencies only and are not owned by this module.

---

# 6. Consumption

Combination Engine consumes declared assets through abstract interfaces only.

---

# 7. Completeness Rule

All declared families required for V1.0 Combination evaluation shall be complete before Published status.
