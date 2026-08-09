# Release Notes — bz_01_strength_core 1.2.0

**Sprint:** KX-1C  
**Supersedes:** 1.1.0

Adds Reasoning Framework instance graphs (strong / weak / balanced). No rule or evidence-logic changes.

---

# Release Notes — bz_01_strength_core 1.1.0

**Date:** 2026-08-09  
**Sprint:** KX-1B  
**Supersedes:** 1.0.0

## Summary

Adds the Knowledge Evidence Layer. Every Strength Core rule now has a reviewable Evidence Bundle (explanation, rationale, confidence, examples, relationships, traceability). Analytical rule logic is unchanged.

## Migration

Additive MINOR. Engines that ignore `evidence/` continue to work. Golden Dataset files were not modified.

---

# Release Notes — bz_01_strength_core 1.0.0

**Date:** 2026-08-09  
**Sprint:** KX-1A  
**Quality target:** Gold (structural + documentation + examples)

## Summary

First production-grade Knowledge Package for Day Master strength. Rules encode BTE traditional weights (month command, root, support, control, level thresholds) without copying copyrighted commentary.

## What is included

- 110 enabled official rules (`SKC-000001` …)
- Structured concept references
- Three chart examples (strong / weak / balanced)
- Package tests and validation profile

## Compatibility

- Schema 2.0.0 / knowledge 1.0.0 / package spec 1.0.0
- `compatible_with_v1`: true (dual-read; does not replace V1 rule files)
- Min platform 1.0.0

## Migration notes

Additive package. No migration of existing Rule Database ids. Engines continue to read V1 until explicitly wired.

## Breaking changes

None (first release).
