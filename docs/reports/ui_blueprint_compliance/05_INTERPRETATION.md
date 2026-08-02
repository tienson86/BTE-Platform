# Tier 5 — Interpretation — Blueprint V1.1 Compliance

**Status:** REVIEW ONLY — no code changes  
**Blueprint refs:** Interpretation / B.3 chapter map, `19_BLUEPRINT_V1_1_FINAL_FREEZE.md`  
**UI sources:** `interpretation_doc.js`, `report_render.js`, `report.css`, `vi.json`  
**Illustration:** [`../ui_sprint05_interpretation/preview/interpretation_light.html`](../ui_sprint05_interpretation/preview/interpretation_light.html) · [`interpretation_dark.html`](../ui_sprint05_interpretation/preview/interpretation_dark.html)

---

## Blueprint target

| Item | Requirement |
|------|-------------|
| Form | Document: TOC + chapters |
| Chapters | Align with B.3 title set / order |
| TOC | Show when chapters available (`availableCount` rule) |
| Dedup | Executive summary must not duplicate Chapter 1 body |

---

## Checklist by dimension

| Dimension | Verdict | Notes |
|-----------|---------|-------|
| Information Architecture | ⚠ | Chapter set/titles diverge from B.3; exec duplicates Ch.1 |
| Visual Hierarchy | ✓ | TOC + chapter headings clear |
| Reading Flow | ⚠ | Duplicate exec↔Ch.1 lengthens path |
| Spacing | ✓ | Doc spacing soft |
| Typography | ✓ | Document hierarchy |
| Component Hierarchy | ✓ | `interpretation_doc.js` |
| Binding | ⚠ | Chapters bound but set not B.3-faithful |
| Empty State | ✓ | Empty chapter handling |
| Localization | ✓ | VI chapter chrome |
| Visual Grammar | ✓ | Soft document, not card dump |

---

## Findings

### T5-01 — TOC + chapters document shell
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `interpretation_doc.js` TOC / chapter list |
| **File** | `applications/customer_portal/static/js/report/interpretation_doc.js` |
| **Illustration** | Sprint05 preview |
| **Evidence** | Interpretation renders as document with TOC |

### T5-02 — Chapter set vs B.3
| | |
|--|--|
| **Symbol** | ⚠ Chưa đúng Blueprint |
| **Severity** | **Major** |
| **Component** | Chapter catalog / titles |
| **File** | `interpretation_doc.js` |
| **Illustration** | Sprint05 TOC titles |
| **Gap** | Titles/order/count not fully aligned with Blueprint B.3 chapter map |
| **Fix recommendation** | Remap chapter IDs/titles to B.3; hide unavailable; do not invent extras |

### T5-03 — TOC always on
| | |
|--|--|
| **Symbol** | ⚠ Chưa đúng Blueprint |
| **Severity** | **Minor** |
| **Component** | TOC visibility |
| **File** | `interpretation_doc.js` |
| **Illustration** | Sprint05 with sparse chapters |
| **Gap** | TOC should gate on `availableCount` (or equivalent); currently always visible |
| **Fix recommendation** | Show TOC only when availableCount ≥ threshold (per freeze) |

### T5-04 — Executive summary duplicates Chapter 1
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Major** |
| **Component** | Exec blurb + Chapter 1 body |
| **File** | `interpretation_doc.js` |
| **Illustration** | Sprint05 — repeated opening content |
| **Gap** | Same narrative appears in exec strip and Ch.1 — violates reading-flow dedupe |
| **Fix recommendation** | Keep short exec teaser OR fold into Ch.1 only — not both full texts |

### T5-05 — Soft document visual grammar
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `.bte-interp*` |
| **File** | `report.css` |
| **Illustration** | Sprint05 light/dark |
| **Evidence** | Document feel; soft rules; readable measure |

---

## Tier 5 scorecard

| Area | Score |
|------|-------|
| Document shell | PASS |
| B.3 fidelity / dedupe | WARN–FAIL |
| **Tier verdict** | **WARN** |

**Needs fix:** T5-04, T5-02 (Major); T5-03 (Minor).
