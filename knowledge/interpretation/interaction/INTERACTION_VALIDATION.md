# Interaction Validation

Version: 1.0  
Status: SPECIFICATION  
Issue: B1-P0-002

This document defines how to tell real interaction from natal copy, duplicated thesis, and narrative filler.

It does not define test code.

---

## 1. Real interaction

A statement (or fact) is **real interaction** when all of the following are true:

1. It names the **current Da Yun** as the living period (already-published identity).
2. It names at least one **natal governor** with its real owner (Pattern, Strength, Useful God, Hỷ, Kỵ, or an optional natal domain actually used).
3. It records a **relation kind** from this spec: `identity_overlap`, `no_identity_overlap`, `natal_governor_in_force`, `supported_direction`, `restricted_direction`, `period_identity`, or `next_period_not_current`.
4. The relation is evidenced by **upstream field refs**, not by Narrative wording.
5. Removing the decade name would **change the claim** (the period side would disappear), or the claim is explicitly “no evidenced overlap”.
6. It does not reselect natal values.

Valid examples (facts, not required wording):

- Period stem `Đinh` overlaps natal Useful God `Đinh`.
- Period stem `Ất` has no identity overlap with natal Useful God `Thực Thần` or Hỷ/Kỵ lists.
- Natal Useful God `Thực Thần` remains in force; period overlap empty.
- Next cycle `Bính Ngọ` is published and is not current.

---

## 2. Copied natal truth

A statement is **copied natal truth** when:

1. The payload is a natal fact or natal explanation, and
2. The only period contribution is a prefix, suffix, or frame (“trong Ất Tỵ”, “Đại vận đang sống”), and
3. No overlap / empty-overlap fact is used, and
4. The sentence remains true, word for word, if the decade name is deleted.

Examples:

- “Trong Ất Tỵ, Dụng thần là Thực Thần, Hỷ là Thực Thần / Thương Quan, Kỵ là Tỷ Kiên / Kiếp Tài.”
- “Trong Quý Mão, thân vượng, cách Chính Tài, Dụng Đinh.”
- Any B1-P0-001 interaction paragraph that lists Pattern, Strength, Dụng, Hỷ, Kỵ and then restates natal reasoning.

Copied natal truth may appear on natal pages.

It must not be presented as Current Da Yun consultation.

---

## 3. Duplicated thesis

A statement is **duplicated thesis** when:

1. It reuses the case thesis title, short thesis, expanded thesis, career implication, primary risk, or corrective direction, and
2. It is placed in a current-period section, and
3. Interaction Facts are not the source of the claim.

Examples:

- “Ất Tỵ quan trọng vì đây là thập niên Người tự gánh phải giữ hướng đã luận: …”
- “Cơ hội chính trong Ất Tỵ:” + natal career implication
- “Áp lực chính trong Ất Tỵ:” + natal thesis risk
- “Hướng vận hành nên giữ trong Ất Tỵ:” + natal corrective

Those slots explain the **chart**.

They do not become true of the **decade** by insertion of the cycle name.

Duplicated thesis is the B1-P0-001R failure mode.

---

## 4. Narrative filler

A statement is **narrative filler** when it occupies a current-period slot but carries no Interaction Fact and no new natal fact.

Signs:

- Generic importance: “thập niên này cần luận”, “đây là giai đoạn quan trọng”
- Glossary: what Da Yun is, how ten cycles are counted, how luck is calculated
- Empty structure: seven paragraphs that only rename the same natal consultation
- Word-count padding copied from executive summary or warnings because they contain “vượng / thoát / tải”
- Next-cycle discussion that interprets the next decade instead of marking it not-current
- Recommendations that only say “giữ hướng đã chọn” with no evidenced overlap and no explicit empty-overlap fact

Filler can be fluent.

It is still not Interaction Truth.

---

## 5. Decision table

| Question | Yes | No |
|----------|-----|----|
| Does it name the current period identity? | Continue | Not a period claim |
| Does it name a natal governor or an explicit empty-overlap? | Continue | Filler or glossary |
| Is the claim evidenced by LuckEngine + natal engine fields? | Continue | Filler or invented analysis |
| If the decade name is removed, does the claim change or become an explicit empty-overlap? | Real interaction | Copied natal truth |
| Is the body a thesis / career / risk / corrective slot? | Duplicated thesis | Continue |
| Does it reselect Useful God, Strength, Pattern, or compute new wuxing? | Invalid — out of bounds | Continue |

---

## 6. Completeness checks

Interaction Truth is complete enough for Narrative to explain the current life period when:

- Period identity is present
- Useful God natal reference is present (or diagnostic `useful_god_missing`)
- Overlap comparison has been recorded, including empty overlap
- Supported and restricted directions are natal references with overlap qualifiers
- Evidence paths exist
- Status is not `MISSING`

Interaction Truth is **not** incomplete merely because helpful and pressure lists are empty.

Empty overlap + governors in force is a complete, modest truth.

---

## 7. Product acceptance (specification level)

A Professional Current Da Yun page passes this spec only if:

1. Every consulting paragraph traces to at least one Interaction Fact.
2. No paragraph is copied natal truth as defined in §2.
3. No paragraph is duplicated thesis as defined in §3.
4. No paragraph is filler as defined in §4.
5. Engine winners (Useful God, Pattern, Strength, Hỷ, Kỵ, current Da Yun label) are unchanged.
6. All ten cycles are not interpreted.
7. No new engine appears.

A page that is longer, warmer, or more “consulting” than a timestamp, but still fails §2–§4, is not Interaction Truth.

---

## 8. Three-chart illustration (identity only)

These rows are identity checks, not implementations.

| Chart | Natal Useful God | Current Da Yun | Real interaction must be able to say |
|-------|------------------|----------------|--------------------------------------|
| Nguyễn Tiến Sơn | Thực Thần (role) | Ất Tỵ 2022–2031 | Period identity + whether luck stem/branch/ten-god/hidden stems overlap Thực Thần / Hỷ / Kỵ identities. If none overlap, say so. Do not print Thực Thần (Kim) as period effect. |
| Lương Ngọc Huỳnh | Đinh (stem) | Quý Mão 2021–2030 | Period identity + whether luck identities overlap Đinh / Hỷ stems / Kỵ stems. Do not restamp Chính Tài · Thân vượng · Đinh as the decade. |
| Ngô Đặng Minh Tân | Canh (stem) | Đinh Tỵ 2024–2033 | Period identity + whether luck identities overlap Canh / Hỷ stems / Kỵ stems. Do not restamp Chính Ấn · Trung hòa · Canh as the decade. |

No algorithm is defined here for those overlap checks.

The requirement is that the overlap result **exist as a fact** before Narrative speaks.
