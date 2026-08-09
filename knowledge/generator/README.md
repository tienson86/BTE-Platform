# BTE Knowledge Package Generator

| Field | Value |
|-------|-------|
| **Framework** | Knowledge Package Generator |
| **Version** | 1.0.0 |
| **Status** | Canonical Foundation |
| **Scope** | Specification only — no runtime, no packages generated in this sprint |

This folder is **not** a Knowledge Package and **not** a Rule Package.

It is the master specification used to generate every future Knowledge Package (Strength, Seasonal, Temperature, Pattern, Combination, Useful God, Shen Sha, Feng Shui, Qi Men, I Ching, …).

```
Profile → Skeleton → Metadata → Manifest → Rules → Evidence → Reasoning
      → Examples → Tests → Validation → Documentation → RC → Released
```

Existing packages (including Strength Core) are **not** modified. They remain valid dual-read artifacts. New packages MUST be produced from this Generator.

---

## Contents

| Path | Role |
|------|------|
| `KNOWLEDGE_PACKAGE_GENERATOR.md` | Canonical generator specification |
| `generator.schema.json` | Generator envelope schema |
| `package_profile.schema.json` | Generation profile schema |
| `generation_pipeline.md` | Thirteen canonical stages |
| `generation_workflow.md` | Mapping to KD-4 authoring states |
| `generation_constraints.md` | Mandatory constraints |
| `generation_validation.md` | Validation requirements (no runtime) |
| `generation_quality.md` | Bronze → Platinum gates |
| `generation_templates/` | Copy-paste artifact templates |
| `profiles/` | Reusable type profiles |
| `examples/` | Instance profiles (Strength, Seasonal, Pattern, Shen Sha) |
| `documentation/` | Philosophy, architecture, lifecycle, AI, extension |

Architecture pointer: `knowledge/docs/architecture/KNOWLEDGE_PACKAGE_GENERATOR.md`

---

## Standards referenced

| Sprint | Standard |
|--------|----------|
| KD-1 | Knowledge Database V2 envelopes |
| KD-2 | Taxonomy & ontology |
| KD-3 | Knowledge Package Specification |
| KD-4 | Authoring & validation pipeline |
| KX-1A | Analytical package (Strength Core rules) |
| KX-1B | Evidence layer |
| KX-1C | Reasoning Framework |

---

## Forbidden

Do not use this folder to modify engines, API, contracts, Rule Database content, Golden Dataset, snapshots, or existing released packages.
