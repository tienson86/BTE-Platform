# B1_P0_003_INTERACTION_TRUTH_INTEGRATION_REPORT

| Field | Value |
|-------|-------|
| Issue | B1-P0-003 Interaction Truth Integration |
| Date | 2026-08-17 |
| Type | IMPLEMENTATION |
| Spec | B1-P0-002 Interaction Truth Specification |

---

## 1. Status

**COMPLETE — READY_FOR_ARTIFACT_REVIEW**

Canonical Interaction Truth is implemented as a facts-only layer between already-published Natal Truth / Luck identity and Narrative / Professional Report.

No new engine.

No Luck Domain.

No Narrative architecture redesign.

No Product Governance change.

No fabricated overlap.

Professional PDFs for Nguyễn Tiến Sơn, Lương Ngọc Huỳnh, and Ngô Đặng Minh Tân show **new interaction information**, not restamped natal thesis.

---

## 2. InteractionTruthFacts

Canonical model: `engines/interpretation_engine/foundation/facts/interaction.py`

Populated by `build_interaction_truth_facts` from already-published natal facts and LuckEngine period identity. Exact published-string match only.

| Field | Content |
|-------|---------|
| `current_period_identity` | Copied Da Yun label, years, stem, branch, element, yin/yang, ten-god, hidden stems, next cycle |
| `interaction_summary` | Period + natal governors + overlap count / empty-overlap flag + status |
| `helpful_factors` | Identity overlap with Useful God / Hỷ. Empty list is valid |
| `pressure_factors` | Identity overlap with Kỵ. Empty list is valid |
| `supported_direction` | Natal Useful God / Hỷ still in force, with overlap qualifier |
| `restricted_direction` | Natal Kỵ still in force, with overlap qualifier |
| `confidence` | Completeness of upstream evidence (`high` / `medium` / `low` / `unknown`). Not fortune |
| `evidence` | Upstream field paths only |
| `diagnostics` | Missing inputs, unpublished period tokens, `empty_identity_overlap`, `interaction_truth_missing` |
| `status` | `available` / `partial` / `missing` |

When interaction cannot be determined:

- no current period → `status = missing`, diagnostic `interaction_truth_missing`
- Useful God missing → `status = partial`, diagnostic `interaction_truth_missing`

Natal Hỷ / Kỵ are never copied into helpful / pressure merely because they exist.

---

## 3. Integration points

```
Natal Truth (analytical engines)
        ↓
InteractionTruthFacts (foundation builder)
        ↓
InterpretationFoundationBundle.interaction_truth
        ↓
Narrative metadata stamp (`interaction_truth`)
        ↓
Professional Publisher consumes facts as prose
```

| Layer | What it does |
|-------|----------------|
| Foundation service | Builds facts after natal facts. Does not write prose |
| `stamp_interaction_truth` | Copies `to_dict()` onto Narrative metadata |
| `interaction_copy` | Turns stamped facts into customer sentences. No calculation |
| Professional publisher | `sec-luck` required; Career / Finance / Relationship / Health / Recommendations / Conclusion overlay only |
| `sec-chart` | Unchanged. Must not show interaction overlays |

LuckEngine still owns period identity.

UsefulGodEngine still owns Useful God / Hỷ / Kỵ.

Narrative still owns prose.

Publisher still owns presentation.

---

## 4. Narrative consumption

Narrative may consume Interaction Facts. It must not calculate them.

Wiring:

1. `build_interpretation_foundation` attaches `interaction_truth`
2. `stamp_interaction_truth` copies facts onto payload metadata after `stamp_dayun_frame`
3. `luck_paragraphs_from_interaction` assembles Current Da Yun consultation from those facts
4. Domain overlays read the same stamped dict

Composer internals, Decision/State/Relationship bundles, and case-thesis generation were not redesigned.

B1-P0-001 luck assembly (thesis / career / risk / corrective prefixed with the decade name) is removed from `sec-luck`.

---

## 5. Professional Report changes

| Page | Behavior |
|------|----------|
| Đại vận hiện tại | Interaction Facts only. Honest empty overlap. Honest missing. Never natal thesis paste |
| Sự nghiệp | Natal operating style kept. Period overlay prepended from overlap / empty-overlap |
| Tài chính · Quan hệ · Sức khỏe | Overlap overlay per area. Does not paste natal thesis as decade effect |
| Khuyến nghị | Now-only overlay from overlap, then existing recommendations |
| Kết luận | Period-true close from Interaction Facts when they exist |
| Lá số | No interaction overlay |

Removed luck-page patterns:

- “quan trọng vì đây là thập niên …” + thesis
- “Cơ hội chính trong …” + natal career implication
- “Áp lực chính trong …” + natal risk
- “Hướng vận hành nên giữ trong …” + natal corrective

Fallback when facts are not stamped: name the living decade and say interaction data is insufficient. Do not fill from executive natal luck markers.

---

## 6. Three case comparison

Differences come from published identity overlap, not rewritten wording.

| | Nguyễn Tiến Sơn | Lương Ngọc Huỳnh | Ngô Đặng Minh Tân |
|--|-----------------|------------------|-------------------|
| Period | Ất Tỵ 2022–2031 | Quý Mão 2021–2030 | Đinh Tỵ 2024–2033 |
| Stem / branch | Ất / Tỵ | Quý / Mão | Đinh / Tỵ |
| Hidden stems | Bính, Mậu, Canh | Ất | Bính, Mậu, Canh |
| Useful God | Thực Thần (role) | Đinh | Canh |
| Hỷ | Thực Thần, Thương Quan | Đinh, Bính, Ất | Canh, Tân, Nhâm |
| Kỵ | Tỷ Kiên, Kiếp Tài | Canh, Tân | Giáp, Ất |
| Helpful overlap | none | **Ất** via tàng can | **Canh** via tàng can |
| Pressure overlap | none | none | none |
| Empty overlap | **yes** | no | no |
| Status | available | available | available |
| Diagnostic | `empty_identity_overlap` | none | none |

Sơn: period tokens Ất / Tỵ / Bính / Mậu / Canh / Chính Tài do not equal role-type Useful God / Hỷ / Kỵ. Empty overlap is stated honestly. No inference that Ất “supports” Thực Thần.

Huỳnh: Mão tàng can **Ất** equals Hỷ **Ất**. That is the only helpful factor.

Tân: Tỵ tàng can **Canh** equals Useful God / Hỷ **Canh**. That is the only helpful factor.

Luck sections share the same sentence slots. They differ because period identity and overlap lists differ.

---

## 7. Files changed

Implementation:

- `engines/interpretation_engine/foundation/facts/interaction.py`
- `engines/interpretation_engine/foundation/builders/interaction_truth_builder.py`
- `engines/interpretation_engine/foundation/diagnostics.py`
- `engines/interpretation_engine/foundation/service.py`
- `engines/interpretation_engine/foundation/narrative/publish/current_dayun.py`
- `engines/interpretation_engine/foundation/narrative/publish/interaction_copy.py`
- `engines/interpretation_engine/foundation/narrative/publish/professional.py`
- `applications/api/services/narrative_result_truth.py`

Product check and artifacts:

- `knowledge/editorial_validation/b1_p0_003_product_test.py`
- `knowledge/editorial_validation/exports/b1_p0_003/_metrics.json`
- `knowledge/editorial_validation/exports/b1_p0_003/professional/BTE_CASE-0001_Production_E2E.pdf`
- `knowledge/editorial_validation/exports/b1_p0_003/professional/BTE_HUYNH_Production_E2E.pdf`
- `knowledge/editorial_validation/exports/b1_p0_003/professional/BTE_TAN_Production_E2E.pdf`

Tests were not modified.

Golden Dataset / snapshots / expected output were not modified.

---

## 8. Engine changes

**NONE** as analytical engines.

UsefulGodEngine ranking unchanged.

LuckEngine Da Yun calculation unchanged.

No clash / harm / punishment added.

No ten-cycle analysis.

No predictions.

Winners remain:

- Sơn: Thực Thần
- Huỳnh: Đinh
- Tân: Canh

Interpretation Foundation gained an Interaction Truth **builder** over existing facts. That is not a new engine.

---

## 9. Architecture changes

**NONE**

Ownership preserved:

| Object | Owner |
|--------|-------|
| Natal values | analytical engines |
| Period identity | LuckEngine |
| Relation facts | Interaction Truth |
| Prose | Narrative |
| Presentation | Publisher |

No Knowledge content change.

No composer bundle kinds added.

No Product Governance change.

---

## 10. Remaining truth gaps

These are out of scope for B1-P0-003 and are not filled by inference:

1. No relation inferred between a period stem and a role-type Useful God (Ất vs Thực Thần).
2. Pattern, Strength, Ten Gods, Shen Sha, Temperature, and Five Elements are copied as governors in the summary. They are not additional overlap sources in this implementation.
3. Clash / harm / punishment remain unused because they are not already published as interaction inputs for this contract.
4. Next cycle is identity only. It is not interpreted.
5. Liu Nian / Liu Yue / Liu Ri remain unused.
6. Interpretation luck facts still drop most DayunPeriod fields; Interaction Truth copies them from the shaped luck payload instead of expanding Luck Domain.

Empty overlap is a completed fact, not a remaining gap.

---

## 11. Final verdict

Interaction Truth is live between Natal Truth and Professional Report.

Professional `sec-luck` no longer repeats natal thesis.

When overlap exists, the report names the published identities that overlap.

When overlap is empty, the report says so.

Three-chart sections differ because of interaction facts.

**READY_FOR_ARTIFACT_REVIEW**

STOP.
