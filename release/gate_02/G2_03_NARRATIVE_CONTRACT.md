# G2-03 — Canonical V1.0 narrative contract

**Status:** frozen for commercial release  
**Consumer contract:** `pack05_narrative_result_v1`  
**Generator:** `narrative_composer_v2`  
**Customer Useful God contract:** `analysis_result.UsefulGodView@1.5`

This is a freeze contract, not an enhancement spec. Narrative may paraphrase frozen analytical truth. It must not invent a second analysis.

## Canonical path (one)

```
OrchestratorService.analyze
  → interpretation_foundation (frozen Gate-1 facts)
  → build_narrative_result_dict()
       prefers compose_narrative_v2_from_production()
       Pack 05 NarrativeEngine only if V2 lacks 7 sections
  → apply_published_narrative + Dayun / Luck / Ten Gods stamps
  → HTTP stamp_customer_result_identity()
       data.analysis_id = request_id
       narrative_result.run_id copied when empty
  → Portal /result + Full Report + Report/PDF bind the same blob
```

No re-analysis. No second analytical payload. Report/PDF source name remains `pack05_narrative_result_v1`. Detailed PDF rendering is G2-04.

## Source inventory

| Source | Producer | Input | Consumer | Canonical? | Fallback? | Legacy? |
|--------|----------|-------|----------|------------|-----------|---------|
| `narrative_result` V2 | `NarrativeComposerV2` via `build_narrative_result_dict` | Decision/State/Relationship/Knowledge from `interpretation_foundation` + frozen analysis bag | Portal interpretation, Full Report, Report/PDF | **Yes — V1.0 customer path** | No | No |
| Commercial KU overlay | `CommercialKnowledgeAdapter` | Projected signals from `useful_god` / `strength` / `pattern.cach_cuc` | Exec identity, career support inside the same `narrative_result` | Presentation overlay on canonical path | No | No |
| Pack 05 `NarrativeEngine.compose_narrative_result` | `engines/narrative_engine` | Same analysis bag | Same consumer contract | No | **Yes — only if V2 lacks 7 sections** | Compatibility |
| `InterpretationResult` / `interpret_from_analysis()` | Pack 04 Interpretation Engine | Analysis engines | Expert/internal; not the customer spine | No | No | Expert pipeline |
| Sentence / template / placeholder libraries | `knowledge/sentence_library`, Pack 04 templates | Engine facts | Internal composition helpers | No | No | Internal |
| Legacy Portal `presenters/narrative.js` | Customer portal static JS | Stored blob | `?legacy=1` only | No | No | **Yes** |
| Preview / mock prose | Canonical Desktop fixture | None | `?preview=1` only | No | No | Dev only |
| Old History stored narrative | Prior Analyze snapshot | Stored `data` | History URL only, G2-01R version policy | Historical | No | If unversioned: notice, do not reinterpret |

## Narrative input contract

Canonical narrative **reads** frozen customer fields:

| Topic | Canonical field | Must not read as winner |
|-------|-----------------|-------------------------|
| Four Pillars / Day Master | `bazi.*`, `day_master` | — |
| Strength | `strength.strength_level`, `strength.strength_score` (0–1) | Score Engine 0–100 as thân |
| Pattern / override | `pattern.cach_cuc`, `detected_special_pattern`, `qualification_level`, `ug_override_eligible` | Detected LEVEL-1 as Overall override |
| Điều hậu | `useful_god.climate_preference_label`, temperature labels | Climate as Overall Dụng |
| Five Elements | structural counts | Counts as vượng/suy proof |
| Ten Gods | G1-01 mapping (Nhật Chủ / Tỷ Kiên / hidden) | Stale polarity aliases |
| Overall Dụng | `useful_god.useful_display` | `pattern.dung_than`, old season winner |
| Dụng reason | HK-R1H `short_reason` / archetype | Independently invented reason |
| Customer Hỷ | `useful_god.favorable_display` (HK-R1H) | `pattern.hy_than`, internal `favorable_gods` as customer Hỷ |
| Kỵ | `useful_god.unfavorable_display` | `pattern.ky_than`; “toàn bộ hành bất lợi” |
| ShenSha | supplementary observations | Override of Strength/Pattern/Dụng/Luck |
| Luck | canonical current cycle | Stale month-pillar Dayun sequence |
| Score | composite score only if labeled as such | “Điểm thân” for composite 55.xx |

Release blockers that were closed in presentation (not engines):

- Commercial projection no longer falls back to `pattern.dung_than` / `pattern.ky_than`.
- Canonical 0–1 Strength score is no longer treated as Score Engine 0–100.
- Insufficient Hỷ uses HK-R1H copy; narrative must not later state a definite Hỷ.

## Same analysis ID

After HTTP Analyze:

`data.analysis_id` = `narrative_result.run_id` = Full Report `analysisId`

In-process `OrchestratorService.analyze()` does not invent an ID (both empty). Identity is stamped at the API boundary so ResultStore cannot mint a second customer id.

## Semantics freeze

- **Điều hậu ≠ Overall Dụng.** Both may be mentioned; neither invalidates the other.
- **LEVEL-1 detected ≠ qualified Overall override.** Allowed: nhận diện dấu hiệu. Forbidden unless `ug_override_eligible` is true: chuyên cách hoàn chỉnh / chuyên cách quyết định Dụng.
- **Follow patterns:** only the gated winner. Rejected Tòng Tài must not appear as winner (Tuyền).
- **Hỷ insufficient:** no “Hỷ thần là…” and no lifestyle prose that silently becomes canonical Hỷ.
- **Kỵ:** explain published Kỵ; do not claim completeness.
- **Health / finance / marriage:** tendency/reference only; keep existing disclaimers; do not deepen prediction.

## Fallback

| Gap | Customer behavior |
|-----|-------------------|
| `narrative_result` missing | Interpretation zone shows limited empty state (`Chưa đủ dữ liệu để đưa ra kết luận.`). Do not fabricate a chart-specific essay from other cards. |
| One section missing | That section body is empty/unavailable; remaining canonical sections still bind. |
| Optional ShenSha missing | Omit; do not invent. |
| Hỷ insufficient | HK-R1H sentence; no invented Hỷ action environment. |
| Old History / unversioned | G2-01R notice; do not recompose as current V1.0 truth. |
