# Tier 3 — Metrics — Blueprint V1.1 Compliance

**Status:** REVIEW ONLY — no code changes  
**Blueprint refs:** `docs/ui_blueprint/15_TIER3_METRICS.md` / wireframes ChartBand, `19_BLUEPRINT_V1_1_FINAL_FREEZE.md`  
**UI sources:** `metrics.js`, `report_render.js`, `report.css`, `vi.json`  
**Illustration:** [`../ui_sprint03_metrics/preview/metrics_light.html`](../ui_sprint03_metrics/preview/metrics_light.html) · [`metrics_dark.html`](../ui_sprint03_metrics/preview/metrics_dark.html)

---

## Blueprint target

| Item | Requirement |
|------|-------------|
| Layout | Desktop **2×2 ChartBand**: Strength Gauge · Element Balance · Ten Gods · (supporting chart/summary as defined) |
| Order | Metrics → Gauge → Elements → TenGods (Sprint03 contract aligned with freeze) |
| Forbidden | Unbound summary grids; English raw payload chrome; dashboard clutter |

---

## Checklist by dimension

| Dimension | Verdict | Notes |
|-----------|---------|-------|
| Information Architecture | ✗ | Not true 2×2 ChartBand; SummaryMetricGrid present / unbound risk |
| Visual Hierarchy | ⚠ | Gauge competes with unbound summary tiles |
| Reading Flow | ⚠ | Extra summary strip before/around ChartBand breaks glance path |
| Spacing | ✓ | Soft section spacing OK |
| Typography | ⚠ | Some EN labels (“Score payload”) |
| Component Hierarchy | ⚠ | `metrics.js` + leftover summary grid |
| Binding | ✗ | SummaryMetricGrid often unbound / placeholder |
| Empty State | ⚠ | Mixed VI placeholders vs EN debug strings |
| Localization | ✗ | Residual English in metrics chrome |
| Visual Grammar | ✓ | Soft cards overall |

---

## Findings

### T3-01 — Metrics module exists (Gauge / Elements / TenGods)
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `metrics.js` ChartBand builders |
| **File** | `applications/customer_portal/static/js/report/metrics.js` |
| **Illustration** | Sprint03 preview charts |
| **Evidence** | Strength gauge, element balance, ten gods surfaces implemented |

### T3-02 — Desktop 2×2 ChartBand layout
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Critical** |
| **Component** | ChartBand layout container |
| **File** | `metrics.js`, `report.css` |
| **Illustration** | Sprint03 — stacked / non-2×2 arrangement |
| **Gap** | Blueprint wireframe: 2×2 chart band. Current UI does not preserve that desktop composition |
| **Fix recommendation** | CSS grid 2×2 for ≥lg breakpoints; single column only on mobile |

### T3-03 — Unbound SummaryMetricGrid
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Critical** |
| **Component** | SummaryMetricGrid / summary tiles |
| **File** | `metrics.js` / `report_render.js` |
| **Illustration** | Sprint03 empty or placeholder summary row |
| **Gap** | Extra summary grid not in ChartBand contract; frequently unbound → noise / empty chrome |
| **Fix recommendation** | Remove from Result Tier 3 or bind fully and demote to optional collapsed strip |

### T3-04 — English “Score payload” / debug chrome
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Major** |
| **Component** | Metrics empty / error labels |
| **File** | `metrics.js`, possibly presenters |
| **Illustration** | Sprint03 when score missing |
| **Gap** | Localization rule: customer VI; EN payload strings violate freeze |
| **Fix recommendation** | Replace with `report.metrics.*` VI keys; never surface raw EN payload labels |

### T3-05 — Reading order Metrics → Gauge → Elements → TenGods
| | |
|--|--|
| **Symbol** | ⚠ Chưa đúng Blueprint |
| **Severity** | **Minor** |
| **Component** | Section order in `metrics.js` |
| **File** | `metrics.js` |
| **Illustration** | Sprint03 DOM order |
| **Gap** | Order mostly intended but SummaryMetricGrid interrupts ChartBand sequence |
| **Fix recommendation** | Enforce single ChartBand order after removing summary grid |

### T3-06 — Soft visual grammar for charts
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | Gauge / element / ten-god cards |
| **File** | `report.css` |
| **Illustration** | Sprint03 light/dark |
| **Evidence** | Soft radius, restrained color — not neon dashboard |

---

## Tier 3 scorecard

| Area | Score |
|------|-------|
| Chart content | PASS (partial) |
| Layout fidelity | FAIL |
| Binding / i18n | FAIL |
| **Tier verdict** | **WARN / layout FAIL** |

**Needs fix:** T3-02, T3-03 (Critical); T3-04 (Major); T3-05 (Minor).
