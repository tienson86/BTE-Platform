# 07 — BTE V1 Deprecation Status

Version: 1.0  
Status: **CANONICAL** — Release Candidate A  
Date: 2026-08-08  
Scope: Documentation only

---

## 1. Purpose

Inventory every known **deprecated or parallel** module relevant to V1, with migration status and removal recommendations.

Deprecation does **not** mean “delete now.” V1 promises backward compatibility.

---

## 2. Status Legend

| Status | Meaning |
|--------|---------|
| **Deprecated — Active** | Still shipped; prefer successor |
| **Legacy — Supported** | Older contract still required for BC |
| **Parallel — Not official** | Works; not the official product path |
| **Deferred removal** | Needs product confirmation + cleanup epic |

---

## 3. Legacy Analysis Paths

| Item | Status | Successor | Migration | Removal recommendation |
|------|--------|-----------|-----------|------------------------|
| Direct Interpretation-as-UI-prose scraping | Deprecated — Active (fallback only) | `narrative_result` / Pack 05 | Portal prefers Pack 05 when present | Keep fallback ≥1 major; remove after zero consumers |
| Orchestrator payload `interpretation` as commercial source | Legacy — Supported | `narrative_result` | Document preference; keep publishing | Deprecate for *external commercial* clients after SDK update |
| Mixed analysis helper paths outside Orchestrator | Legacy — Supported | `OrchestratorService.analyze` | Route all product traffic through `/analyze` | Audit `analysis_engine` usage; collapse in cleanup epic |

---

## 4. Payload Field Naming

| Item | Status | Successor | Notes |
|------|--------|-----------|-------|
| `data.narrative` (Report delivery) | Legacy — Supported | Keep as delivery; commercial = `narrative_result` | Naming collision — document, do not silently rename |
| Stage alias `narrative` → `delivery` | Legacy — Supported | Prefer `delivery` / `analyze` | Keep alias |

---

## 5. Old ViewModels

| Item | Status | Successor | Migration | Removal recommendation |
|------|--------|-----------|-----------|------------------------|
| `BaZiResultViewModel` | Parallel — Not official | `CanonicalDesktopViewModel` + `ResultPageViewModel` | Already Pack 05–aware | Retire with BaZi screen |
| WP-0004 Executive Summary ViewModels | Parallel — Not on NarrativeResult | Result Page executive zone / Pack 05 summary | Future Pack 06 consumer epic | Keep until product drops screen |
| WP-0009 Consultation Report ViewModels | Parallel — Not on NarrativeResult | Future Report Engine + NarrativeResult | Future epic | Keep |
| Fixture / mock Canonical Desktop leakage into API path | Removed in Stabilization V1 | API-backed adapters | Done | N/A |

---

## 6. Old Adapters

| Item | Status | Successor | Migration | Removal recommendation |
|------|--------|-----------|-----------|------------------------|
| Interpretation section scraping in Canonical / BaZi adapters | Deprecated — Active (fallback) | `narrativeResultAdapter` + Pack 05 | Prefer path done | Delete scrape branches after G3 window |
| Duplicate commercial mapping across Canonical + Result + BaZi | Parallel | Collapse to Canonical → Result only | After BaZi retirement | Cleanup epic (Product Integration G7) |
| Report markdown scrape for S11 when Pack 05 absent | Legacy fallback | Pack 05 conclusion / summary | Prefer Pack 05 | Keep fallback |

---

## 7. Old Screens

| Item | Status | Successor | Migration | Removal recommendation |
|------|--------|-----------|-----------|------------------------|
| `BaZiResultScreen` | Parallel — Not official | Canonical Desktop / Result Page | Prefer Result boot | Product confirmation → delete |
| Legacy AppLayout result flows | Deprecated where superseded | `PortalPage` / Result Page | Stabilization | Confirm no entrypoints |
| Executive Summary Screen (WP-0004) | Parallel | Result executive zone | Optional Pack 06 | Product call |
| Consultation Report Screen (WP-0009) | Parallel | Future Report UX | Future | Product call |

---

## 8. Engine Co-location Notes

| Item | Status | Notes |
|------|--------|-------|
| WP7 `NarrativeReport` path inside Narrative Engine | Legacy — Supported | Not Portal official prose |
| Pack 05 `NarrativeResult` | **Official** | Prefer for all commercial UI |
| Report Engine current markdown path | Active · pending redesign | Future must consume NarrativeResult |

---

## 9. Migration Status Snapshot (Product Integration V1)

| Consumer | Prefers NarrativeResult? |
|----------|--------------------------|
| Result Page LP-005 Recommendations | Yes |
| Result Page LP-006 Interpretation | Yes |
| Canonical S01 / S08 / S11 | Yes |
| BaZi interpretation block | Yes |
| WP-0004 / WP-0009 | No |
| Report delivery `narrative` | N/A (different object) |

---

## 10. Recommended Removal Order

1. Confirm Result Page as sole commercial UI.  
2. Remove BaZi Result entrypoints / adapter / tests (dedicated epic).  
3. Collapse adapter scrape fallbacks once API always emits Pack 05.  
4. Migrate or retire Pack 06 parallel screens.  
5. Redesign Report Engine on NarrativeResult; then consider renaming delivery field with wrappers.  
6. Only then consider stopping publication of raw `interpretation` to external clients.

---

## 11. Non-Deprecated (Do Not Mark)

- Foundation V1.0  
- Design System packs  
- Score / Interpretation / Narrative Pack 05 facades  
- Orchestrator stage order  
- `narrative_result` contract  

---

END
