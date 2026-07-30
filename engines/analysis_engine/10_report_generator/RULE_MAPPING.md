# Report Generator Rule Mapping

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Mapping Specification)

---

# 1. Purpose

This document defines how Report Generator maps upstream outputs into report structures and format artifacts.

Report Generator does not consume domain Knowledge Modules for interpretation or recomputation.

Mapping is structural assembly of published InterpretationResult and AnalysisResult content.

---

# 2. Mapping Principle

```text
Upstream published output  →  Assembly target  →  Format artifact
```

---

# 3. Interpretation → Report Mapping

| InterpretationResult Source | Assembly Target | StructuredReport Section |
|----------------------------|-----------------|--------------------------|
| Interpreted section | ReportSection | report.sections[] |
| Section title / identity | Section metadata | section.id / section.title |
| Section body content | Bound content reference | section.content |
| Interpretation trace metadata | Trace reference | section.source_trace |

Exact section identifiers remain backward compatible within V1.x once published.

---

# 4. Analysis → Structured Data Mapping

| AnalysisResult Source | Assembly Target | StructuredReport Block |
|-----------------------|-----------------|------------------------|
| Stage result payload | StructuredDataBlock | structured_data.blocks[] |
| SummaryResult | Summary structured block | structured_data.summary |
| Chart / request metadata | Report metadata | metadata.analytical_context |

Binding is read-only projection; no semantic override.

---

# 5. StructuredReport → Format Mapping

| StructuredReport Element | HTML | PDF | JSON | Markdown |
|--------------------------|------|-----|------|----------|
| ReportSection | Section HTML node | Section page block | Section JSON object | Section heading + body |
| StructuredDataBlock | Data table / block | Data table / block | JSON data node | Markdown table / block |
| ReportMetadata | Document header | Document header | Envelope metadata | Front matter |
| Trace references | Footer / meta | Footer / meta | trace field | Comment / meta block |

All mappings are deterministic and non-interpreting.

---

# 6. Non-Mapping Rules

Report Generator must not:

- map to Interpretation Engine sentence libraries for text generation
- map to domain Knowledge Modules for rule execution
- map to priority engines for narrative resolution
- override InterpretationResult semantics
- recompute analytical stage outputs

---

# 7. Layout Template Mapping

Presentation layout templates may map layout slots to StructuredReport sections.

Layout templates control presentation only.

They do not supply interpretive content.

---

# 8. Acceptance Criteria

Rule Mapping is accepted when interpretation-to-report mapping, structured-data mapping, format mapping, and non-mapping rules are complete.
