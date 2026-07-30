# Temperature Knowledge Assets

**Module:** Temperature Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Inventory)

---

# 1. Purpose

This document defines the complete Knowledge Asset inventory required by Temperature Knowledge.

---

# 2. Declared Asset Families

| Asset Type | Role |
|------------|------|
| Rule Asset | Temperature / climate decision rules |
| Decision Table | Compact conditional climate outcomes |
| Mapping Table | Factor/category mappings |
| Formula Library | Declarative weight and confidence models |
| Priority Table | Conflict and priority ordering |
| Terminology | Climate domain vocabulary |
| Reference Table | Shared lookup references for climate factors |
| Metadata | Module and asset metadata |
| Manifest | Published inventory |
| Example Asset | Illustrative climate cases |
| Validation Dataset | Integrity and consistency checks |
| Golden Dataset | Deterministic expected knowledge outcomes |
| Documentation | Module documentation set |
| Version Information | SemVer and compatibility matrix |
| Configuration | Optional evaluation profiles |

---

# 3. Asset Coverage by Domain Concern

| Concern | Primary Assets |
|---------|----------------|
| Seasonal Temperature | Rules, Decision Tables, Mappings, Weights |
| Climate Categories | Rules, Mappings, Terminology |
| Cold / Hot Classification | Rules, Decision Tables, Terminology |
| Warm / Cool Adjustment | Rules, Formula Library, Adjustment Principles |
| Dryness / Humidity | Rules, Mappings, Terminology |
| Seasonal Energy | Rules, Mappings, Reference Tables |
| Month Climate Characteristics | Mapping Tables, Reference Tables, Rules |
| Climate Balance | Rules, Decision Tables, Formula Library |
| Temperature Exceptions | Rules, Priority Tables |
| Adjustment Principles | Rules, Decision Tables, Formula Library |
| Confidence Models | Formula Library, Rules |
| Weight Models | Formula Library, Reference Tables |
| Priority Concepts | Priority Tables, Rules |

---

# 4. Dependency on Fundamental Knowledge

Temperature Knowledge references, and does not redefine:

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Season Definitions
- Climate Definitions
- shared relationship taxonomies where fundamental

---

# 5. Consumption

Temperature Engine consumes declared assets through abstract interfaces only.

---

# 6. Completeness Rule

All declared families required for V1.0 temperature evaluation shall be complete before Published status.
