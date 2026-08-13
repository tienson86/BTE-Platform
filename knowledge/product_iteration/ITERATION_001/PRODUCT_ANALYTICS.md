# PRODUCT_ANALYTICS

| Field | Value |
|-------|-------|
| Iteration | 001 |
| Status | **AUTHORITATIVE schema** |

Definitions only. No new scoring engine.

---

## Feature scores (0–10)

| Metric | Question |
|--------|----------|
| **Identity** | Does the buyer recognize themselves (or the child, if parent)? |
| **Career** | Does this help a work decision — or is Career correctly hidden? |
| **Executive** | Does the close create confidence to act (or to rest)? |
| **Overall** | Commercial score for that deliverable (mean of CX dimensions used in that review) |

Lab feature scores for CASE_0001 Identity/Career come from product feature reviews.  
Discovery scores use the persona lens (P04 ≠ P01).

---

## Commercial CX (0–10)

| Metric | Question |
|--------|----------|
| **Trust** | Do I believe this consultant — nothing invented or hidden? |
| **Clarity** | Can I retell this without a glossary? |
| **Actionability** | Do I know what to do (or stop) this week? |
| **Purchase Intent** | Would I pay for this as delivered? |
| **Recommendation** | Would I recommend this to someone like me? |

RC3 also tracks **Value**. Record Value in notes when present; the official 001 ledger columns are the five above plus features.

---

## Sources (do not mix silently)

| Code | Meaning |
|------|---------|
| `lab` | Internal commercial review (CASE_0001–0003, EPIC-A/B) |
| `discovery` | Persona simulation (P04–P06) |
| `live-beta` | RC3-FF-1.0 completed by a real participant |

A `lab` 8.0 must not be averaged with a `discovery` 5.7 to “pass” a cohort.

---

## Floors (reference — Quality Gates remain authority)

| Set | Floor |
|-----|-------|
| Lab adult commercial (RC2) | Identity / Career / Executive / Overall **≥ 7.0** |
| RC3 discovery cohort | Trust / Clarity / Value / Action **≥ 7.0** · Rec ≥ 7/10 · Pay ≥ 6/10 |
| CASE_0001 | Frozen Golden — regression **PASS** |

001 does not change those gates.

---

## ROI

| Term | Definition |
|------|------------|
| Expected ROI | Forecast Δ Overall (and which metrics) **before** the change |
| Observed ROI | Actual Δ after revalidation |
| Layer | Single owner: Context · CLL · Theme Library consume · Composer · (not Truth) |

High ROI = large expected Δ · small surface · no Golden risk · no new architecture.

---

END
