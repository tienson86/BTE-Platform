# QA Scoring — V1.0

| Field | Value |
|-------|-------|
| Document | QA_SCORING |
| Standard | Knowledge QA V1.0 |
| Scale | 0–10 integers only |

---

# 1. Rule

- Each criterion receives one integer **0–10**.
- No half scores.
- No “N/A” without written justification (excluded from average).
- **Unit average** = sum of scored criteria ÷ number of scored criteria.

Verdict thresholds: [PASS_REVIEW_FAIL.md](PASS_REVIEW_FAIL.md).

---

# 2. Frozen anchors

| Score | Definition | Promotion impact |
|-------|------------|------------------|
| **0** | Criterion is **absent or actively harmful**. Claim violates doctrine, invents facts, or would damage customer trust if printed. | Automatic **FAIL** on unit |
| **3** | **Major defect** present. Unit cannot promote until fixed or explicitly waived by Domain Reviewer with record. | **FAIL** unless waived |
| **5** | **Material gap**. Unit may remain Draft; not Validated. Defect is documented and has assigned owner. | **REVIEW** maximum |
| **7** | **Acceptable with documented gap**. Production-usable if other criteria pass and gap is tracked. | **PASS** eligible |
| **9** | **Production-ready**. At most a minor note; no blocking gap. | **PASS** |
| **10** | **No defect** detected for this criterion under review conditions. | **PASS** |

---

# 3. Interpolation (not used)

Scores **1, 2, 4, 6, 8** are **not used** in V1.0.

If a reviewer cannot choose between anchors, use the **lower** anchor.

Example: between 5 and 7 → assign **5**.

---

# 4. Automatic FAIL triggers (any criterion)

Assign **0 or 3** and unit **FAIL** when:

| Trigger | Criterion |
|---------|-----------|
| Claim contradicts published class | Professional Correctness |
| Requires unpublished fact as if present | Evidence Compatibility |
| Wrong topic (score explanation in MEANING) | Domain Purity |
| Hard cross-pack dependency on unpublished pack | Cross-Pack Dependency |
| Rule ID, score, or threshold in claim | Commercial Quality |
| customer_mode ALLOWED for teaching-only governance claim | Consistency |
| No `source_document` or claim not in source | Traceability |

---

# 5. Unit average bands (guidance only)

Average **does not override** per-criterion FAIL triggers.

| Average | Typical verdict |
|---------|-----------------|
| ≥ 8.5 | PASS candidate if no criterion ≤ 3 |
| 7.0 – 8.4 | PASS or REVIEW |
| 6.0 – 6.9 | REVIEW |
| < 6.0 | REVIEW or FAIL |

Borderline: average **7.0–7.4** with all criteria ≥ 5 and none ≤ 3 → **Borderline** (human decision).

---

# 6. Pack phase reviews

Pack reviews (e.g. `PHASE_03_ADVANTAGES_REVIEW.md`) report:

1. Per-criterion score per unit
2. Unit average
3. Criterion averages across topic
4. PASS / REVIEW / FAIL counts

Criterion averages are diagnostic; **unit verdict is authoritative**.

---

END
