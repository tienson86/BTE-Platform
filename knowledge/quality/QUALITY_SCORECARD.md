# QUALITY_SCORECARD

| Field | Value |
|-------|-------|
| Document | QUALITY_SCORECARD |
| System | Quality Gate System V1.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-13 |
| Scale | 0–10 · PASS / PARTIAL / FAIL where noted |

Numbers are copied from published reviews. This scorecard does not invent scores.

Sources: `knowledge/validation/GOLDEN_DATASET_V1/` · feature commercial reviews · CASE_0003 customer review · CLL V1.2 commercial review.

---

## Dimensions

| Dimension | What it tracks |
|-----------|----------------|
| Identity | Customer Identity Report |
| Career | Customer Career Report |
| Executive | Executive / Master consulting |
| Composer | Customer-facing commercial-quality / lived language |
| Knowledge | Knowledge depth and status (not engine math) |
| Reasoning | Fact fidelity, conflict handling, no leakage |
| Context | Audience / capacity / input packaging |
| Regression | Frozen Golden hold |
| Commercial | Overall CX |
| Overall | Published commercial overall for the case; platform = current gate |

---

## CASE_0001 — Frozen Golden

| Dimension | Score / verdict | Source |
|-----------|-----------------|--------|
| Identity | **8.7** | Identity COMMERCIAL_REVIEW |
| Career | **8.6** | Career COMMERCIAL_REVIEW |
| Executive | **9.4** | Part 08 customer review |
| Composer | **8.5+** (commercial readiness) | feature reviews / Part 08 |
| Knowledge | PARTIAL — Master present; Part 06 timeline thin | customer acceptance conditions |
| Reasoning | PASS — self-carry / Chính Ấn held | Golden + CDR regression |
| Context | PASS — adult pass_through | product_context/CASES.md |
| Regression | **PASS** (this case is the target) | Golden regression records |
| Commercial | **8.0** | COMMERCIAL_ACCEPTANCE_REVIEW |
| Overall | **8.0** · Acceptance **PASS** | same |

---

## CASE_0002 — Active / not Golden

| Dimension | Score / verdict | Source |
|-----------|-----------------|--------|
| Identity | **6.8** | CLL V1.2 COMMERCIAL_REVIEW |
| Career | **6.5** | same |
| Executive | **6.9** | same |
| Composer | **6.5** (commercial quality) | same |
| Knowledge | PARTIAL — DRAFT_KNOWLEDGE (ISS-009); stems improved not closed (RV-003) | issue tracker |
| Reasoning | PARTIAL — dual-layer mapped; publish wording clash OPEN (RV-004) | DOMAIN_REVIEW / RV-004 |
| Context | PASS — adult | product_context |
| Regression | **PASS** vs CASE_0001 | CASE_0001_REGRESSION records |
| Commercial | **~6.7** | CLL V1.2 |
| Overall | **~6.7** · Acceptance **NOT PASS** | below 7.0 |

---

## CASE_0003 — Stress / not Golden

| Dimension | Score / verdict | Source |
|-----------|-----------------|--------|
| Identity | **4.7** | CASE_0003 CUSTOMER_REVIEW |
| Career | **3.1** | same |
| Executive | **4.3** | same |
| Composer | **3.5** (commercial quality) | same |
| Knowledge | PARTIAL — not the primary failure | ROOT_CAUSE |
| Reasoning | PARTIAL — CDR detects TRUE_CONFLICT; CX under-surfaces (ISS-C3-003) | BASELINE / ISSUES |
| Context | **FAIL** — child + weak packaged as adult career | ISS-C3-004 / 008 · product_context |
| Regression | **PASS** vs CASE_0001 | CASE_0003 REGRESSION |
| Commercial | **4.2** | CUSTOMER_REVIEW |
| Overall | **4.2** · Acceptance **NOT PASS** | same |

---

## Platform rollup (2026-08-13)

| Dimension | Platform verdict | Rule used |
|-----------|------------------|-----------|
| Identity | NOT at RC2 | Mandatory RC2 case 0002 = 6.8 |
| Career | NOT at RC2 | 0002 = 6.5; 0003 FAIL (out of V1 ship set) |
| Executive | NOT at RC2 | 0002 = 6.9 |
| Composer | NOT at RC2 | 0002 = 6.5 |
| Knowledge | PARTIAL | DRAFT on generic domains |
| Reasoning | PARTIAL | 0001 PASS; 0002/0003 residual |
| Context | FAIL for child SKU | 0003; adult context PASS |
| Regression | **PASS** | Frozen set n=1 |
| Commercial | **8.0** on Golden only; **6.7** blocks RC2 | min of mandatory set |
| Overall | **Q1 / RC1** | cannot advance |

Do not average 8.0 with 6.7 and 4.2 to claim a platform 6.x “almost ready.”

---

## CASE_0004–0010

Unscored. Placeholders.

---

END
