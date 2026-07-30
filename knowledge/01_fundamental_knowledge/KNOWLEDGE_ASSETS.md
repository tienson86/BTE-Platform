# Fundamental Knowledge Assets

**Module:** Fundamental Knowledge  
**Version:** V1.0.0  
**Status:** Frozen (Knowledge Asset Inventory)

---

# 1. Purpose

This document defines the Knowledge Asset inventory of Fundamental Knowledge in accordance with KAS.

---

# 2. Declared Asset Families

| Asset Type | Status in this Module |
|------------|------------------------|
| Terminology | Declared |
| Mapping Table | Declared |
| Reference Table | Declared |
| Formula Library | Declared (structural only) |
| Metadata | Declared |
| Manifest | Declared |
| Example Asset | Declared |
| Validation Dataset | Declared |
| Golden Dataset | Declared |
| Documentation | Declared |
| Configuration | Optional |
| Priority Table | Not declared |
| Decision Table | Not declared |
| Rule Asset / Rule Database | Explicitly excluded |

---

# 3. Asset Groups

## 3.1 Identity Catalogs

- Heavenly Stem catalog
- Earthly Branch catalog
- Element catalog
- Polarity catalog
- Chang Sheng stage catalog
- Na Yin catalog

## 3.2 Composition Tables

- Hidden Stem composition mappings

## 3.3 Relationship Matrices

- Five Element relationships
- Stem relationships
- Branch relationships
- Ten Gods relationships

## 3.4 Definition Frames

- Season definitions
- Climate definitions

## 3.5 Language Assets

- Shared terminology

## 3.6 Assurance Assets

- Examples
- Validation Datasets
- Golden Datasets

---

# 4. Rule Asset Exclusion

Fundamental Knowledge does not publish analytical Rule Assets.

Any future attempt to place Strength, Temperature, Pattern, Useful God, or other business rules into this module violates module scope.

---

# 5. Consumption

Downstream modules and engines consume these assets by logical identity and version through abstract interfaces only.

---

# 6. Completeness Rule

All declared asset families must be complete before Published status.

Excluded families must remain excluded unless a MAJOR version explicitly expands scope.
