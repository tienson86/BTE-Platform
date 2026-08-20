# G2-02 — Visual acceptance

Date: 2026-08-20. Surface: `/result` Canonical Desktop V2.

Captures: `release/gate_02/screenshots/g2_02/` (HTML freeze of the live Result tree).

## Hierarchy freeze

**Primary:** Tứ trụ · Điểm thân · Cách cục · Dụng/Hỷ/Kỵ + Căn cứ chọn Dụng · Điều hậu  
**Secondary:** Phân bố Ngũ hành · Thập thần · Thần sát · Đại vận · Cung Phi compact  
**Narrative:** Interpretation / recommendations / report links — present, not competing with core facts.

## Case A–I

| ID | Expected | Result |
|----|----------|--------|
| A Sơn | Pillars Bính Dần… · Thân vượng · 0.87 · Chính Ấn · Dụng Hỏa · Đinh · Chính Quan · reason CHẾ · Hỷ insufficient · Điều hậu Hỏa separate | **PASS** (`A_son.html`) |
| B Tuyền | 0.66 · Kiếp Tài · Dụng Mộc · Ất · Chính Quan · CHẾ · Hỷ insufficient · Điều hậu Thủy separate · no Tòng Tài | **PASS** (`B_tuyen.html`) |
| C Dũng | 1.00 · Giá Sắc detected LEVEL-1 · Dụng Thủy · Nhâm · Thực Thần · reason Tiết/V1.0 · Hỷ insufficient · Điều hậu Hỏa separate | **PASS** (`C_dung.html`) |
| D Neutral Hỷ | Same Dũng; Hỷ = “Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng”; Hỷ ≠ Dụng | **PASS** (`D_hy_neutral.html`) |
| E Supported Hỷ | Đặng Thị Dung; Hỷ = Mộc · Ất · Tỷ Kiên | **PASS** (`E_hy_supported.html`) |
| F LEVEL-1 | “Cấu trúc đặc biệt được nhận diện: Giá Sắc”; no tuyệt đối / chuyên cách | **PASS** (`F_level1_special.html`) |
| G Empty | Empty gate + CTA `/analyze`; no mock fixture / no Dụng preview | **PASS** (`G_empty.html`) |
| H Version mismatch | Reanalyze notice; no stale Dụng cards; no `UsefulGodView@1.5` in body | **PASS** (`H_contract_mismatch.html`) |
| I History | Banner “Đang xem kết quả đã lưu…”; History identity only; current Tuyền Dụng not mixed in | **PASS** (`I_history.html`) |

## Layout / responsive / print

| Check | Result |
|-------|--------|
| Cards use `rp-card--auto`; reason / Hỷ / Điều hậu / pillars `overflow: visible` | PASS |
| Desktop content max-width 1600; tokens 1366 / 1600 / 1920 | PASS (`canonical_desktop_viewports.test.ts`) |
| Breakpoints already in Result CSS: `<1440` / `<1024` / `<640` — no mobile redesign | PASS |
| `@media print` hides chrome, keeps critical cards unclipped | PASS (CSS freeze; PDF engine is G2-04) |
| Long Vietnamese reason (Dũng / Tuyền / Dung) wraps, no table clip | PASS in HTML tree |

## Language / leak

| Check | Result |
|-------|--------|
| Nam / Nữ; Thân vượng / nhược / cân bằng; no male/female in body | PASS |
| Điểm thân = `strength.strength_score` (e.g. `Thân vượng · 1.00`), not Score 45 / 51.25 / D+ | PASS |
| Phân bố Ngũ hành + structural disclaimer; no Mạnh/Yếu | PASS |
| No rule IDs / `str_` / `pat_` / contract id in customer body | PASS |
| Analysis id only in technical expand / DOM metadata | PASS |
| Production empty is not fixture preview | PASS |

## Accessibility baseline

| Check | Result |
|-------|--------|
| Semantic headings on cards (`h2` via `ResultCardShell`) | PASS |
| Empty/error CTA labeled; header icon buttons have `aria-label` | PASS |
| History banner `role="status"` | PASS |
| Meaning not color-only (labels + values on Dụng/Hỷ/Kỵ and elements) | PASS |
| No full a11y redesign in this gate | N/A (baseline only) |
