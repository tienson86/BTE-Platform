# UI Sprint 01 — Executive Hero (Tier 1) Handover

| Field | Value |
|-------|--------|
| **Sprint** | UI Sprint 01 — Tier 1 Executive Hero |
| **Blueprint** | V1.1 Final Freeze |
| **Date** | 2026-08-02 |
| **Scope** | Tier 1 only |

---

## 1. Screenshots

| Theme | File |
|-------|------|
| Desktop Light | [preview/screenshot_desktop_light.png](preview/screenshot_desktop_light.png) |
| Desktop Dark | [preview/screenshot_desktop_dark.png](preview/screenshot_desktop_dark.png) |
| HTML Light | [preview/hero_light.html](preview/hero_light.html) |
| HTML Dark | [preview/hero_dark.html](preview/hero_dark.html) |

Rebuild: `node applications/customer_portal/tests/js/ui_sprint01_hero_preview_build.js`

---

## 2. New / updated components (logical)

| Component | Location |
|-----------|----------|
| `ExecutiveHero` | `report_render.js` → `renderExecutive` (`data-component="ExecutiveHero"`) |
| `DayMasterDisplay` | `renderDayMasterDisplay` |
| `QualityVerdictCaption` | `renderQualityVerdictCaption` |
| `SummaryMetricRow` / `metricSlot` | Hero metrics with Unavailable honesty |
| `StrengthWeaknessPanel` | existing panels, Hero order |
| `FirstRecommendation` | `renderFirstRecommendation` |

---

## 3. Bindings used (from `18_BINDING_INDEX.md`)

| Slot | Source |
|------|--------|
| `hero.eyebrow` | i18n `report.executive_eyebrow` |
| `hero.day_master.*` | SummaryBuilder / bazi day master |
| `hero.quality_verdict` | grade → else score band (≥70/40–69/<40) → else confidence → Unavailable |
| `hero.quality_value` | grade \| total_score \| overall_score \| confidence |
| `hero.sentence` | composed DM / pattern / useful |
| `hero.than` | pattern than / strength aliases |
| `hero.dung_than` / `hy_than` / `ky_than` / `cach_cuc` | pattern / useful_god aliases |
| `hero.strengths` / `weaknesses` | score lists |
| `hero.first_recommendation` | `score.recommendations[0]` else advice/conclusion first sentence |

Missing slots → `report.unavailable` (never `null` / `undefined` / raw i18n keys).

---

## 4. Accessibility

- Hero metrics: `role="group"` + `aria-label`
- Quality verdict: `role="status"`
- First recommendation: `aside` + `aria-label`
- Tier heading remains `h2`; Day Master is the visual dominant value
- Unavailable copy is human language, not placeholders like `null`

---

## 5. Performance

- Presentation-only adapter in `report_model.js` (no extra API)
- Hero render is string templates; no new network calls
- CSS limited to Hero selectors in `report.css`

---

## 6. Backend / API / Engine / Database

| Layer | Changed? |
|-------|----------|
| Backend | **No** |
| API | **No** |
| Engine | **No** |
| Database | **No** |
| Navigation / Reading Flow / Tier 2–6 structure | **No** (Tier 2–6 renderers untouched aside from shared legacy `metric()` kept for Analysis) |

---

## 7. Files changed

- `applications/customer_portal/static/js/report/report_model.js`
- `applications/customer_portal/static/js/report/report_render.js`
- `applications/customer_portal/static/css/report.css`
- `applications/customer_portal/static/i18n/vi.json`
- `applications/customer_portal/tests/js/ui_sprint01_hero_preview_build.js` (preview builder)
- `docs/reports/ui_sprint01_executive_hero/**` (handover + screenshots)

---

## 8. Tests

`python -m pytest applications/customer_portal/tests -q` → **18 passed**

---

## 9. PASS check (Insight First)

Hero alone answers within first viewport:

1. Nhóm / chất lượng — QualityVerdictCaption  
2. Nhật Chủ — DayMasterDisplay  
3. Thân — metric  
4. Dụng — metric  
5. Hỷ — metric  
6. Kỵ — metric  
7. Cách cục — metric  
8. Đánh giá tổng quan — verdict + quality value  
9. Khuyến nghị đầu tiên — FirstRecommendation  

**Verdict:** Sprint 01 Hero **PASS** against Blueprint V1.1 Tier 1 contract.
