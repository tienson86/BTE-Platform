# ENGINE_INTEGRATION_DESKTOP.md

> Status: IN PROGRESS
>
> Started: 2026-08-07 (immediately after Desktop V2 freeze)

---

## Goal

Portal Canonical Desktop consumes real Orchestrator output (`POST /analyze`) instead of static mock for S00–S11.

---

## Architecture

```
BirthRequest
  → AnalyzeService.getCanonicalDesktopViewModel()
  → POST /api/v1/analyze  (OrchestratorService)
  → adaptAnalysisToCanonicalDesktop(AnalysisDataDto)
  → CanonicalDesktopProvider
  → S00–S11 / PortalChrome
```

### Key files

| Layer | Path |
|-------|------|
| Adapter | `applications/customer_portal/src/adapters/canonicalDesktopAdapter.ts` |
| Service | `applications/customer_portal/src/services/analyzeService.ts` |
| Hook | `applications/customer_portal/src/hooks/useCanonicalDesktopResult.ts` |
| Context | `applications/customer_portal/src/screens/canonical_desktop/CanonicalDesktopContext.tsx` |
| Page | `applications/customer_portal/src/screens/canonical_desktop/PortalPage.tsx` |

### Usage

```tsx
<PortalPage
  request={{
    year: 1990,
    month: 8,
    day: 15,
    hour: 10,
    minute: 30,
    gender: "male",
    full_name: "Nguyễn Văn A",
  }}
/>
```

Omit `request` → fixture preview (`data-mode="dashboard-preview"`).

With live API (`VITE_DATA_SOURCE=api`) → `data-mode="engine-live"`.

---

## Engine mapping

| Section | Engine / API slice |
|---------|-------------------|
| S00 | Request + customer echo + calendar lunar |
| S01 | BaZi day master + Pattern + Strength + Interpretation |
| S02 | Score wuxing + Pattern/UsefulGod |
| S03 | BaZi pillars (Calendar→BaZi) |
| S04 | Score `wuxing_series` |
| S05 | Strength (+ score) |
| S06 | Score `ten_god_series` / BaZi ten_gods |
| S07 | BaZi `shensha` |
| S08 | Interpretation sections |
| S09 | Calendar feng-shui fields (`cung_phi`, `menh_quai`, `nhom_trach`) |
| S10 | **No engine yet** — fixture fallback |
| S11 | Report / Narrative markdown |

---

## Remaining integration work

1. Route host: pass birth `request` from case/URL into `PortalPage`.
2. Improve Interpretation → S08/S11 structured lists (section taxonomy).
3. Bone-weight engine for S10.
4. Richer Feng Shui bullets from full `GuaResult` when exposed on calendar payload.
5. Remove fixture fallback from production route once live path is mandatory.

---

END
