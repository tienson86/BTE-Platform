# S00 — Context Header Review Package

| Item | Value |
|------|-------|
| Section | **S00 Context Header** |
| Spec | `PORTAL_SCREEN_SPECIFICATIONS.md` (S00) |
| IA | Freeze v1.1 APPROVED |
| Spec Freeze | APPROVED |
| Status | **AWAITING PRODUCT OWNER REVIEW** |
| Scope | S00 only — **no S01** |

---

## Screenshots

Path: `knowledge/ui_reference/migration_report/screenshots/s00_context/`

| # | File | Viewport |
|---|------|----------|
| 1 | `01_desktop_full.png` | Desktop 1440×900 — Result page with S00 first |
| 2 | `02_desktop_zoom_s00.png` | Desktop zoom — S00 alone (`?page=s00`) |
| 3 | `03_tablet.png` | Tablet 768×1024 |
| 4 | `04_mobile.png` | Mobile 390×844 |

Preview: `http://127.0.0.1:5177/?page=bazi` · `?page=s00`

---

## Design Rationale

1. **Context strip, not Hero**  
   Low visual weight: compact padding, section surface, no large stem, no Decision Support. Confirms “đúng hồ sơ / đúng phiên bản” in ≤ 3s.

2. **Fields per Spec + PO GOAL**  
   Hồ sơ · Mã lá số · Giới tính · Ngày giờ sinh · Phiên bản phân tích · Thời điểm phân tích · Trạng thái.  
   Optional: Avatar initials + light link “Chi tiết hồ sơ” → `#tong-quan`.

3. **Explicit exclusions**  
   S00 **không** chứa Nhật Chủ, Dụng/Hỷ/Kỵ, Thập Thần, Luận giải, Tứ Trụ.

4. **Reading order**  
   S00 renders first (`#ngu-canh`), before legacy Executive (pending S01) and Overview.

5. **Responsive**  
   Desktop: one horizontal strip. Tablet: wrap + status row. Mobile: stack 2–3 line groups — does not dominate the viewport.

6. **Design System only**  
   Avatar, Badge, BaseText, existing tokens — no new theme.

---

## Completion Report

### Files changed

| File | Change |
|------|--------|
| `applications/customer_portal/src/screens/bazi/ContextHeader.tsx` | **New** — S00 component |
| `applications/customer_portal/src/screens/bazi/BaZiResultScreen.tsx` | Mount S00 first |
| `applications/customer_portal/src/screens/bazi/mockData.ts` | Labels + `analyzedAt` |
| `applications/customer_portal/src/screens/bazi/index.ts` | Export ContextHeader |
| `applications/customer_portal/src/adapters/baziResultAdapter.ts` | Map `analyzedAt` |
| `applications/customer_portal/src/layouts/Navigation/navItems.ts` | TOC “Ngữ cảnh” |
| `applications/customer_portal/src/styles/bazi-result.css` | S00 strip styles |
| `knowledge/release_review/review_01/preview/main.tsx` | `?page=s00` zoom harness |
| `knowledge/ui_reference/migration_report/screenshots/s00_context/*` | Review shots |
| `knowledge/ui_reference/UI_CHANGELOG.md` | UI-015 entry |

### Build / Tests

| Check | Result |
|-------|--------|
| `npm run build` (`tsc --noEmit`) | **PASS** |
| `npm test` (vitest) | **PASS** |
| TypeScript | **PASS** |

### Remaining failures

None in customer_portal module tests.

### Out of scope (honored)

- S01 Identity & Decision Panel
- S02–S08 redesign
- Learning Panel
- Integration / API / Engine
- Theme / Component Library expansion

---

## Acceptance Checklist (Spec S00)

- [x] Renders before S01 / Executive in DOM order
- [x] Profile confirmation without Hero weight
- [x] Not confused with Primary Nav
- [x] chartId + status visible on Desktop strip
- [x] No Dụng/Hỷ/Kỵ, Thập Thần, Luận giải, Tứ Trụ in S00

---

## STOP

```
S00 complete → chờ Product Owner Review
Không triển khai S01
```
