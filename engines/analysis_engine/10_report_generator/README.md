# Report Generator

| Field | Value |
|-------|-------|
| Module Path | `engines/analysis_engine/10_report_generator` |
| Module Type | Analysis Engine Output Assembly Stage |
| Stage Order | 10 — Report assembly and multi-format publication |
| Document Type | Architecture Baseline |
| Version | 1.0.0 |
| Status | Frozen |

---

# 1. Purpose

The Report Generator assembles finalized analytical and interpretive content into deliverable report artifacts.

It is the tenth stage of the extended Analysis Engine output pipeline. Its purpose is to produce deterministic, structured, multi-format report outputs without performing interpretation or domain recomputation.

The module answers one question only:

> How is the already-interpreted analytical content assembled and published as HTML, PDF, JSON, Markdown, and Structured Report?

It does not interpret rules, select sentences, resolve priorities, or recompute any analytical stage.

---

# 2. Responsibilities

1. Accept validated `ReportAssemblyContext` containing published upstream outputs.
2. Read `InterpretationResult` as the primary narrative and section source.
3. Read `AnalysisResult` for structured analytical data binding when required by the report profile.
4. Validate assembly prerequisites and format profile completeness.
5. Build canonical `StructuredReport` as the internal assembly model.
6. Bind interpreted sections and structured data into report layout slots.
7. Serialize `StructuredReport` into HTML, PDF, JSON, and Markdown outputs.
8. Record assembly diagnostics and execution metadata.
9. Publish immutable `ReportGeneratorResult`.

---

# 3. Scope

In scope:

- InterpretationResult consumption
- AnalysisResult structured data binding (read-only)
- StructuredReport assembly
- HTML publication
- PDF publication
- JSON publication
- Markdown publication
- Format profile validation
- Assembly diagnostics
- Publication of `ReportGeneratorResult`

---

# 4. Out of Scope

| Concern | Owning Module |
|---------|---------------|
| Sentence selection / narrative generation | Interpretation Engine |
| Rule matching for interpretation | Interpretation Engine |
| Priority resolution for interpretation | Interpretation Engine |
| Strength / Temperature / Pattern / Useful God / Ten Gods / Combination / ShenSha / Luck recomputation | Upstream Analysis stages |
| Cross-stage analytical consolidation | Summary Engine |
| Domain knowledge rule execution | Upstream stages / Interpretation Engine |
| Client delivery transport (HTTP, portal routing) | Delivery Layer |

---

# 5. Inputs

| Input | Source |
|-------|--------|
| ReportAssemblyContext | Analysis Runtime / Orchestrator |
| InterpretationResult | `ReportAssemblyContext.interpretation_result` |
| AnalysisResult | `ReportAssemblyContext.analysis_result` (when profile requires structured data) |
| Format Profile | `ReportAssemblyContext.format_profile` |

Upstream outputs are never accepted as separate function parameters.

---

# 6. Output

```text
ReportGeneratorResult
```

Containing at minimum:

- `StructuredReport`
- HTML artifact
- PDF artifact
- JSON artifact
- Markdown artifact

---

# 7. Public API

```text
ReportGenerator.assemble(context: ReportAssemblyContext) -> ReportGeneratorResult
```

---

# 8. Position in Pipeline

```text
Summary Engine
        │
        ▼
AnalysisResult
        │
        ▼
Interpretation Engine
        │
        ▼
Report Generator              ← this module
        │
        ▼
Delivery Layer
```

---

# 9. Design Principles

- Single responsibility (assembly and serialization only)
- Deterministic
- Stateless
- No interpretation
- No upstream recomputation
- Non-mutating consumption of upstream results
- Immutable outputs
- Fail-closed validation

---

# 10. Version

| Item | Value |
|------|-------|
| Module Version | 1.0.0 |
| Status | Frozen |

Breaking semantic changes require a major version increment.
