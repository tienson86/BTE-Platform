# Strength Knowledge Assets

**Module:** Strength Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Inventory)

---

# 1. Purpose

This document defines the complete Knowledge Asset inventory required by Strength Knowledge.

---

# 2. Declared Asset Families

| Asset Type | Role |
|------------|------|
| Rule Asset | Strength decision rules |
| Decision Table | Compact conditional strength outcomes |
| Mapping Table | Factor/category mappings |
| Formula Library | Declarative weight and confidence models |
| Priority Table | Conflict and priority ordering |
| Terminology | Strength domain vocabulary |
| Reference Table | Shared lookup references for strength factors |
| Metadata | Module and asset metadata |
| Manifest | Published inventory |
| Example Asset | Illustrative strength cases |
| Validation Dataset | Integrity and consistency checks |
| Golden Dataset | Deterministic expected knowledge outcomes |
| Documentation | Module documentation set |
| Version Information | SemVer and compatibility matrix |
| Configuration | Optional evaluation profiles |

---

# 3. Asset Coverage by Domain Concern

| Concern | Primary Assets |
|---------|----------------|
| Seasonal Strength | Rules, Decision Tables, Mappings, Weights |
| Monthly Branch Influence | Rules, Mappings |
| Heavenly Stem Support | Rules, Mappings |
| Hidden Stem Support | Rules, Mappings |
| Root Strength / Tong Gen | Rules, Decision Tables, Terminology |
| Five Element Support / Restriction | Rules, Mappings, Formula Library |
| Combination / Clash / Harm / Punishment / Void Influence | Rules, Mappings, Priority Tables |
| Temperature Adjustment Influence | Rules, Mappings, Formula Library |
| Growth Stage | Mappings, Rules, Terminology |
| De Ling / De Di / De Shi | Rules, Decision Tables, Terminology |
| Special Exceptions | Rules, Priority Tables |
| Confidence Models | Formula Library, Rules |
| Weight Models | Formula Library, Reference Tables |

---

# 4. Dependency on Fundamental Knowledge

Strength Knowledge references, and does not redefine:

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Chang Sheng stage identities
- shared relationship taxonomies where fundamental

---

# 5. Consumption

Strength Engine consumes declared assets through abstract interfaces only.

---

# 6. Completeness Rule

All declared families required for V1.0 strength evaluation shall be complete before Published status.
