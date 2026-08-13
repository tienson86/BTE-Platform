# ISSUE_TRACKER

| Field | Value |
|-------|-------|
| Document | ISSUE_TRACKER |
| Dataset | GOLDEN_DATASET_V1 |
| Status | **CANONICAL FORMAT** |
| Date | 2026-08-13 |

This is the official issue register for Golden Dataset validation.

Do not invent a second format. Case-level ISSUES.md files must use the same columns.

Existing issue bodies stay in their original files. This tracker **indexes** them.

---

## Canonical format

| Column | Required | Values |
|--------|----------|--------|
| Issue ID | Yes | Stable id (`ISS-001`, `ISS-C3-001`, `RV-001`, …). Do not reuse. |
| Case | Yes | `CASE_0001` … `CASE_0010` |
| Severity | Yes | S0 blocker · S1 high · S2 medium · S3 low |
| Layer | Yes | ENGINE · REASONING · COMPOSER · KNOWLEDGE · FEATURE_PACKAGING · POLICY · RUNTIME_DATA · COMMERCIAL · NARRATIVE |
| Owner | Yes | Named layer team / role, not a person nickname |
| Status | Yes | OPEN · IMPROVED · RESOLVED · WONTFIX · WAIVED |
| Resolution | Yes | Pointer or one-line outcome. Empty only if OPEN. |

Optional fields (in the case ISSUES.md body, not required in this index table): Symptom, Customer impact, Evidence, Fix category.

---

## Severity

| Level | Meaning | Release |
|-------|---------|---------|
| S0 | Blocker — cannot deliver the product | Blocks Freeze and commercial release |
| S1 | High — trust, wrong-person advice, unsafe packaging | Blocks Freeze unless Product written waiver with expiry |
| S2 | Medium — depth, polish, lexicon | Does not block RC1; may block V1.0 if systemic |
| S3 | Low — residual packaging notes | Track only |

---

## Index — populated cases

Bodies are **not** copied. Open the source file.

### CASE_0001

No formal issue register exists in `knowledge/validation/` (CASE_0001 was accepted as Golden). Residual commercial notes live in the customer review; they are **not** promoted to S0/S1 here.

| Issue ID | Case | Severity | Layer | Owner | Status | Resolution |
|----------|------|----------|-------|-------|--------|------------|
| *(none registered)* | CASE_0001 | — | — | Dataset Steward | GOLDEN | Residual notes only: `knowledge/customer_review/CASE_0001/COMMERCIAL_ACCEPTANCE_REVIEW.md` (Part 06 thin, Part 03 dry, specialist vocabulary, appendix leakage). Packaging conditions, not open blockers. |

### CASE_0002 — baseline register

Source: `knowledge/validation/CASE_0002/ISSUES.md`

| Issue ID | Case | Severity | Layer | Owner | Status | Resolution |
|----------|------|----------|-------|-------|--------|------------|
| ISS-001 | CASE_0002 | S0 | COMMERCIAL | Feature composers | IMPROVED | Identity wired in CDR V1.1 revalidation. See `CASE_0002/REVALIDATION_V1_1/ISSUE_RETEST.md` |
| ISS-002 | CASE_0002 | S0 | COMMERCIAL | Feature composers | IMPROVED | Career wired in CDR V1.1 revalidation |
| ISS-003 | CASE_0002 | S1 | REASONING | Cross-domain / narrative | IMPROVED | Dual-layer reading in CDR V1.1 DOMAIN_REVIEW |
| ISS-004 | CASE_0002 | S1 | REASONING | Narrative / composer | IMPROVED | Chart-specific OPERATING_OUTPUT; CASE_0001 leakage removed |
| ISS-005 | CASE_0002 | S1 | COMPOSER | Composer / Knowledge | OPEN / IMPROVED | Lexicon reduced in CLL V1.2; still tracked via RV-003 |
| ISS-006 | CASE_0002 | S1 | REASONING | Cross-domain | IMPROVED | Tension explained; see DOMAIN_REVIEW |
| ISS-007 | CASE_0002 | S1 | COMPOSER | Career composer | IMPROVED | RV-002 later RESOLVED in CLL V1.2 acceptance |
| ISS-008 | CASE_0002 | S2 | KNOWLEDGE | Useful God pack + composer | IMPROVED | CLL V1.2 lived cooling language; not closed as Knowledge-complete |
| ISS-009 | CASE_0002 | S2 | KNOWLEDGE | Knowledge packs | OPEN | DRAFT_KNOWLEDGE program state |
| ISS-010 | CASE_0002 | S2 | COMMERCIAL | Feature packaging | OPEN | Master NOT_AVAILABLE (RV-005) |
| ISS-011 | CASE_0002 | S2 | NARRATIVE | Composer | IMPROVED | Avoids retargeted in revalidation |
| ISS-012 | CASE_0002 | S2 | ENGINE | Pattern publish | OPEN | RV-004 publish wording clash remains |

### CASE_0002 — post-revalidation register

Source: `knowledge/validation/CASE_0002/REVALIDATION_V1_1/REMAINING_ISSUES.md`  
Retest: `knowledge/commercial_language/IMPLEMENTATION_V1_2/CASE_0002_ACCEPTANCE.md`

| Issue ID | Case | Severity | Layer | Owner | Status | Resolution |
|----------|------|----------|-------|-------|--------|------------|
| RV-001 | CASE_0002 | S1 | COMPOSER | Feature composers | RESOLVED | CLL V1.2 — no claim keys |
| RV-002 | CASE_0002 | S1 | COMPOSER | Career composer | RESOLVED | CLL V1.2 — AUTHORITY output-led |
| RV-003 | CASE_0002 | S2 | KNOWLEDGE | UG pack + composer | IMPROVED | Lived cooling; stems not fully Knowledge-closed |
| RV-004 | CASE_0002 | S2 | ENGINE | Pattern publish | OPEN | Internal wording clash remains |
| RV-005 | CASE_0002 | S2 | FEATURE_PACKAGING | Packaging / master | OPEN | Master Consulting NOT_AVAILABLE |
| RV-006 | CASE_0002 | S2 | COMPOSER | Identity packaging | IMPROVED | Lived Identity improved in CLL V1.2; commercial floor not yet met |

### CASE_0003

Source: `knowledge/validation/CASE_0003/ISSUES.md`

| Issue ID | Case | Severity | Layer | Owner | Status | Resolution |
|----------|------|----------|-------|-------|--------|------------|
| ISS-C3-001 | CASE_0003 | S1 | RUNTIME_DATA | Calendar / input contract | OPEN | Stated pillars ≠ engine pillars |
| ISS-C3-002 | CASE_0003 | S1 | COMPOSER | CLL memory templates | OPEN | “mạnh hơn” on weak chart |
| ISS-C3-003 | CASE_0003 | S1 | COMPOSER | Composer / reasoning surface | OPEN | TRUE_CONFLICT under-surfaced in Customer Mode |
| ISS-C3-004 | CASE_0003 | S1 | FEATURE_PACKAGING | Packaging + policy | OPEN | Adult career for child |
| ISS-C3-005 | CASE_0003 | S1 | COMPOSER | CLL theme priority | OPEN | Output empowerment dominates conservation |
| ISS-C3-006 | CASE_0003 | S2 | COMPOSER | Action language | OPEN | Action realism vs weak 0.19 |
| ISS-C3-007 | CASE_0003 | S2 | COMPOSER | Composer / engine pairing | OPEN | Follow readability |
| ISS-C3-008 | CASE_0003 | S2 | POLICY | Product policy | OPEN | Minor / child feature gate unpublished |

### CASE_0004–CASE_0010

No issues. Placeholders.

---

## New issue rule

1. Assign next id in the case series (`ISS-…` baseline, `RV-…` revalidation cycle, `ISS-C3-…` CASE_0003).
2. Add a row here **and** a body in the case `ISSUES.md` (or pointer to the existing body).
3. Do not close an issue by deleting it. Set Status + Resolution.
4. Do not rewrite historical issue bodies to match a later fix. Add a retest note.

---

END
