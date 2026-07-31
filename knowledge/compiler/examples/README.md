# Compiler Examples

**Path:** `knowledge/compiler/examples/`  
**Version:** `1.0.0`  
**Status:** Non-normative samples  

---

## Purpose

Demonstrate shapes expected by future Compiler / Validation Engine integrators.

These files are **examples only**. They do not represent a real compile of academic packs or Knowledge Records.

---

## Files

| File | Demonstrates |
|------|----------------|
| `pipeline_run.sample.json` | Run envelope, stages executed, publish not attempted |
| `stage_invocation.sample.json` | Single stage call with artifact I/O + warning code |
| `compiler_error.sample.json` | Error event bound to `error_registry.json` code |
| `validation_report.sample.json` | `validation_report` artifact with findings |

---

## Rules for samples

1. Stage IDs MUST exist in `stage_registry.json`
2. Artifact IDs MUST exist in `artifact_registry.json` (snake_case)
3. Error / finding codes MUST exist in `error_registry.json`
4. Do not invent academic `SRC-*` / `KNO-*` claims in samples
5. Do not treat sample `run_id` values as production telemetry

---

## Integration tip

When implementing the runtime compiler:

1. Emit errors using registry `code` + copy `title` / `severity` / `recommended_action`
2. Attach `context` objects for paths, artifact IDs, and source IDs
3. Aggregate findings into `validation_report` before STAGE-PUBLISH

---

## Out of scope

- Executable fixtures
- Golden academic outputs
- Load tests / performance baselines
