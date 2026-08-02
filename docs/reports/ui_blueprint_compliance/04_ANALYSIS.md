# Tier 4 — Analysis — Blueprint V1.1 Compliance

**Status:** REVIEW ONLY — no code changes  
**Blueprint refs:** Analysis wireframe / Tier 4 docs, `19_BLUEPRINT_V1_1_FINAL_FREEZE.md`, USER_READING_FLOW  
**UI sources:** `analysis.js`, `report_render.js`, `report.css`, `vi.json`  
**Illustration:** [`../ui_sprint04_analysis/preview/analysis_light.html`](../ui_sprint04_analysis/preview/analysis_light.html) · [`analysis_dark.html`](../ui_sprint04_analysis/preview/analysis_dark.html)

---

## Blueprint target

| Item | Requirement |
|------|-------------|
| Blocks | Explainable analysis cards (primary four default-expanded as specified) |
| Grouping | Useful / Favorable / Unfavorable grouped; Relations as matrix/section |
| Content | No pattern-rules essay dumped into Priority·Knowledge |
| Forbidden | Extra Thân narrative block if not in Tier 4 IA; wrong default-expand |

---

## Checklist by dimension

| Dimension | Verdict | Notes |
|-----------|---------|-------|
| Information Architecture | ⚠ | Extra Thân block; Dụng/Hỷ/Kỵ + Relations split vs blueprint grouping |
| Visual Hierarchy | ⚠ | Default-expand not matching primary-four rule |
| Reading Flow | ⚠ | Essay-length Priority content breaks scan |
| Spacing | ✓ | Soft accordion / card gaps |
| Typography | ✓ | Title/body roles OK |
| Component Hierarchy | ✓ | `analysis.js` owns blocks |
| Binding | ⚠ | Priority/Knowledge may bind pattern-rules prose incorrectly |
| Empty State | ✓ | Collapsed empties with VI hints |
| Localization | ✓ | Mostly VI keys |
| Visual Grammar | ✓ | Soft explainable cards |

---

## Findings

### T4-01 — Explainable analysis blocks present
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `analysis.js` block cards |
| **File** | `applications/customer_portal/static/js/report/analysis.js` |
| **Illustration** | Sprint04 preview |
| **Evidence** | Tier 4 renders structured explainable sections |

### T4-02 — Extra Thân (Day Master) block
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Major** |
| **Component** | Thân / DayMaster analysis card |
| **File** | `analysis.js` |
| **Illustration** | Sprint04 — extra Thân section |
| **Gap** | Blueprint IA for Tier 4 does not place a standalone Thân essay here (or duplicates Tier 2/5) |
| **Fix recommendation** | Remove or relocate Thân narrative to Interpretation / Knowledge per B.3 map |

### T4-03 — Useful / Favorable / Unfavorable + Relations IA
| | |
|--|--|
| **Symbol** | ⚠ Chưa đúng Blueprint |
| **Severity** | **Major** |
| **Component** | Useful/Favorable/Unfavorable cards; Relations section |
| **File** | `analysis.js` |
| **Illustration** | Sprint04 split cards |
| **Gap** | Blueprint expects Useful grouped with clear Relations matrix; UI splits Dụng/Hỷ/Kỵ and Relations in a way that diverges from wireframe IA |
| **Fix recommendation** | Regroup Useful family; Relations as dedicated matrix/list per blueprint |

### T4-04 — Default-expand primary four
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Major** |
| **Component** | Accordion / expand state |
| **File** | `analysis.js` |
| **Illustration** | Sprint04 initial expand state |
| **Gap** | Wrong set expanded by default vs “primary four” rule |
| **Fix recommendation** | Default-expand only the blueprint primary four; collapse the rest |

### T4-05 — Priority essay from pattern rules
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Critical** |
| **Component** | Priority · Knowledge content binder |
| **File** | `analysis.js` (and any rule-text mapper) |
| **Illustration** | Sprint04 long Priority body |
| **Gap** | Pattern-rules essay dumped into Priority/Knowledge — violates Analysis explainable short-form + Knowledge tier boundaries |
| **Fix recommendation** | Stop injecting pattern-rules essay; bind short explainable bullets only; long form → Interpretation/Knowledge |

### T4-06 — Soft explainable visual grammar
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `.bte-analysis*` |
| **File** | `report.css` |
| **Illustration** | Sprint04 light/dark |
| **Evidence** | Soft cards, restrained expand UI |

---

## Tier 4 scorecard

| Area | Score |
|------|-------|
| Block presence | PASS |
| IA / expand / content | FAIL–WARN |
| **Tier verdict** | **WARN** |

**Needs fix:** T4-05 (Critical); T4-02, T4-03, T4-04 (Major).
