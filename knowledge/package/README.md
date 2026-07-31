# BTE Knowledge Package — Specification

**Sprint:** 4D  
**Location:** `knowledge/package/`  
**Status:** Specification only (no package manager runtime)

---

## Purpose

Define Pack / Module packaging: schemas, registries, layout hierarchy, and package lifecycle — including Section, Knowledge Record, Release, Version, and Compatibility.

---

## Folder tree

```text
knowledge/package/
├── README.md
├── pack.schema.json
├── module.schema.json
├── pack_registry.json
├── module_registry.json
├── package_layout.json
├── package_lifecycle.json
└── examples/
    ├── pack_01_example.json
    └── module_01_example.json
```

---

## Core units

| Unit | Meaning |
|------|---------|
| **Module** | Domain folder (`01_fundamental_knowledge`) owning packs |
| **Pack** | Design/publication bundle (`PACK_01`) of related KRs |
| **Section** | Logical group inside a Pack (`SEC-*`) |
| **Knowledge Record** | Atomic academic unit (`KR-*`) |
| **Release** | Publication status/event on Pack or Module |
| **Version** | SemVer on Pack, Module, and KR |
| **Compatibility** | Version ranges + breaking-change declarations |

Hierarchy: **Module → Pack → Section → Knowledge Record**.

---

## Schemas & registries

| File | Role |
|------|------|
| `pack.schema.json` | Draft 2020-12 Pack descriptor |
| `module.schema.json` | Draft 2020-12 Module descriptor |
| `pack_registry.json` | Pack inventory (PACK_01…07 seeded) |
| `module_registry.json` | Module inventory |
| `package_layout.json` | Containment + directory conventions |
| `package_lifecycle.json` | planned → … → released → retired |

---

## Related

- `knowledge/index/pack_index.json` — lookup index (complementary)
- `knowledge/dependency/` — inter-pack/record dependency levels
- `knowledge/governance/` — KR-level freeze/release gates

---

## Out of scope

- Packaging CLI / installer
- Automatic registry generation from disk
- Mutation of `knowledge/bazi/**`
