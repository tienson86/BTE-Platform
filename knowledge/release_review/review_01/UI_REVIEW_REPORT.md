# Release Review 01

**Product:** BTE Platform V1.0  
**Scope:** Sprint 01 UI Acceptance (WP01–WP09 / Wave 2–3)  
**Date:** 2026-08-05  
**Mode:** Product UI review (not code review)  
**Frontend canonical:** `applications/customer_portal/` (ADR-001)

---

## Build

**PASS**

- `applications/customer_portal` → `npm run build` (`tsc --noEmit`) exit 0
- Vitest suite last known: **116 passed** (Wave 3 included)
- Runtime started for review:
  - FastAPI Portal: `http://127.0.0.1:8081` (Jinja production shell)
  - Wave UI preview (review-only harness): `http://127.0.0.1:5177`  
    Path: `knowledge/release_review/review_01/preview/`  
    *(Harness phục vụ chụp screenshot Wave 2/3 React — **không** phải thay đổi product code trong `applications/customer_portal`.)*

---

## Screens Captured

Tổng: **36** PNG trong `screenshots/{desktop,tablet,mobile}/`

### Wave UI (React — Dashboard / BaZi Result / Shell patterns)

| Screen | Desktop | Tablet | Mobile |
|--------|---------|--------|--------|
| Dashboard full | `wave_01_dashboard_full.png` | ✓ | ✓ |
| BaZi Result full | `wave_02_bazi_full.png` | ✓ | ✓ |
| BaZi Loading | `wave_03_bazi_loading.png` | ✓ | ✓ |
| BaZi Empty | `wave_04_bazi_empty.png` | ✓ | ✓ |
| BaZi Error | `wave_05_bazi_error.png` | ✓ | ✓ |
| Patterns (Empty / Skeleton / Toast / Tooltip / Dialog) | `wave_06_patterns.png` | ✓ | ✓ |
| Drawer | `wave_07_drawer.png` | ✓ | ✓ |
| Auth layout | `wave_08_auth_layout.png` | ✓ | ✓ |

### Runtime production (Jinja FastAPI — đang được serve thật)

| Screen | Desktop | Tablet | Mobile |
|--------|---------|--------|--------|
| Dashboard | `runtime_jinja_dashboard.png` | ✓ | ✓ |
| Result | `runtime_jinja_result.png` | ✓ | ✓ |
| Analyze | `runtime_jinja_analyze.png` | ✓ | ✓ |
| Login | `runtime_jinja_login.png` | ✓ | ✓ |

### Viewport sizes used

- Desktop: 1440 × 2600  
- Tablet: 834 × 2600  
- Mobile: 390 × 2800  

---

## UI Quality

### Typography

- Hierarchy rõ trên Dashboard / BaZi (page title → section → body → caption).
- Font sans thống nhất; không thấy font clash giữa shell và card.

### Spacing / White space

- Khoảng cách section/card nhìn đồng đều trên desktop.
- Mobile: padding ngang khá rộng; nội dung hẹp hơn mong đợi trên BaZi (nhiều white space 2 bên).

### Alignment / Card consistency

- Card radius / border / nền surface nhìn nhất quán.
- Dashboard stats 4 cột cân trên desktop; stack ổn trên mobile.
- BaZi split row (Ngũ Hành | Strength): **chiều cao 2 card không đồng đều**.

### Color consistency

- Primary Emerald dùng cho CTA chính, active nav, accent border Day pillar — đúng hướng Sprint.
- **Bell notification màu vàng/gold** lệch palette Emerald/Slate.
- Jinja runtime vẫn dùng **accent xanh dương** — khác hẳn Wave React (2 visual systems).

### Visual hierarchy / Readability

- Welcome + primary CTA “Lập Lá Số Mới” nổi bật đúng hướng.
- Disabled Quick Actions trên BaZi Header: nhìn giống secondary button bình thường → khó nhận biết disabled.
- Status badge “Mock” trên Statistics lộ rõ (đúng ADR-006 nhưng ảnh hưởng cảm nhận production).

### Hover / Disabled / Loading

- Loading skeletons Wave 3: đầy đủ các section (Header / Pillars / Elements / Strength / Ten Gods) — tốt.
- Empty / Error gates có mặt.
- Hover pillar / tooltip: có component; screenshot static không thể chứng minh hover — cần PO verify tay.

### Responsive

- Desktop / Tablet / Mobile đều capture được.
- Không thấy horizontal scroll rõ trong các ảnh Wave.
- Mobile BaZi: Tứ Trụ xếp dọc đúng; trang rất dài.
- Mobile Dashboard: status text trong Recent Analyses có dấu hiệu **bị cắt** (“đa…”).

### Accessibility

- Landmarks header/sidebar/footer có trên Wave shell.
- Aria labels trên section cards.
- Focus ring / keyboard: chưa verify bằng tay trong review này → ghi TODO cho PO.

### Icon consistency

- Header dùng emoji/icon text (🔔 / ☾ / ☰) — chưa đồng bộ icon system.
- Mobile user chip hiện “C” thay vì tên đầy đủ — khác desktop.

---

## Issues Found

**UI-001**  
Runtime FastAPI (Jinja `:8081`) và Wave React UI (preview `:5177`) là **hai giao diện khác nhau**. Product Owner đang review Wave UI qua harness; user production vẫn thấy Jinja cho đến khi Integration.

**UI-002**  
Search header có nút primary “Tìm” quá nặng cho chức năng placeholder (chưa search thật).

**UI-003**  
Icon thông báo (bell) màu vàng/gold không khớp Design System Emerald.

**UI-004**  
BaZi Header lặp title với `PageWrapper` (breadcrumb + H1 + title trong card) → hierarchy hơi dư.

**UI-005**  
Quick Actions BaZi (PDF / In / Chia sẻ / Phân tích lại) disabled nhưng visual gần như secondary enabled → khó nhận biết trạng thái disabled.

**UI-006**  
Card Ngũ Hành và Strength cạnh nhau trên desktop: **đáy không thẳng hàng** (chiều cao không đồng bộ).

**UI-007**  
Strength Card đã có border accent nhưng vẫn chưa “nổi bật hơn hẳn” so với các card khác (theo tiêu chí WP09).

**UI-008**  
Nạp Âm / Trường Sinh vẫn hiện chữ “(placeholder)” trong UI production-facing mock.

**UI-009**  
Statistics Dashboard hiện nhãn “Mock” trực tiếp trên card.

**UI-010**  
Mobile Recent Analyses: text trạng thái có nguy cơ **overflow/clip**.

**UI-011**  
Mobile header user control không giữ cùng pattern desktop (tên đầy đủ → chip “C”); thiếu Theme toggle rõ trên mobile capture.

**UI-012**  
Iconography chưa thống nhất (emoji / chữ / badge) — chưa có icon set chuẩn.

**UI-013**  
Five Elements ScoreBar hiển thị dạng `value/100` cạnh % legend → có thể gây nhầm “điểm” vs “phần trăm”.

**UI-014**  
Dialog gallery mở overlay che phần patterns phía sau; Toast/Tooltip khó review đồng thời trên cùng một frame.

**UI-015**  
Jinja Dashboard (runtime) còn skeleton/empty và palette xanh dương — lệch hoàn toàn với Wave Design System đã khóa.

---

## Suggestions

1. **Ưu tiên Integration (TASK_003):** mount Wave React (`DashboardScreen`, `BaZiResultScreen`) vào runtime portal — nếu không, PO review Wave UI không phản ánh production.
2. Polish Wave 4 (WP10+): disabled styles rõ hơn; cân chiều cao split cards; giảm lặp title; ẩn “(placeholder)” hoặc thay copy thân thiện hơn.
3. Thống nhất icon + notification color theo token.
4. Mobile: kiểm tra overflow Recent Analyses / status badges; rút gọn header actions.
5. Giữ mock data nhưng cân nhắc badge “Demo data” thay vì “Mock” trên từng stat.

---

## Ready For Polish

**YES — có điều kiện**

- Wave UI (Design System + Layout + Dashboard + BaZi Result) đủ để PO review visual/hierarchy/responsive.
- **Chưa Ready for Production release** cho đến khi:
  - Wave UI được gắn vào runtime (`:8081`), và
  - Các issue P0 UI-001 / UI-005 / UI-010 được xử lý trong polish/integration.

---

## Notes

- Không sửa product code trong review này (đúng STOP).
- Screenshot Wave lấy từ review harness vì `customer_portal` React package **không có** `npm run dev` / Vite app — chỉ là library + FastAPI Jinja.
- Preview harness nằm tại `knowledge/release_review/review_01/preview/` (phục vụ Acceptance Review, không phải feature mới của product).
- Không triển khai WP10 / Wave 4 / Integration trong review này.
- Chờ Product Owner review screenshots + issues trước khi mở bước tiếp theo.

### How PO can re-open preview

```bash
# Terminal 1 — production-like Jinja portal
python -m uvicorn applications.customer_portal.app:app --host 127.0.0.1 --port 8081

# Terminal 2 — Wave UI review preview
cd knowledge/release_review/review_01/preview
npm install
npm run dev
# open http://127.0.0.1:5177/?page=dashboard
# pages: dashboard | bazi | bazi-loading | bazi-empty | bazi-error | patterns | drawer | auth
```
