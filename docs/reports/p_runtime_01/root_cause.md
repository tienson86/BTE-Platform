# P-RUNTIME-01 root cause

Product Tickets P-001 → P-004 passed unit tests and preview.html because those paths imported the new adapters/components directly.

Live `http://localhost:8081/result` did not show the same surfaces for four independent reasons. None of them were astrology or Narrative meaning defects.

## 1. BUNDLE + CACHE (P-001, P-003, P-003B, P-004)

Classification: **BUNDLE**, **CACHE**

Production `/result` is `result_desktop.html` → `/static/dist/result.js`.

Vite output is gitignored. Preview tickets never required a production rebuild + cache-bust.

`result_desktop.html` kept `?v=P004R` after later source edits. The browser could keep the old module even when `static/dist/result.js` on disk was newer.

`result.css` had **no** cache token at all.

Repair: rebuild `npm run build:result` and bump both assets to `?v=PRUNTIME01`.

Post-repair `result.js` contains `data-overview-section`, `data-tg-commercial`, `data-tg-combination`, `data-life-consulting`.

## 2. COMPONENT MOUNT (P-002)

Classification: **COMPONENT MOUNT**

Approved Cân Xương location is Identity Header Region C (`IdentityFoundation`).

`CommercialDashboardPage` still mounted `CanXuongDetail` after the grid. Desktop customers saw a second "Cân Xương Đoán Mệnh" block at the bottom. Header already had the summary, plus an "Xem chi tiết" jump to `#sec-can-xuong` on that bottom block.

Tests/previews that only asserted the header, or hid `.bte-id__cx-detail` on mobile, did not catch the desktop duplicate.

Repair: keep one `#sec-can-xuong` on the header region; remove the page-bottom `CanXuongDetail` mount.

## 3. CSS ORDER (reachability, not absence)

Classification: **CSS ORDER**

P-003 / P-003B live inside the Ten Gods card. Visual V2 previously used `order: 32` (after Bát Tự / Ngũ Hành). The section existed after a long scroll, so a first-viewport audit looked like "not live".

P-004 Life Consulting was already mounted in `DashboardGrid` at `order: 15`, but a stale bundle made it absent on the real page.

Repair: keep Life at `order: 15` (after Overview). Move Ten Gods to `order: 22` (after Action Plan, before Bát Tự) so commercial + combination are customer-reachable without changing frozen card `data-span`.

## 4. FIXTURE / LIVE SHAPE (not a silent engine repair)

Classification: **FIXTURE/LIVE SHAPE**

P-001 / P-004 fixtures used `useful_display: Thủy · Nhâm · Thực Thần`.

Live CASE-0001 Analyze publishes `useful_display: Hỏa · Đinh · Chính Quan`.

Hỷ is published as the incomplete sentence `Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng`. P-001 correctly omits Hỷ only and still shows Dụng and Kỵ.

P-004 children (`Con cái`) requires useful/output tokens Thực Thần / Thương Quan. Live Dụng is Chính Quan, so children is omitted independently. Five other domains still render.

This is lookup against published fields, not a missing mount.

## Not the cause

- ROUTING of `/result` was already `CommercialDashboardPage` via `resultApp.tsx` when pathname is `/result` and surface is production.
- RESULTSTORE already saved `bte_last_result` from `POST /api/v1/analyze`. Fresh CASE-0001 has `calendar.calendar_rule_version = G1-10C` and UsefulGodView@1.5, so the calendar/contract gates did not drop the payload.
- ADAPTERS for P-001/P-003/P-003B/P-004 were already wired on the production page. They were not preview-only once the bundle included them.
- No astrology / Narrative / combination-knowledge / Life copy changes were required.
