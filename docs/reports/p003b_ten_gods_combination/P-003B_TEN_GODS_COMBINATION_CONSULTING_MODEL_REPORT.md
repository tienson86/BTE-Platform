# P-003B TEN GODS COMBINATION CONSULTING MODEL REPORT

Status: **COMPLETE**

Date: 2026-09-04  
Case: CASE-0001  
Surface: Ten Gods card (`THẬP THẦN`)

---

## Status

Visible Ten Gods now interpret as one **business model**, not only as separate capability cards.

Runtime, Narrative Engine, Presentation contract, Ten Gods calculation, visible calculation, and hidden calculation were not modified.

Only customer combination consulting assets and Hero-card presentation of those assets changed.

---

## Architecture

```
Published visible Ten God names
        ↓
Catalog lookup (no astrology)
        ↓
Combination consulting card
        ↓
P-003 single-god capability cards
        ↓
Placement + Tàng Can support
```

One Ten God remains one capability (P-003 cards).

Multiple published visible Ten Gods become one value-creation model when a catalog asset exists.

Lookup rules:

1. Drop Nhật Chủ.
2. Order remaining names in traditional Ten God order.
3. Exact set match first.
4. Else longest catalog subset (pair or triple).
5. Omit the combination card when no asset exists.

No CASE-0001 identity hardcode. No stem-to-god mapping. No sentence-merging of single-god copy.

---

## Combination model

Catalog: `tenGodsCombinationAssets.ts`

Each asset answers:

- Core capability
- Commercial value (executive insight)
- Income model
- Career model
- Leadership model (label **Cầm việc**)
- Growth model
- Risk model
- Improvement direction

Titles are consulting language. They do not say “Thiên Tài + Thực Thần means…”.

Shipped patterns:

| Published visible set | Consulting title |
|---|---|
| Thực Thần · Thiên Tài | Đổi cửa lệch thành món thấy được |
| Thương Quan · Thiên Tài | Sửa khung bằng cửa không cố |
| Chính Quan · Chính Ấn | Chạy việc trong khung có nền |
| Kiếp Tài · Thất Sát | Mở cửa khi việc đang khó |
| Kiếp Tài · Thất Sát · Thiên Ấn | Bứt cửa hiểm bằng lối không theo khuôn |

Hidden names that are not already visible may attach one muted support line. They do not replace the visible model.

Layout on the card:

Combination  
↓  
Executive Insight  
↓  
Năng lực  
↓  
Thu nhập  
↓  
Công việc  
↓  
Cầm việc  
↓  
Tăng trưởng  
↓  
Rủi ro  
↓  
Hướng đi

---

## CASE-0001

Published visible Ten Gods (actual payload, not hardcoded):

- Năm: Thất Sát
- Tháng: Kiếp Tài
- Ngày: Nhật Chủ (axis, not a combination member)
- Giờ: Thiên Ấn

Bound combination members: Kiếp Tài · Thất Sát · Thiên Ấn

Title: **Bứt cửa hiểm bằng lối không theo khuôn**

Hidden support: Thiên Tài · Chính Ấn  
Muted line: nền ẩn keeps option and incubation; it is not the money model that is already running.

P-003 single-god cards remain for Thất Sát, Kiếp Tài, Thiên Ấn.

---

## Screenshots

Preview: `docs/reports/p003b_ten_gods_combination/preview.html`

| Frame | File |
|-------|------|
| Before | `docs/reports/p003b_ten_gods_combination/screenshots/case0001_before.png` |
| After | `docs/reports/p003b_ten_gods_combination/screenshots/case0001_after.png` |
| Before + After | `docs/reports/p003b_ten_gods_combination/screenshots/case0001_before_after.png` |
| After mobile | `docs/reports/p003b_ten_gods_combination/screenshots/case0001_after_mobile.png` |

The after preview keeps one P-003 capability card so the combination block stays readable. Production still renders all three single-god cards under the model.

---

## Tests

Passed:

- `tests/js/p003b_ten_gods_combination.test.tsx` (4)
- `tests/js/p003_ten_gods_commercial.test.tsx` (3)
- UI-07 T1–T19, semantic safety, visual fixture
- UI-15 information visualization
- UI-16 executive report

Verified:

- Adapter does not import engines
- Adapter does not calculate Ten Gods
- Presentation adapter unchanged
- Combination copy is consulting language, not “A + B means…”
- Nhật Chủ is not a combination member
- Hidden gods do not become an equal business-model card

Remaining:

- UI-07 T20 `resultSource` empty vs current is a pre-existing `resolveResultBoot` issue. Not caused by P-003B.

---

## Known gaps

1. Screenshots are CASE-0001 Ten Gods previews with production CSS, not a live `/result` session.
2. Catalog covers the requested pair/triple patterns, not every possible visible set. Unknown sets omit the combination card.
3. Hidden combination support is a muted line, not a full consulting grid.
4. Span remains 4/12. Combination plus three capability cards makes the module tall.
5. Catalog is presentation-layer copy. Knowledge JSON and Narrative Engine were not edited.

---

## Verdict

**PASS.** Published visible Ten Gods now explain one value-creation model: capability, income, career, how the person cầm việc, growth, risk, and next step. Calculation, Runtime, Narrative, and Presentation contract are unchanged.

STOP.
