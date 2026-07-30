# Report Generator Public API

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Public API Contract)

---

# 1. Purpose

This document defines the official public interface of the Report Generator.

---

# 2. Public Entry Point

```text
ReportGenerator.assemble(
    context: ReportAssemblyContext
) -> ReportGeneratorResult
```

No additional public methods are exposed.

No multi-parameter APIs are permitted.

Upstream results must not be passed as separate parameters.

---

# 3. Input Contract

Input Type:

```text
ReportAssemblyContext
```

Requirements:

- Immutable
- Validated
- Complete for declared format profile
- Contains published `interpretation_result`
- Contains published `analysis_result` when format profile requires structured analytical sections

Upstream results are accessed through:

```text
ReportAssemblyContext.interpretation_result
ReportAssemblyContext.analysis_result
ReportAssemblyContext.format_profile
```

---

# 4. Output Contract

```text
ReportGeneratorResult
```

Shall be immutable, deterministic, and safe for Delivery Layer consumption.

Mandatory format outputs when profile declares full publication:

- `StructuredReport`
- HTML artifact
- PDF artifact
- JSON artifact
- Markdown artifact

Partial format profiles may restrict outputs; restricted profiles must be explicit in format_profile.

---

# 5. Assembly Boundary

Public API does not expose interpretation logic or upstream stage recomputation.

Assembly reads from ReportAssemblyContext only.

---

# 6. Error Contract

Failures surface as classified errors. No false-complete ReportGeneratorResult on mandatory failure.

---

# 7. Compatibility

| Consumer | May consume ReportGeneratorResult |
|----------|-----------------------------------|
| Delivery Layer | Yes |
| Portal / API / CLI | Via Delivery Layer |
| Interpretation Engine | No (upstream only) |
| Upstream Analysis stages | No |

---

# 8. Non-Public Surfaces

Internal serializers, layout binders, and intermediate models are not public API.

---

# 9. Acceptance Criteria

Public API is accepted when single entry point, input/output contracts, and boundaries are complete.
