# Report Generator Algorithm

**Module:** `engines/analysis_engine/10_report_generator`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document defines the logical algorithm of Report Generator assembly and serialization.

It does not provide implementation source code.

---

# 2. Algorithm Principles

- Deterministic
- Non-mutating
- Non-interpreting
- Non-recomputing
- Format-neutral canonical model first
- Fail-closed on incomplete prerequisites

---

# 3. Logical Algorithm

```text
1. Validate ReportAssemblyContext
2. Read InterpretationResult from context
3. Read AnalysisResult from context when profile requires it
4. Verify assembly prerequisites for declared format profile
5. Resolve format profile and requested output set
6. Initialize StructuredReport skeleton
7. Bind InterpretationResult sections into ReportSection entries
8. Bind AnalysisResult structured data into StructuredDataBlock entries (read-only)
9. Attach report metadata and trace references
10. Validate StructuredReport schema and completeness
11. Serialize StructuredReport to HTML
12. Serialize StructuredReport to PDF
13. Serialize StructuredReport to JSON
14. Serialize StructuredReport to Markdown
15. Assemble ReportGeneratorResult with all required artifacts
16. Return immutable result
```

---

# 4. Assembly Rules

- StructuredReport is built before any format-specific serialization.
- Interpretation content is bound by reference; text is not rewritten or regenerated.
- Analytical data is attached read-only; values are not recalculated.
- All format outputs must derive from the same StructuredReport instance for a given request.
- Missing mandatory interpreted section aborts assembly.

---

# 5. Serialization Rules

| Format | Source | Rule |
|--------|--------|------|
| HTML | StructuredReport | Deterministic layout rendering |
| PDF | StructuredReport | Deterministic document rendering |
| JSON | StructuredReport | Lossless structured envelope where profile allows |
| Markdown | StructuredReport | Deterministic text/markdown rendering |

Serializers must not introduce interpretation not present in upstream results.

---

# 6. Format Profile Resolution

Format profile determines:

- which output formats are mandatory
- whether AnalysisResult binding is required
- layout ordering constraints
- metadata inclusion policy

Profile resolution is read-only; Report Generator does not infer business meaning from profile.

---

# 7. Complexity Constraints

Assembly is linear in the number of sections and structured data blocks.

Unbounded interpretation, rule matching, or domain recomputation is forbidden.

---

# 8. Acceptance Criteria

Algorithm is accepted when logical steps, assembly rules, serialization rules, and non-interpretation guarantees are complete and implementation-free.
