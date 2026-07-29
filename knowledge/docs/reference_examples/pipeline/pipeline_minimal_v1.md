# Pipeline Minimal Reference Example

> Module: Knowledge Framework
>
> Version: 1.0.0
>
> Status: Stable
>
> Document Type: Pipeline Reference Example
>
> Origin: reference_example
>
> BTE Platform

---

# Summary

Minimal valid pipeline stage listing per `PIPELINE_MODEL_SPEC.md`.

---

# Stages

| Stage | Output |
|-------|--------|
| Input | Raw birth data |
| Context Builder | Context |
| Validation | Pass or fail |
| Rule Loader | Rule registry |
| Rule Matcher | Rule matches |
| Priority Resolver | Resolved matches |
| Score Engine | Scores |
| Interpretation Builder | Interpretations |
| Result Builder | Result |

---

# Flow

```
Raw Input → Context → Validation → Rules → Match → Priority → Score → Interpretation → Result
```

---

# References

- `PIPELINE_MODEL_SPEC.md`
- `REFERENCE_EXAMPLE_REQUIREMENTS.md`

---

# Metadata

| Field | Value |
|-------|-------|
| schema_version | 1.0.0 |
| version | 1.0.0 |
| status | active |
| origin | reference_example |
| author | BTE |
| created_at | 2026-07-29T08:00:00Z |
| updated_at | 2026-07-29T08:00:00Z |
