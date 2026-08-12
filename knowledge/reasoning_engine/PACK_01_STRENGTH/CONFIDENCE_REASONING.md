# Confidence Reasoning

| Field | Value |
|-------|-------|
| Document | CONFIDENCE_REASONING |
| Version | 1.0.0 |

---

# 1. Purpose

Confidence is not only a Mode A percentage.

It changes **which claims** enter Customer Mode and **how strong** the language may be.

Customers never see `%` or the word `confidence`.

---

# 2. Bands → language_strength

| Band | Customer claims | Modality (composer later) |
|------|-----------------|---------------------------|
| canonical / high | firm allowed for class + well-gated units | clear assertion |
| medium | qualified | thường / có xu hướng / khả năng cao |
| low | Validation-only, or “có dấu hiệu / cần đối chiếu thêm” | no firm life advice |
| experimental | almost never Customer Mode | insufficient or omit |

`partially_supported` units cannot be `firm` even if band is high.

---

# 3. Effects on selection

1. Units with `confidence_requirement = high_plus` drop from Customer Mode if band < high.
2. Alternative runner-up forces at least `qualified` on Conclusion if shares are material (see Alternative).
3. Engine confidence 100% is **not** a license for `firm` if interpretation band is high-but-not-canonical or C1 is live.
4. Low interpretation confidence + strong evidence on one dimension → still cautious globally; that dimension may be `qualified` in Why, not a new class.

---

# 4. CASE-0001 (from prototype input)

Interpretation confidence **72% = high**.

C1 live + thin root → Conclusion `qualified`, not `firm` omnipotence.

Not `cautious` (class is not at 0.65 edge; four strengthen groups).

No percent in Mode B.

---

END
