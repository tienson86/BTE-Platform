# QUALITY_BACKLOG

| Field | Value |
|-------|-------|
| Document | QUALITY_BACKLOG |
| System | Quality Gate System V1.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-13 |

Every tracked issue belongs to **exactly one** quality category.

Bodies stay in original issue files. This backlog classifies them for release governance.

Issue identities: `knowledge/validation/GOLDEN_DATASET_V1/ISSUE_TRACKER.md` (do not edit that file from here).

---

## Categories (frozen)

| Category | Use when the defect is primarily |
|----------|----------------------------------|
| Identity | Who-am-I product quality |
| Career | Work-direction product quality |
| Executive | Integrated consulting / master substitute |
| Composer | Lived language, templates, bias, claim-key leakage |
| Knowledge | Missing / draft / untranslated Knowledge |
| Reasoning | Cross-domain, conflict, fact mapping, publish-consistency of meaning |
| Context | Audience, age, capacity, input/chart contract |
| Regression | Golden hold / leakage into Golden |
| Commercial | Packaging, SKU, feature availability, sellability |

If two categories fit, choose the **customer-visible primary**. Do not split one Issue ID.

---

## Open / residual — CASE_0002

| Issue ID | Category | Severity | Status | Blocks |
|----------|----------|----------|--------|--------|
| ISS-009 | Knowledge | S2 | OPEN | Commercial V1.1 (not RC2 if scores hit floor) |
| ISS-010 / RV-005 | Commercial | S2 | OPEN | Advisor / Master SKU; not adult V1 Identity/Career if features AVAILABLE |
| ISS-012 / RV-004 | Reasoning | S2 | OPEN | V1.1 polish; Domain PARTIAL |
| RV-003 | Knowledge | S2 | IMPROVED | V1.1 lexicon completeness |
| ISS-005 | Composer | S1→improved | IMPROVED | Closed enough for CLL; residual via RV-003 |
| RV-006 | Identity | S2 | IMPROVED | RC2 until Identity ≥ 7.0 |

Score gap (no separate Issue ID): Identity 6.8 · Career 6.5 · Executive 6.9 · Commercial ~6.7. That **score gap is the RC2 blocker**. Treat as category **Commercial** until a new Issue ID is opened against the owning layer.

---

## Open — CASE_0003

| Issue ID | Category | Severity | Status | Blocks |
|----------|----------|----------|--------|--------|
| ISS-C3-001 | Context | S1 | OPEN | Commercial V1.1 (input contract) |
| ISS-C3-002 | Composer | S1 | OPEN | Q3 / V1.1 |
| ISS-C3-003 | Composer | S1 | OPEN | Q3 / V1.1 |
| ISS-C3-004 | Context | S1 | OPEN | Q3; any child SKU; RC2 **decision** required |
| ISS-C3-005 | Composer | S1 | OPEN | Q3 / V1.1 |
| ISS-C3-006 | Composer | S2 | OPEN | V1.1 |
| ISS-C3-007 | Composer | S2 | OPEN | V1.1 |
| ISS-C3-008 | Context | S2 | OPEN | Q3 policy gate |

Primary RC2 duty for this case: **record a packaging decision** (policy live vs owned S1 with expiry). Closing all S1 is Commercial V1.1 / Q3.

---

## CASE_0001

No S0/S1. Residual packaging notes (Part 06 thin, Part 03 dry, vocabulary, appendices) stay in the customer review. Category if promoted later: **Commercial** (packaging), not engine defects.

Regression category: **PASS**.

---

## Resolved (keep visible)

| Issue ID | Category | Status |
|----------|----------|--------|
| ISS-001, ISS-002 | Commercial | IMPROVED (features wired) |
| ISS-003, ISS-004, ISS-006 | Reasoning | IMPROVED |
| ISS-007 / RV-002 | Career / Composer | RESOLVED |
| ISS-011 | Composer | IMPROVED |
| RV-001 | Composer | RESOLVED |

---

## Category counts (open + improved-not-closed)

| Category | Open S1 | Open S2 | RC2 relevant |
|----------|--------:|--------:|--------------|
| Identity | 0 | 1 (RV-006 improved; score still < 7) | Yes — score |
| Career | 0 | 0 (+ score < 7) | Yes — score |
| Executive | 0 | 0 (+ score < 7) | Yes — score |
| Composer | 3 (0003) | 2 | V1.1; 0002 composer 6.5 |
| Knowledge | 0 | 2 | No for RC2 if CX floor met |
| Reasoning | 0 | 1 | No for RC2 if CX floor met |
| Context | 2 S1 + 1 S2 | — | RC2 decision; Q3 close |
| Regression | 0 | 0 | Must stay PASS |
| Commercial | 0 | 1 (Master) + score gap | Yes — 0002 overall |

---

## New issue rule

1. Register in Golden Dataset tracker first (identity + severity + layer).
2. Add one row here with **one** category.
3. Name the earliest gate it blocks.
4. Do not recategorize to dodge a gate.

---

END
