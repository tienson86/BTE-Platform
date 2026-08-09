# Generation Quality Gates

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Aligns with** | KD-4 `knowledge/authoring/quality/` |
| **Status** | Canonical |
| **Runtime** | None — no scoring algorithm implementation |

Official packages MUST declare `quality_target`. Release candidate minimum remains **Bronze**. Default official target remains **Silver** (KD-4). Analytical packages that include evidence + reasoning SHOULD target **Gold**.

Metrics are specified as ratios 0.0–1.0. Future tools compute them; this document does not implement a scorer.

---

## 1. Inherited KD-4 metrics

| Id | Bronze | Silver | Gold | Platinum |
|----|--------|--------|------|----------|
| QM-META-COMPLETE | 1.0 | 1.0 | 1.0 | 1.0 |
| QM-ID-QUALITY | 1.0 | 1.0 | 1.0 | 1.0 |
| QM-DEP-QUALITY | 1.0 | 1.0 | 1.0 | 1.0 |
| QM-PKG-COMPLETE | 1.0 | 1.0 | 1.0 | 1.0 |
| QM-EXAMPLE-BOUND | 1.0 | 1.0 | 1.0 | 1.0 |
| QM-DOC-COMPLETE | 0.5 | 1.0 | 1.0 | 1.0 |
| QM-REF-QUALITY | 0.5 | 0.8 | 0.95 | 1.0 |
| QM-LANG-CONSISTENCY | 0.8 | 0.95 | 1.0 | 1.0 |

---

## 2. Generator completeness metrics

| Id | Formula | When required |
|----|---------|---------------|
| QM-EVD-COMPLETE | bundles_with_required_sections / production_rules | `evidence_required` |
| QM-RSN-COMPLETE | conclusion_classes_with_full_chain / primary_conclusion_classes | `reasoning_required` |
| QM-GEN-TRACE | artifacts_with_generator_metadata / generated_artifacts | always |
| QM-PIPELINE-COMPLETE | stages_pass_or_na / 13 | always |

If a metric is N/A (flag false), treat as 1.0 for gate math and record `not_applicable`.

| Id | Bronze | Silver | Gold | Platinum |
|----|--------|--------|------|----------|
| QM-EVD-COMPLETE | 1.0 if required else N/A | 1.0 | 1.0 | 1.0 |
| QM-RSN-COMPLETE | 0.0 allowed if draft-only | 1.0 if required | 1.0 | 1.0 |
| QM-GEN-TRACE | 1.0 | 1.0 | 1.0 | 1.0 |
| QM-PIPELINE-COMPLETE | ≥ 9/13 (through tests or N/A) | 13/13 | 13/13 | 13/13 |

---

## 3. Gate definitions

### Bronze

Structurally valid generated draft that may become a release candidate.

- PVP-STANDARD technical stages pass (or PVP-MINIMAL only if still `draft` and not claiming RC)
- KD-4 Bronze floors
- QM-GEN-TRACE = 1.0
- Unique ids; taxonomy domain exists
- No engine / existing-package mutation

### Silver

Bronze plus complete documentation and strong references.

- All Bronze
- QM-DOC-COMPLETE = 1.0
- QM-REF-QUALITY ≥ 0.8
- QM-LANG-CONSISTENCY ≥ 0.95
- QM-PIPELINE-COMPLETE = 13/13
- If `evidence_required` / `reasoning_required`: corresponding completeness = 1.0

### Gold

Silver plus examples/tests and near-complete references.

- All Silver
- QM-REF-QUALITY ≥ 0.95
- QM-LANG-CONSISTENCY = 1.0
- `example_required` satisfied
- Analytical / interpretation / report: `tests/` present
- Primary conclusion classes each have a reasoning chain when reasoning is required

### Platinum

Gold plus release hygiene.

- All Gold
- QM-REF-QUALITY = 1.0
- PVP-RELEASE pass
- golden_dataset_validation `pass` or `not_applicable` with waiver
- Zero unacknowledged release warnings
- Checksum sealed; `status=released` immutability recorded

---

## 4. Type recommendations

| Package type | Suggested `quality_target` |
|--------------|----------------------------|
| analytical | `gold` |
| interpretation | `gold` |
| report | `gold` |
| sentence | `silver` |
| metadata | `silver` |
| minimal / reference | `bronze` |

Claims above the measured gate are a GV-QUALITY-CLAIM failure.
