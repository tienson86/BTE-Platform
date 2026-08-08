# Product Integration V1 — Remaining Gaps

Version: 1.0  
Status: OPEN ITEMS (not blockers for V1 Portal preference)  
Date: 2026-08-08

---

## 1. Summary

Product Integration V1 wires Pack 05 `NarrativeResult` into API + Result Page Portal. Gaps below are intentional deferrals or out-of-scope items, not regressions of the preference contract.

---

## 2. Gaps

### G1 — Parallel BaZi Result screen still exists

- **What:** `BaZiResultScreen` + `BaZiResultViewModel` + `useBaZiResult` remain as a Wave-3 path beside Canonical Desktop / Result Page.
- **Status:** Pack 05–aware (`mapInterpretation` prefers `narrative_result`), but duplicate presentation stack not removed.
- **Why kept:** Still exported, tested (`wave3_bazi_result.test.tsx`), and used by `analyzeService.getBaZiResultViewModel`.
- **Next:** Deprecate entry points once product confirms Result Page is sole commercial surface; then delete BaZi adapter/screen in a dedicated cleanup epic.

### G2 — Pack 06 WP-0004 / WP-0009 ViewModels not on NarrativeResult

- **What:** Executive Summary Screen / Consultation Report Screen use their own ViewModels (`view_models/executive_summary.ts`, `consultation_report.ts`).
- **Status:** Not Result Page; not migrated to Pack 05.
- **Next:** Separate Pack 06 consumer epic if those screens remain product surfaces.

### G3 — Legacy `interpretation` still published on `/analyze`

- **What:** Orchestrator still emits full Interpretation Engine sections.
- **Why:** Backward compatibility for older clients and Portal fallback when Pack 05 is absent.
- **Next:** After all consumers migrate, mark deprecated in API docs; do not remove until BC window closes.

### G4 — Naming collision: `data.narrative` vs `data.narrative_result`

- **What:** `narrative` = ReportEngine delivery markdown; `narrative_result` = Pack 05 commercial object.
- **Risk:** Integrators may confuse fields.
- **Next:** Document in OpenAPI / client SDK; optionally rename delivery field in a future BC-breaking major (wrapper required).

### G5 — Knowledge / Timeline / structural cards are not NarrativeResult prose

- **What:** Knowledge zone and some timeline snippets still bind chart/score/pattern facts (or S08-derived lists), not full Pack 05 section paragraphs.
- **Why:** Those zones are structural / glossary, not commercial narrative grammar.
- **Next:** Optional polish — map Knowledge “references” detail from Pack 05 conclusion/observation only if product asks.

### G6 — Insufficient-evidence quality of Pack 05 output

- **What:** Many live analyses still yield `partial_insufficient` / approved insufficient copy when Interpretation evidence is thin.
- **Impact:** Portal correctly shows Pack 05 text, but commercial richness depends on Narrative Engine + Interpretation evidence upstream — **out of scope** for this epic (no Narrative Engine edits).
- **Next:** Narrative quality / evidence enrichment epic.

### G7 — Duplicate adapter surface not fully collapsed

- **What:** Three adapters still map commercial text: `canonicalDesktopAdapter`, `resultPresentationAdapter`, `baziResultAdapter` (+ shared `narrativeResultAdapter` helpers).
- **Status:** Preference logic is consistent; physical duplication of fallback scraping remains for BC.
- **Next:** After BaZi screen retirement, collapse to: DTO helper → Canonical Desktop → Result Presentation only.

### G8 — Report Engine not implemented / not redesigned

- **What:** Explicit epic constraint. Delivery `narrative` remains ReportEngine markdown path.
- **Next:** Future Report Engine epic; must consume Pack 05 `NarrativeResult`, not re-scrape Interpretation.

---

## 3. Explicit non-gaps (closed by V1)

| Item | Resolution |
|------|------------|
| Portal Result Page prefers Pack 05 | Done |
| API publishes `narrative_result` | Done |
| S01 / S08 / S11 prefer Pack 05 | Done |
| LP-005 / LP-006 prefer Pack 05 | Done |
| BaZi interpretation prefers Pack 05 | Done |
| Foundation unchanged | Confirmed |
| Narrative Engine not edited in integration layer | Confirmed (public API consume only) |
| Report Engine not implemented | Confirmed |

---

## 4. Recommended order for follow-ups

1. Narrative quality / evidence enrichment (G6) — product blocker for “consultant-grade” copy  
2. Deprecate BaZi Result screen (G1 → G7)  
3. Pack 06 WP-0004/0009 NarrativeResult consumers (G2)  
4. API deprecation of raw interpretation for external clients (G3)  
5. Report Engine epic consuming Pack 05 (G8)

---

## 5. Acceptance reminder

Do **not** treat G1–G8 as failures of Product Integration V1. V1 acceptance is: **every Result Page commercial prose path prefers `NarrativeResult` when present.**
