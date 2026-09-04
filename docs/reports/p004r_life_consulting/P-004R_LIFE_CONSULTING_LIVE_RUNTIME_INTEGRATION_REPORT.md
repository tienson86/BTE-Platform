# P-004R LIFE CONSULTING LIVE RUNTIME INTEGRATION REPORT

Status: **COMPLETE**

Date: 2026-09-04  
Case: CASE-0001 live Analyze → `/result`  
Surface: production Commercial Dashboard (`static/dist/result.js?v=P004R`)

---

## 1. Status

Life Consulting now renders on live `/result` after Overview and before Interpretation.

No new domain copy. No new astrology. Narrative meaning and Presentation contract unchanged.

---

## 2. Root cause

Two stacked integration failures. Not an adapter-empty CASE-0001.

**F — stale production bundle (primary)**  
P-004 existed in source and unit tests. Live `/result` loads `/static/dist/result.js`. That bundle had not been rebuilt after P-004. The HTML cache token was still `?v=UI17`. Customers therefore still saw the old grid: Overview → Interpretation → Action → evidence cards.

**B — mounting outside the visual grid (secondary)**  
Source mounted Life Consulting as a page sibling *before* the entire grid. Visual V2 reorders grid children so Overview is first. Even after a rebuild, Life would sit above the hero, outside the approved reading journey. P-004R places it inside the grid as a non-`data-card` full-width row with `order: 15` (Overview `10`, Interpretation `20`).

Not A (unmounted in source). Not C (ResultStore analysis was present once calendar G1-10C booted). Not E as a whole-section suppress: live CASE-0001 matches five domains.

---

## 3. Live payload audit

Captured from ResultStore after live POST Analyze for CASE-0001 (1987-01-21 04:30, male).

| Field | Live Analyze | P-004 fixture | Gap |
|-------|----------------|---------------|-----|
| gender | male | male | none |
| visible Ten Gods | Thất Sát, Kiếp Tài, Nhật Chủ, Thiên Ấn | same | none |
| hidden Ten Gods | Thiên Tài, Thất Sát, Thiên Ấn, Chính Ấn, Thương Quan, Kiếp Tài, Chính Quan, … | Thiên Tài, Chính Ấn only | live publishes full hidden set |
| pattern | Chính Ấn | Chính Ấn | none |
| strength | strong → Thân vượng | strong | none |
| useful god | **Hỏa · Đinh · Chính Quan** | Thủy · Nhâm · Thực Thần | **live Dụng is Chính Quan** |
| current luck | Ất Tỵ | Nhâm Ngọ (test-only) | live cycle name differs; both count as published current luck |
| five elements | status `EXCESS` | omitted | live status is technical; P-004 only trusts CÂN BẰNG / MẤT CÂN BẰNG NHẸ / LỆCH RÕ |
| temperature | Hàn | omitted | live has climate; health still binds from Pattern + Strength first |
| shensha | Thiên Ất, Hồng Loan, Thiên Đức, Nguyệt Đức | omitted | marriage still binds from gender + Tài; no new ShenSha copy |
| calendar | G1-10C | omitted in P-004 unit fixture | **required for ResultStore boot** |

Raw audit: `docs/reports/p004r_life_consulting/live_payload_audit.json`

---

## 4. Mounting repair

`LifeConsultingSection` is rendered from `DashboardGrid` after the frozen `DASHBOARD_CARDS` map. It is not a tenth card. Spans stay `[4, 8, 4, 4, 4, 6, 6, 12, 12]`.

Desktop visual order:

Overview (`order: 10`)  
↓  
Life Consulting (`order: 15`)  
↓  
Interpretation (`order: 20`)  
↓  
Action (`order: 21`)  
↓  
Evidence (`30+`)

Mobile: Life shares `order: 1` with Overview so it follows the hero, then Action remains `2` (UI-18 thumb-zone hierarchy preserved).

Cache token: `/static/dist/result.js?v=P004R`.

---

## 5. Adapter binding

Live path: `adaptLifeConsulting(analysis, { request })`.

Gender also reads Analyze request when identity omits it. Current luck also reads published `identity.luck.current_cycle_ganzhi`. No new profiles. No CASE-0001 hardcode.

Visual fixture is used only when `layoutMode === "visual"`.

---

## 6. Partial domain behavior

Live CASE-0001 rendered:

- Hôn nhân
- Sức khỏe
- Sự nghiệp
- Tài chính
- Nhà đất

**Con cái omitted.** Children lookup needs published Useful God / output tokens (Thực Thần / Thương Quan). Live Dụng is Chính Quan. The section still renders the five matched domains. One missing domain does not hide the section.

---

## 7. CASE-0001 live verification

POST Analyze → open `/result` → `[data-life-consulting]` present.

Marriage / Career / Finance cards match authored P-004 copy. No Thập Thần / Thần Sát in customer domain text.

---

## 8. Screenshots

`docs/reports/p004r_life_consulting/screenshots/`

- `01_live_full.png`
- `02_life_consulting_section.png`
- `03_marriage.png`
- `04_career.png`
- `05_finance.png`
- `06_mobile.png`

---

## 9. Tests

`npx vitest run tests/js/p004r_life_consulting_runtime.test.tsx tests/js/p004_life_consulting.test.tsx`

- P-004R: 7 passed (R1–R10)
- P-004: 5 passed

Related frozen-grid checks: UI-18 pass, UI-20 pass.

---

## 10. Bundle / runtime verification

`docs/reports/p004r_life_consulting/bundle_verify.json`

- `result.js` mtime changed after `npm run build:result`
- size 310029 bytes
- HTML script: `?v=P004R`

Live Playwright: Analyze CASE-0001, wait for `[data-life-consulting]`, capture six screenshots.

---

## 11. Known gaps

1. Live Useful God is Chính Quan, so Children stays omitted until a matching published output token exists. That is empty-policy, not a mount bug.
2. Five Elements live status `EXCESS` is not a customer-trusted balance label; health uses Pattern + Strength.
3. Hồng Loan is published live but P-004 did not author extra ShenSha marriage copy; marriage still binds from spouse-star tokens.
4. UI-07 T20 (`resultSource` empty vs current) remains the pre-existing calendar-gate / boot issue when stored payloads lack `calendar.calendar_rule_version = G1-10C`. Live Analyze includes G1-10C and boots.

---

## 12. Verdict

**PASS**

Live `/result` now shows Life Consulting in the production bundle, bound from ResultStore, with partial domains, after Overview and before Interpretation.

STOP.
