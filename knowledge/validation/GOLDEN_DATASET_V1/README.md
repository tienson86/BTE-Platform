# GOLDEN_DATASET_V1

| Field | Value |
|-------|-------|
| Document | README |
| Dataset | GOLDEN_DATASET_V1 |
| Status | **OFFICIAL — Validation Laboratory** |
| Version | V1.0 (laboratory created 2026-08-13) |
| Location | `knowledge/validation/GOLDEN_DATASET_V1/` |
| Scope | Governance and case registry only |

This repository is the canonical **validation laboratory** for BTE Platform commercial acceptance and regression.

It does **not** modify engines, Knowledge packs, Rule Database, Reasoning, production pipeline, or commercial features.

It does **not** move or rewrite existing reports. Existing artifacts remain in place. This laboratory **indexes and governs** them.

---

## Purpose

Establish one official ground-truth set for:

- regression after any improvement
- commercial acceptance before release
- issue registration and root-cause classification
- freeze / version policy for Golden Cases

Future validation work must start here.

This laboratory is **not** `knowledge/golden_dataset/` (Knowledge Infrastructure framework) and **not** `tests/golden_dataset/` (engine fixture suite). Those remain separate.

---

## Scope

### In scope

- Case registry (CASE_0001–CASE_0010)
- Validation protocol
- Regression rules
- Issue tracker format
- Release criteria (RC1 / RC2 / V1.0)
- Change policy and governance
- Official KPIs
- Pointers to existing validation artifacts

### Out of scope

- Engine, Knowledge, Rule Database, or Reasoning edits
- Production pipeline or commercial feature code
- Duplicating Master Interpretations, PDFs, or pipeline JSON
- Moving files from `knowledge/validation/CASE_0002/`, `knowledge/validation/CASE_0003/`, `knowledge/master_interpretations/CASE_0001/`, or related trees
- Authoring new chart content for CASE_0004–CASE_0010 (placeholders only)

---

## Validation philosophy

```text
Measure first
    ↓
Review as customer
    ↓
Review as domain
    ↓
Register issues
    ↓
Classify root cause
    ↓
Improve the owning layer
    ↓
Prove no Golden regression
    ↓
Freeze what passed
```

Rules:

1. **Ground truth is frozen output + frozen review**, not a moving target rewritten to pass.
2. **Improvement is layer-owned.** Composer issues are not fixed by changing engines. Engine issues are not fixed by rewriting copy.
3. **No case is Golden because it looks good once.** It is Golden when protocol, scores, and regression hold.
4. **A later case must not break an earlier Golden Case.**
5. **Honesty over flattery.** Weak charts, children, and unresolved conflicts must remain visible.

Official workflow: [VALIDATION_PROTOCOL.md](VALIDATION_PROTOCOL.md).

---

## Ground Truth

Ground Truth for a case is the combination of:

| Layer | Meaning |
|-------|---------|
| Input | Frozen birth / chart input |
| Pipeline output | Deterministic engine + composition result |
| Customer review | Paying-customer scores and tests |
| Domain review | Chart-fact fidelity |
| Issue register | Open / resolved defects |
| Final score | Official KPI snapshot |
| Freeze record | Version + date + approvers |

Ground Truth lives in the **original artifact paths**. This laboratory records the pointer, status, and scores. It does not become a second copy of the report.

---

## Golden Cases

A **Golden Case** is a case that has completed the protocol and is frozen as commercial / regression reference.

| Status | Meaning |
|--------|---------|
| PLACEHOLDER | Slot reserved; no chart bound |
| ACTIVE | Artifacts exist; protocol in progress |
| REVIEWED | Customer + domain reviews recorded |
| GOLDEN | Meets commercial + regression gates |
| FROZEN | Golden and immutable except via CHANGE_POLICY |
| STRESS | Extreme / gap case; not a commercial ship sample |
| SUPERSEDED | Replaced by a later frozen version |

Current Golden / Frozen reference: **CASE_0001**.

CASE_0002 and CASE_0003 are registered validation cases, not Golden.

CASE_0004–CASE_0010 are empty slots.

Index: [CASE_INDEX.md](CASE_INDEX.md).

---

## Regression

No improvement may regress a frozen Golden Case.

Minimum rule: if CASE_0001 commercial meaning, pillars, strength band, pattern family, or customer-pass status moves without an approved version bump, the change is rejected.

Full rules: [REGRESSION_RULES.md](REGRESSION_RULES.md).

---

## Commercial Acceptance

Engineering tests are necessary and insufficient.

A case is commercially accepted only when:

- Identity, Career, and Executive (as applicable) meet KPI floors in [METRICS.md](METRICS.md)
- Customer Test questions are answerable
- No S0/S1 open blockers (unless Product waiver per [RELEASE_CRITERIA.md](RELEASE_CRITERIA.md))
- Domain review confirms chart-fact fidelity
- Consulting acceptance criteria in `knowledge/consulting_quality/05_ACCEPTANCE_CRITERIA.md` are respected

CASE_0001 is the current commercial reference (PASS, with packaging conditions recorded in the existing customer review).

CASE_0002 and CASE_0003 are **not** commercially accepted.

---

## Reading order

| Order | File |
|------:|------|
| 1 | This README |
| 2 | [DATASET_OVERVIEW.md](DATASET_OVERVIEW.md) |
| 3 | [CASE_INDEX.md](CASE_INDEX.md) |
| 4 | [VALIDATION_PROTOCOL.md](VALIDATION_PROTOCOL.md) |
| 5 | [REGRESSION_RULES.md](REGRESSION_RULES.md) |
| 6 | [ISSUE_TRACKER.md](ISSUE_TRACKER.md) |
| 7 | [RELEASE_CRITERIA.md](RELEASE_CRITERIA.md) |
| 8 | [CHANGE_POLICY.md](CHANGE_POLICY.md) |
| 9 | [METRICS.md](METRICS.md) |
| 10 | [GOVERNANCE.md](GOVERNANCE.md) |
| 11 | [CHANGELOG.md](CHANGELOG.md) |

Then the relevant `CASE_NNNN/` folder.

---

## Constraints

| Allowed | Forbidden |
|---------|-----------|
| Index existing artifacts | Duplicate report bodies |
| Record scores and status | Rewrite Master Interpretations |
| Register issues by reference | Move validation files |
| Freeze protocol and KPIs | Edit engines / Knowledge / rules to fill slots |

---

END
