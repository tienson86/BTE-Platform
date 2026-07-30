# Knowledge Version Matrix

**Component:** Knowledge Compatibility Matrix  
**Version:** V1.0.0  
**Status:** Frozen (Version Matrix Specification)

---

# 1. Purpose

This document defines the version planes and baseline compatibility matrix structure used to authorize co-selection.

---

# 2. Version Planes

```text
1. Compatibility Matrix Spec Version
2. Knowledge Architecture / KMS / KAS Versions
3. Knowledge Registry Spec Version
4. Knowledge Loader Spec Version
5. Knowledge SDK Spec Version
6. Knowledge Module Versions
7. Knowledge Asset Versions
8. Analysis Engine Version
9. Interpretation Engine Version
10. Report Engine Version
11. Registry Catalog Revision (runtime observation, not SemVer substitute)
```

These planes must not be conflated.

---

# 3. Matrix Entry Schema

Each matrix entry shall include:

| Field | Requirement |
|-------|-------------|
| subject_id | Module / Asset / Registry / Loader / SDK / Engine identity |
| subject_version | Exact version or declared subject range |
| target_id | Compatibility target identity |
| target_version_range | Compatible target range |
| status | Compatible / CompatibleWithMigration / Incompatible / Unknown |
| plane | Compatibility plane label |
| breaking_change_flags | Optional flags |
| notes | Migration or constraint notes |
| declared_by / declared_at | Provenance |

---

# 4. Baseline Control-Plane Matrix (V1.x)

| Subject | Compatible Target | Range | Status |
|---------|-------------------|-------|--------|
| Knowledge Registry | Knowledge Architecture / KMS / KAS | 1.x | Compatible |
| Knowledge Loader | Knowledge Registry | 1.x | Compatible |
| Knowledge SDK | Knowledge Loader | 1.x | Compatible |
| Knowledge SDK | Knowledge Registry | 1.x | Compatible |
| Analysis Engine | Knowledge SDK | 1.x | Compatible |
| Interpretation Engine | Knowledge SDK | 1.x | Compatible |
| Report Engine | Knowledge SDK | 1.x | Compatible |

V1.0 control-plane stack is intended to operate as a Compatible 1.x family unless a MAJOR break is published.

---

# 5. Baseline Knowledge Module Matrix (V1.x)

| Subject Family | Compatible Target | Range | Status |
|----------------|-------------------|-------|--------|
| All analytical Knowledge Modules | Fundamental Knowledge | 1.x | Compatible |
| All Knowledge Modules | KMS / KAS / Architecture | 1.x | Compatible |
| Strength Knowledge | Knowledge SDK consumers (Analysis Strength stage) | 1.x | Compatible |
| Temperature Knowledge | Knowledge SDK consumers (Analysis Temperature stage) | 1.x | Compatible |
| Pattern Knowledge | Knowledge SDK consumers (Analysis Pattern stage) | 1.x | Compatible |
| Useful God Knowledge | Knowledge SDK consumers (Analysis Useful God stage) | 1.x | Compatible |
| Ten Gods Knowledge | Knowledge SDK consumers (Analysis Ten Gods stage) | 1.x | Compatible |
| Combination Knowledge | Knowledge SDK consumers (Analysis Combination stage) | 1.x | Compatible |
| ShenSha Knowledge | Knowledge SDK consumers (Analysis ShenSha stage) | 1.x | Compatible |
| Luck Knowledge | Knowledge SDK consumers (Analysis Luck stage) | 1.x | Compatible |

Evidence-compatible references among analytical modules are Compatible within 1.x when identities remain recognizable; breaking upstream classification identity changes require MAJOR and matrix updates.

---

# 6. Knowledge Asset Matrix Rules

| Subject | Compatible Target | Rule |
|---------|-------------------|------|
| Knowledge Asset@version | Owning Knowledge Module@version | Exact owning module version must be Compatible |
| Knowledge Asset@1.x | KAS 1.x | Required |
| Golden / Validation Dataset | Referenced Assets | Referenced asset versions must be Compatible within declared set |

An asset cannot be production-Compatible with a Retired owning module version.

---

# 7. Engine-to-Knowledge Matrix

| Engine | Must declare Compatible ranges for |
|--------|-------------------------------------|
| Analysis Engine | Knowledge SDK; stage Knowledge Modules used |
| Interpretation Engine | Knowledge SDK; Interpretation / Sentence Knowledge Modules |
| Report Engine | Knowledge SDK; Report Template Knowledge Modules |

Engines that bypass SDK are Incompatible with this matrix architecture by definition.

---

# 8. Runtime Co-Selection Snapshot

For one request, the effective matrix slice includes:

- SDK + Loader + Registry versions in use
- resolved Knowledge Module versions
- resolved Knowledge Asset versions
- consuming Engine version

All required pairs in that slice must be Compatible or CompatibleWithMigration.

---

# 9. Acceptance Criteria

Version Matrix is accepted when planes, entry schema, baseline V1.x control-plane/module rules, and asset/engine matrix requirements are complete.
