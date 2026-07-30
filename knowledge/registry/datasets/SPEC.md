# Datasets Registry Specification

**Document:** SPEC  
**Registry:** `datasets`  
**Version:** V1.0.0  
**Status:** Official  

---

## 1. Purpose

Define the global registry contract for **Datasets Registry**.

---

## 2. Authority Model

| Layer | Role |
|-------|------|
| Source module (`knowledge/golden_dataset/`) | Authoritative record |
| Global registry (this module) | Locator / catalog index |
| Governance registry | Frozen policy/control plane |

Conflict rule: source module wins over global INDEX until reconciled.

---

## 3. Identity

Primary identity: **CASE-NNNNNN**

IDs SHALL be unique within this registry catalog.

---

## 4. Required Entry Fields

- Dataset ID
- Title
- Domain
- Category
- Status
- Version
- Path
- Notes

---

## 5. Lifecycle

`Placeholder / Draft → Review → Official → Deprecated`

Global registry rows SHOULD mirror source-module Status.

---

## 6. Prohibitions

- No fabricated entries
- No edits to frozen source modules from this registry
- No edits to `knowledge/governance/registry/`

---

## 7. Acceptance (Framework V1.0.0)

- [ ] README / INDEX / TEMPLATE / SPEC exist
- [ ] INDEX contains no real entries
- [ ] Frozen modules untouched
