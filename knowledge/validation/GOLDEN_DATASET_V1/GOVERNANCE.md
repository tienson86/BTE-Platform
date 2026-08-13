# GOVERNANCE

| Field | Value |
|-------|-------|
| Document | GOVERNANCE |
| Dataset | GOLDEN_DATASET_V1 |
| Status | **FROZEN** |
| Date | 2026-08-13 |

---

## Golden Case ownership

| Case | Owner | Role |
|------|-------|------|
| CASE_0001 | Dataset Steward | Frozen Golden commercial reference |
| CASE_0002 | Validation Owner | Active generalization case |
| CASE_0003 | Validation Owner | Stress / extreme case |
| CASE_0004–0010 | Unassigned until bind | Placeholder |

**Dataset Steward** owns the laboratory tree, freeze status, and index integrity.

**Validation Owner** runs protocol stages 1–7 for non-frozen cases.

**Case Owner** (after bind) is accountable for INPUT freeze and artifact pointers. Until Product assigns a person, Validation Owner holds the slot.

A Golden Case is not owned by the engineer who last improved a layer.

---

## Review authority

| Review | Authority | Binding? |
|--------|-----------|----------|
| Customer Review | Customer Reviewer (paying-customer stance) | Binding on CX scores |
| Domain Review | Domain Reviewer | Binding on chart-fact fidelity |
| Consulting scorecard | Consultant Reviewer per `knowledge/consulting_quality/` | Binding when used |
| Issue severity | Validation Owner + Domain Reviewer | Binding |
| Root-cause layer | Domain + owning-layer engineer | Binding on layer, not on fix design |
| Regression verdict | Validation Owner | Binding |
| Commercial acceptance | Product | Binding on ship / no-ship |

No reviewer may rewrite Ground Truth artifacts to change a score.

---

## Approval chain

```text
Validation Owner (protocol complete)
        ↓
Customer Reviewer (CX)
        ↓
Domain Reviewer (facts)
        ↓
Dataset Steward (index, freeze, regression policy)
        ↓
Product (commercial gate / waivers)
```

| Decision | Required approvers |
|----------|-------------------|
| Bind a placeholder | Product + Dataset Steward + Domain |
| Mark GOLDEN | Customer + Domain + Dataset Steward |
| Mark FROZEN | Dataset Steward + Product |
| Waive S1 | Product (written, expiry required) |
| Waive S0 | Never for commercial freeze |
| Unfreeze / supersede | Dataset Steward + Product + Domain |
| Change this governance file | Dataset Steward + Product |

---

## Version policy

| Object | Policy |
|--------|--------|
| Laboratory | This folder is V1. Breaking protocol changes require a new laboratory version folder |
| Case freeze | Independent per case; CASE_0001 Frozen does not freeze CASE_0002 |
| Improvement cycles | Versioned subfolders in the **existing** artifact tree (example: `REVALIDATION_V1_1`) |
| Policy files in this tree | Frozen; amend only via CHANGELOG + approval chain |
| Historical captures | Immutable |

Version names:

- Laboratory: `GOLDEN_DATASET_V1`, later `V1.1` / `V2`
- Case cycle: `BASELINE`, `REVALIDATION_V1_1`, …
- Product commercial release labels (RC1 / RC2 / V1.0) are defined in [RELEASE_CRITERIA.md](RELEASE_CRITERIA.md) and are **not** the same as engine semver

---

## Dataset lifecycle

```text
PLACEHOLDER
    ↓  bind chart (approval)
ACTIVE
    ↓  protocol through Domain + Issues
REVIEWED
    ↓  commercial + regression gates
GOLDEN
    ↓  approval chain
FROZEN
    ↓  optional later cycle
SUPERSEDED  →  new GOLDEN/FROZEN version
```

STRESS is a parallel status for cases that remain in the laboratory but are not commercial ship samples. STRESS cases still follow protocol through Root Cause and still protect Golden regression.

Terminal states: FROZEN (current truth) or SUPERSEDED (historical truth).

Do not delete cases.

---

## Boundaries

| This laboratory governs | This laboratory does not govern |
|-------------------------|---------------------------------|
| Validation protocol and Golden status | Engine implementation |
| Issue format and freeze policy | Knowledge pack authoring |
| Commercial acceptance for cases | Portal / UI Foundation |
| Pointers to artifacts | File moves or report rewrites |
| KPI floors for cases | `tests/golden_dataset/` expected JSON |

---

## Records

Every governance action (bind, freeze, waive, supersede) must appear in [CHANGELOG.md](CHANGELOG.md) and [CASE_INDEX.md](CASE_INDEX.md).

---

END
