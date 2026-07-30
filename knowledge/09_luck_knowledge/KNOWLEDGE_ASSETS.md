# Luck Knowledge Assets

**Module:** Luck Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Inventory)

---

# 1. Purpose

This document defines the complete Knowledge Asset inventory required by Luck Knowledge.

---

# 2. Declared Asset Families

| Asset Type | Role |
|------------|------|
| Rule Asset | Luck timing, activation, interaction, and priority rules |
| Decision Table | Compact Luck determination outcomes |
| Mapping Table | Layer / timing / favorability mappings |
| Formula Library | Declarative confidence and timing models |
| Priority Table | Conflict and priority ordering |
| Terminology | Luck domain vocabulary |
| Reference Table | Shared Luck reference lookups |
| Metadata | Module and asset metadata |
| Manifest | Published inventory |
| Example Asset | Illustrative Luck cases |
| Validation Dataset | Integrity and consistency checks |
| Golden Dataset | Deterministic expected knowledge outcomes |
| Documentation | Module documentation set |
| Version Information | SemVer and compatibility matrix |
| Configuration | Optional evaluation profiles |

---

# 3. Asset Coverage by Domain Concern

| Concern | Primary Assets |
|---------|----------------|
| Da Yun | Rules, Reference Tables, Terminology |
| Liu Nian | Rules, Reference Tables, Terminology |
| Liu Yue | Rules, Reference Tables, Terminology |
| Liu Ri | Rules, Reference Tables, Terminology |
| Liu Shi | Rules, Reference Tables, Terminology |
| Luck Interaction | Rules, Decision Tables, Mapping Tables |
| Timing Principles | Rules, Formula Library, Reference Tables |
| Activation Rules | Rules, Decision Tables |
| Favorability Concepts | Rules, Decision Tables, Terminology |
| Confidence Models | Formula Library, Rules |
| Priority Concepts | Priority Tables, Rules |
| Reference Tables | Reference Tables |

---

# 4. Dependency on Fundamental Knowledge

Luck Knowledge references, and does not redefine:

- Yin Yang
- Wu Xing
- Heavenly Stems
- Earthly Branches
- Hidden Stems
- Season / Climate definition frames where fundamental
- Sexagenary cycle identities where fundamental

---

# 5. Upstream Analytical Dependencies

Luck Knowledge may declare interaction concepts on published natal:

- Strength classifications
- Temperature / climate classifications
- Pattern identities
- Useful God roles
- Ten Gods classifications
- Combination outcomes
- ShenSha identities

These are evidence dependencies, not ownership of those domains.

---

# 6. Consumption

Luck Engine consumes declared assets through abstract interfaces only.

---

# 7. Completeness Rule

All declared families required for V1.0 Luck evaluation shall be complete before Published status.
