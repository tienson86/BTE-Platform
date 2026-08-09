# PX-2 — Result Data Binding & Component Specification

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2 · Result Data Binding & Component Specification  
Owner: BTE Product  
Scope: **Specification only — no implementation**

Depends on: PX-1 Result Experience Blueprint V2 · CanonicalReportResult (RX-1) · CanonicalReportLayout (RE-2) · CanonicalReportArtifact (RE-3, metadata only)

---

## 1. Purpose

PX-2 is the canonical data-binding layer between Report and Portal UI.

It establishes:

- UI Contract  
- Portal Data Model  
- Presentation Adapter  
- Component API / state / events  
- Field catalog and 1:1 mappings  

No React. No CSS. No Tailwind. No Portal code. No engine changes.

---

## 2. Allowed inputs

```
CanonicalReportResult
        ↓
CanonicalReportLayout          (via result.layout_result)
        ↓
CanonicalReportArtifact        (metadata only)
```

UI consumes **Report only**.

Forbidden inputs:

- Engines  
- Pipelines (as runtime imports)  
- Packages  
- Knowledge Units directly  
- Analysis / Decision / Luck / Interpretation types  

---

## 3. Dependency chain

```
PX-1 Experience Blueprint
        ↓
PX-2 UI Contract + Binding     ← this pack
        ↓
Future Portal Adapter implementation (not this sprint)
        ↓
React Components (UI Contract only)
```

Foundation, Design System tokens, and Report pipeline source remain frozen. PX-2 does not edit them.

---

## 4. Reading order

| Order | File | Role |
|------:|------|------|
| 0 | `README.md` | This index |
| 1 | `RESULT_DATA_BINDING.md` | Binding laws |
| 2 | `UI_CONTRACT.md` | Official Portal contract |
| 3 | `PORTAL_DATA_MODEL.md` | Shape React may see |
| 4 | `PRESENTATION_ADAPTER.md` | Adapter duties |
| 5 | `REPORT_TO_UI_MAPPING.md` | Report → UI |
| 6 | `FIELD_CATALOG.md` | Every visible field |
| 7 | `COMPONENT_API.md` | Props / events / slots |
| 8 | `COMPONENT_PROPERTY_GUIDE.md` | Prop rules |
| 9 | `COMPONENT_EVENT_MODEL.md` | Events |
| 10 | `COMPONENT_STATE_MODEL.md` | Component states |
| 11 | `COMPONENT_LIFECYCLE.md` | Receive → dispose |
| 12 | `EXPANSION_STATE_MODEL.md` | Collapse / expand |
| 13 | `SECTION_VISIBILITY_RULES.md` | Show / hide / collapse |
| 14 | `RENDERING_PRIORITY.md` | Bind/render order |
| 15 | `CTA_SPECIFICATION.md` | Primary / secondary / tertiary |
| 16 | `LOADING_STRATEGY.md` | Loading |
| 17 | `EMPTY_STATE_STRATEGY.md` | Empty |
| 18 | `ERROR_STATE_STRATEGY.md` | Error |
| 19 | `LANGUAGE_BINDING.md` | Content vs chrome |
| 20 | `I18N_GUIDE.md` | Vietnamese keys |
| 21 | `UI_TOKEN_CATALOG.md` | Frozen token roles |
| 22 | `UI_REVIEW_CHECKLIST.md` | Future review |
| 23 | `PX2_SUMMARY.md` | Sprint close |
| — | `mapping/` | Per-section maps |
| — | `states/` | Page / component / nav machines |
| — | `documentation/` | Philosophy |

---

## 5. Frozen surfaces

| Surface | Rule |
|---------|------|
| Portal / React / CSS / Tailwind | Do not modify |
| Engines / pipelines / packages / APIs | Do not modify |
| Foundation / Design System source | Do not modify |
| PX-1 experience docs | Do not modify |

---

## 6. Success criteria

- [x] UI Contract specified  
- [x] 1:1 field bindings specified  
- [x] Adapter specified (formatting only)  
- [x] Component API + states specified  
- [x] Page lifecycle specified  
- [x] Vietnamese chrome + content binding specified  
- [x] No implementation artifacts  

---

## 7. Stop line

**PX-2 is design only.**

Do not implement until Product authorizes a later sprint.

END
