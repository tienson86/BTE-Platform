# 03 — Placeholder Removal Report

**Epic:** BTE Stabilization V1  
**Date:** 2026-08-08  
**Policy:** Do not invent content. Unavailable → `Chưa đủ dữ liệu để đưa ra kết luận.`

---

## Production Result path — fixed

| Location | Was | Action |
|----------|-----|--------|
| `canonicalDesktopAdapter` S08 | Mock fixture strengths/warnings/actions | Removed fixture fallback; use interpretation or unavailable |
| `canonicalDesktopAdapter` S10 | Fixture “MỆNH TỐT / 4 lượng…” | Replaced with unavailable shell |
| `canonicalDesktopAdapter` S07 empty | Returned full mock thần sát | Unavailable lists |
| `canonicalDesktopAdapter` S05 / S06 empty | Fixture insight / gods | Commercial gate / unavailable |
| `resultPresentationAdapter` Knowledge | “BTE Knowledge Base”, “PACK_06…”, “Presentation Layer…” | Removed developer/pack strings |
| `resultPresentationAdapter` Timeline S10 | Fixture bone insight | Unavailable |
| `ContentCards` labels | Observation / Explanation / Impact / Suggestion | Vietnamese commercial labels |
| `previewBuilder` priority badges | Critical / High / Medium / Low | Vietnamese labels |
| `previewBuilder` bindPlaceholder default | `—` | Unavailable conclusion string |
| `baziResultAdapter` interpretation | `BAZI_MOCK_INTERPRETATION` including “(mock)” | API sections + gate |
| `baziResultAdapter` knowledge / shensha / spirit | Mock constants | API-mapped |
| `buildExecutiveFromResult` | “chờ Interpretation Engine”, “Chờ Engine” | Mapped fields / unavailable |

---

## Shared guard

New module: `applications/customer_portal/src/adapters/contentGuards.ts`

- Detects technical/rule/placeholder markers (`Kích hoạt khi`, `Áp dụng bảng`, `PACK_`, `(mock)`, …)
- Replaces unsuitable bodies with unavailable conclusion
- Normalizes 0–1 vs 0–100 strength scores

---

## Intentionally retained (non-Result / demo)

| Location | Reason |
|----------|--------|
| `canonical_desktop/mockData.ts` / `bazi/mockData.ts` fixtures | Required for `source=mock` tests & offline preview |
| `createCanonicalDesktopMockViewModel` | Explicit mock mode |
| Dashboard CMS announcement placeholder | Outside Result pipeline |
| Footer support placeholder | Outside Result pipeline |
| ErrorBoundary logging placeholder | Observability stub, not user narrative |

---

## Remaining Result gaps (not placeholders)

| Gap | Display |
|-----|---------|
| No bone-weight engine | Unavailable conclusion |
| Interpretation rule prose | Gated to unavailable when technical |
| Knowledge Engine retrieval | Chart facts only; no invented theory |

---

## Invented content check

**None invented.** Stabilization only:

1. Maps existing engine/API fields, or  
2. Shows the mandated unavailable sentence.

---

END
