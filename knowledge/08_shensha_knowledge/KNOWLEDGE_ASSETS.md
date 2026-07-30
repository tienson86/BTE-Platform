# ShenSha Knowledge Assets

**Module:** ShenSha Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Inventory)

---

# 1. Purpose

This document defines the complete Knowledge Asset inventory required by ShenSha Knowledge.

---

# 2. Declared Asset Families

| Asset Type | Role |
|------------|------|
| Rule Asset | ShenSha detection, interaction, exception, and priority rules |
| Decision Table | Compact ShenSha determination outcomes |
| Mapping Table | Anchor / identity / polarity / interaction mappings |
| Lookup Table | Compact detection lookups by declared keys |
| Formula Library | Declarative confidence and interaction models |
| Priority Table | Conflict and priority ordering |
| Terminology | ShenSha domain vocabulary |
| Reference Table | Shared calculation and identity references |
| Metadata | Module and asset metadata |
| Manifest | Published inventory |
| Example Asset | Illustrative ShenSha cases |
| Validation Dataset | Integrity and consistency checks |
| Golden Dataset | Deterministic expected knowledge outcomes |
| Documentation | Module documentation set |
| Version Information | SemVer and compatibility matrix |
| Configuration | Optional evaluation profiles |

---

# 3. Asset Coverage by Domain Concern

| Concern | Primary Assets |
|---------|----------------|
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

# 4. Dependency on Fundamental Knowledge

ShenSha Knowledge references, and does not redefine:

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Season / Climate definition frames where fundamental

---

# 5. Upstream Analytical Dependencies

ShenSha Knowledge is primarily anchor- and table-oriented.

Where interaction with published analytical classifications is declared, those classifications are evidence dependencies only and are not owned by this module.

---

# 6. Consumption

ShenSha Engine consumes declared assets through abstract interfaces only.

---

# 7. Completeness Rule

All declared families required for V1.0 ShenSha evaluation shall be complete before Published status.
