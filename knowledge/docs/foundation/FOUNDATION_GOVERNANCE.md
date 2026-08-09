# Foundation Governance

| Field | Value |
|-------|-------|
| **Document** | FOUNDATION_GOVERNANCE |
| **Foundation version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## 1. Purpose

This document defines who may change what after Foundation Freeze v1.0.

Governance principle:

```
Stability > Features
Consistency > Shortcuts
Long-term maintainability > Quick fix
```

---

## 2. What is frozen

The following are Foundation-frozen. In-place edits are prohibited.

| Area | Frozen surface |
|------|----------------|
| Knowledge Database V2 | Envelope schema `2.0.0`, identity rules, checksum two-pass |
| Taxonomy & Ontology | Domain ids, hierarchy, naming conventions |
| Package Specification (KD-3) | Package types, lifecycle, PVP profiles, immutability |
| Authoring & Validation (KD-4) | Validation stages, release admission |
| Generator v1.0 | Generator identity, templates, quality gates |
| Analysis Engine public orchestration | AX-1 `AnalysisPipeline` 1.0.0; AX-2 `CanonicalPipeline` 2.0.0 |
| Decision Engine public orchestration | AX-3 `CanonicalDecisionPipeline` 1.0.0 |
| Released Knowledge Packages | Bytes + checksums of sealed releases |
| Published contracts | Analysis / Decision / package I/O contracts already published |
| Evidence & Reasoning frameworks | Bundle and chain identity rules |
| Stage registries | Canonical stage ids and dependency order already declared |

UI Foundation V1.0 (`knowledge/ui_reference/foundation/`) remains a separate frozen product surface. This document freezes **platform** Foundation (knowledge + analysis + decision). Both freezes stand.

---

## 3. What may change without a Foundation version bump

Allowed as **additive product work** that does not edit frozen identities:

- New Knowledge Packages (new `package_id`, own SemVer)
- New optional peer declarations on **new** packages only
- New engines in new directories (Luck, Interpretation, Report)
- New tests that assert frozen checksums and contracts
- Additive documentation under new paths
- Bug fixes strictly inside non-Foundation modules that do not alter public Foundation APIs
- Content authoring for unreleased draft packages

These still follow engine, testing, and database workspace rules.

---

## 4. What requires a Foundation version upgrade

A Foundation SemVer bump is required when changing:

| Change | Minimum Foundation bump |
|--------|-------------------------|
| Patch documentation typo in freeze docs after seal | Patch `1.0.x` (governance note only) |
| Additive optional field on a Foundation contract with default | Minor `1.x.0` |
| New canonical pipeline stage inserted into a frozen order | Major `2.0.0` |
| Schema version other than `2.0.0` | Major |
| Rename / remove public pipeline API | Major |
| Change checksum algorithm or two-pass rule | Major |
| Change package_type enum in a breaking way | Major |
| Mutate a released package in place | **Forbidden** — ship a new package version instead |

See `FOUNDATION_CHANGE_POLICY.md`.

---

## 5. What requires governance approval

| Request | Approvers |
|---------|-----------|
| Foundation major upgrade | Architecture Board + Knowledge Board + Release Manager |
| Foundation minor upgrade | Architecture Board + Release Manager |
| Foundation patch (freeze docs only) | Release Manager |
| New engine that consumes Foundation contracts | Architecture Board |
| New Decision / Analysis package in a frozen domain | Knowledge Board |
| Deprecation of a Foundation stage or contract | Architecture Board + Knowledge Board |
| Exception to “extend, do not modify” | Architecture Board (written waiver, time-boxed) |

No silent exceptions. Waivers MUST name the Foundation version they apply to and the expiry.

---

## 6. Execution authority

| Role | Authority |
|------|-----------|
| Architecture Board | Frozen component catalog, pipelines, engines boundaries |
| Knowledge Board | Taxonomy, packages, evidence, reasoning, generator profiles |
| Release Manager | Checksums, PVP-RELEASE seal, freeze date placeholder → actual date |
| Engine owners | Implementation **inside** their engine without changing Foundation public contracts |

Canonical pipelines remain the only supported execution models for Analysis Knowledge stages (AX-2) and Decision Packages (AX-3).

---

## 7. Non-goals of governance

Governance does not:

- Re-open sealed package checksums to make tests pass
- Authorize Golden Dataset or snapshot edits
- Authorize mixing Rule Engine business logic into UI or pipeline orchestration
- Authorize Decision Packages to run outside `CanonicalDecisionPipeline`
