# Tier 1 — Executive Hero — Blueprint V1.1 Compliance

**Status:** REVIEW ONLY — no code changes  
**Blueprint refs:** `docs/ui_blueprint/15_TIER1_EXECUTIVE_HERO.md`, `16_WIREFRAMES.md` §1, `19_BLUEPRINT_V1_1_FINAL_FREEZE.md`, `USER_READING_FLOW.md`  
**UI sources:** `report_render.js`, `report_model.js`, `report.css`, `vi.json`  
**Illustration:** [`../ui_sprint01_executive_hero/preview/hero_light.html`](../ui_sprint01_executive_hero/preview/hero_light.html) · [`hero_dark.html`](../ui_sprint01_executive_hero/preview/hero_dark.html)

---

## Blueprint target

| Region | Requirement |
|--------|-------------|
| R1 Identity | Title · Gender · Date · Place |
| R2 Verdict | QualityVerdict primary (≤2 lines) |
| R3 Metrics | Strength · Useful · Favorable · Unfavorable · Pattern · Confidence — glance row |
| R4 Action | FirstRecommendation (≤2 lines) **above the fold** |
| Forbidden | Long essay, expert dump, expandable body |

---

## Checklist by dimension

| Dimension | Verdict | Notes |
|-----------|---------|-------|
| Information Architecture | ⚠ | Regions present; R3 uses 2×3 metric tiles + optional Secondaries; not exact R1→R4 wireframe |
| Visual Hierarchy | ✓ | Verdict strongest; recommendation secondary; metrics tertiary |
| Reading Flow | ⚠ | FirstRecommendation often below fold on typical laptop heights |
| Spacing | ✓ | `.bte-hero` / `.bte-hero__*` tokens aligned with production CSS |
| Typography | ✓ | Title/verdict/body roles distinct |
| Component Hierarchy | ✓ | `buildHero` → Identity → Verdict → Metrics → Recommendation |
| Binding | ✓ | `quality_verdict` / `first_recommendation` via `report_model` with safe fallbacks |
| Empty State | ✓ | Missing fields → short VI placeholders; no blank crash |
| Localization | ✓ | Keys under `report.hero.*` / `report.quality.*` in `vi.json` |
| Visual Grammar | ✓ | Soft card, soft radius, soft shadow — not glass/neon |

---

## Findings

### T1-01 — QualityVerdict present and primary
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `buildHero` / `.bte-hero__verdict` |
| **File** | `applications/customer_portal/static/js/report/report_render.js` |
| **Illustration** | Sprint01 preview — verdict block under identity |
| **Evidence** | Maps `quality_verdict` (or derived) into short VI text; visual weight above metrics |

### T1-02 — FirstRecommendation present
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `.bte-hero__recommendation` |
| **File** | `report_render.js`, `report_model.js` |
| **Illustration** | Sprint01 preview — recommendation card |
| **Evidence** | Bound from `first_recommendation` / safe fallback; ≤2-line intent preserved in copy rules |

### T1-03 — FirstRecommendation above the fold
| | |
|--|--|
| **Symbol** | ⚠ Chưa đúng Blueprint |
| **Severity** | **Major** |
| **Component** | Full `.bte-hero` stack |
| **File** | `report.css` (hero layout), `report_render.js` |
| **Illustration** | `hero_light.html` — recommendation sits after metric grid |
| **Gap** | Blueprint / USER_READING_FLOW: R4 action in first viewport. Current order + metric grid height push recommendation below fold on ~768–900px viewports |
| **Fix recommendation** | Compact R3 to single glance row; keep R4 immediately under verdict or in a two-column hero (verdict+action | metrics) |

### T1-04 — Metric glance row (1×6 vs 2×3)
| | |
|--|--|
| **Symbol** | ⚠ Chưa đúng Blueprint |
| **Severity** | **Minor** |
| **Component** | `.bte-hero__metrics` |
| **File** | `report_render.js`, `report.css` |
| **Illustration** | Sprint01 — 2×3 tile grid |
| **Gap** | Wireframe §1 shows one horizontal glance strip; UI uses wrapped 2×3 cards |
| **Fix recommendation** | Desktop: single-row compact chips; keep wrap only on narrow mobile |

### T1-05 — No long essay / expert dump in Hero
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | Hero only |
| **File** | `report_render.js` |
| **Illustration** | Sprint01 |
| **Evidence** | No expandable expert body inside Tier 1 |

### T1-06 — Identity completeness
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `.bte-hero__identity` |
| **File** | `report_render.js` |
| **Illustration** | Sprint01 header row |
| **Evidence** | Title, gender, date, place (when payload provides) |

### T1-07 — Secondary metrics / extra chrome
| | |
|--|--|
| **Symbol** | ⚠ Chưa đúng Blueprint |
| **Severity** | **Minor** |
| **Component** | Optional secondaries under hero metrics |
| **File** | `report_render.js` |
| **Illustration** | Sprint01 when secondaries render |
| **Gap** | Blueprint R3 lists six primary glances; extra secondary chips increase height and compete with R4 |
| **Fix recommendation** | Hide secondaries from Hero; defer to Tier 3 |

---

## Tier 1 scorecard

| Area | Score |
|------|-------|
| Required content present | PASS |
| Hierarchy / grammar | PASS |
| Fold / layout fidelity | WARN |
| **Tier verdict** | **PASS with WARN** |

**Needs fix before UI sprint:** T1-03 (Major), T1-04 / T1-07 (Minor).
