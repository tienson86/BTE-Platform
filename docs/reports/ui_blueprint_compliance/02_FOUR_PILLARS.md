# Tier 2 — Four Pillars — Blueprint V1.1 Compliance

**Status:** REVIEW ONLY — no code changes  
**Blueprint refs:** `docs/ui_blueprint/15_TIER2_FOUR_PILLARS.md` (if present), wireframes Four Pillars, `19_BLUEPRINT_V1_1_FINAL_FREEZE.md`, USER_READING_FLOW  
**UI sources:** `pillars.js`, `report_render.js`, `report.css`, `vi.json`  
**Illustration:** [`../ui_sprint02_four_pillars/preview/pillars_light.html`](../ui_sprint02_four_pillars/preview/pillars_light.html) · [`pillars_dark.html`](../ui_sprint02_four_pillars/preview/pillars_dark.html)

---

## Blueprint target

| Item | Requirement |
|------|-------------|
| Structure | Year · Month · Day · Hour columns |
| Rows | Stem, Branch, Hidden Stems, Ten Gods (and related chart rows as defined) |
| Grammar | Soft workspace table; missing → `--` |
| Forbidden | Duplicate day-master relation essay in matrix; expert prose blocks |

---

## Checklist by dimension

| Dimension | Verdict | Notes |
|-----------|---------|-------|
| Information Architecture | ⚠ | Core 4×N matrix OK; extra `DayMasterRelation` block outside matrix |
| Visual Hierarchy | ✓ | Column headers / row labels clear |
| Reading Flow | ✓ | Left→right pillars, top→bottom rows |
| Spacing | ✓ | Soft gaps; production tokens |
| Typography | ✓ | Stem/branch emphasis vs secondary rows |
| Component Hierarchy | ✓ | `buildPillarsWorkspace` owns Tier 2 |
| Binding | ✓ | Chart pillars from report model |
| Empty State | ⚠ | Uses Unavailable / VI text instead of `--` in some cells |
| Localization | ✓ | `report.pillars.*` keys |
| Visual Grammar | ✓ | Soft table, no neon |

---

## Findings

### T2-01 — Four-column pillar workspace
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `pillars.js` / `.bte-pillars` |
| **File** | `applications/customer_portal/static/js/report/pillars.js` |
| **Illustration** | Sprint02 preview matrix |
| **Evidence** | Year / Month / Day / Hour columns rendered as workspace |

### T2-02 — Core stem / branch / hidden / ten-god rows
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | Pillar row builders |
| **File** | `pillars.js` |
| **Illustration** | Sprint02 |
| **Evidence** | Primary chart rows present for each pillar |

### T2-03 — Extra DayMasterRelation block
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Major** |
| **Component** | DayMasterRelation / relation strip under or beside matrix |
| **File** | `pillars.js` (and any presenter wiring) |
| **Illustration** | Sprint02 — extra relation section |
| **Gap** | Blueprint treats Tier 2 as chart workspace; day-master relation narrative belongs in Analysis / Knowledge, not duplicated as Tier 2 chrome |
| **Fix recommendation** | Remove DayMasterRelation from Tier 2 surface; keep matrix-only |

### T2-04 — Missing cell display (`--` vs Unavailable)
| | |
|--|--|
| **Symbol** | ⚠ Chưa đúng Blueprint |
| **Severity** | **Minor** |
| **Component** | Cell empty renderer |
| **File** | `pillars.js` |
| **Illustration** | Sprint02 empty cells |
| **Gap** | Visual grammar / freeze: missing → `--`; UI often shows localized “Unavailable” prose |
| **Fix recommendation** | Map null/missing cell values to `--` only |

### T2-05 — No expert essay inside matrix
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | Matrix cells |
| **File** | `pillars.js` |
| **Illustration** | Sprint02 |
| **Evidence** | Cells stay token/short-label oriented |

### T2-06 — Soft visual grammar
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `.bte-pillars*` CSS |
| **File** | `applications/customer_portal/static/css/report.css` |
| **Illustration** | Sprint02 light/dark |
| **Evidence** | Soft radius/shadow; readable contrast |

---

## Tier 2 scorecard

| Area | Score |
|------|-------|
| Matrix IA | PASS |
| Extra chrome | FAIL (DayMasterRelation) |
| Empty grammar | WARN |
| **Tier verdict** | **PASS with WARN** |

**Needs fix:** T2-03 (Major), T2-04 (Minor).
