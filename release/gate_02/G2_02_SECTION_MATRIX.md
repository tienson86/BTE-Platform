# G2-02 — Final section matrix

Canonical customer surface: **`/result`** → Canonical Desktop V2 → PACK_07 `ResultPageBody`.

Legacy `/result?legacy=1` remains **EXPLICIT LEGACY ONLY**. No second competing Result UI.

| Spec section | Current component | Canonical data | Visible on `/result`? | Final V1.0 status |
|--------------|-------------------|----------------|------------------------|-------------------|
| S00 — Thông tin định hướng / identity | `ContextZone` | `s00` + compact Cung Phi / Mệnh Quái / Nhóm Trạch from `s09` | Yes | **KEEP** |
| S00 — analysis ID | `ContextZone` technical expand (“Thông tin kỹ thuật”) | `s00.chartId` | Only after expand | **KEEP** (support reference, not hero) |
| S01 — career / định hướng nghề | `DestinyDirectionCard` | `s01.decisions` / NarrativeResult | When commercial career copy exists | **KEEP** |
| S01 — Cách cục | `PatternSnapshotCard` | `s01` row `Cách cục` ← `pattern.cach_cuc` | Yes when present | **KEEP** (primary) |
| S01 — Điều hậu | `ClimateSnapshotCard` | `s01` row `Điều hậu` ← Temperature + climate preference | Yes when present | **KEEP** (primary, separate from Dụng) |
| S01 — Đại vận | `LuckTimelineCard` | `s01` luck rows | Yes when cycles exist | **KEEP** (secondary) |
| S02 — Dụng / Hỷ / Kỵ | `CoreIndicatorsCard` (`data-card="useful-gods"`) | `@1.5` `useful_display` / `favorable_display` / `unfavorable_display` | Yes | **KEEP** (primary) |
| S02 — Căn cứ chọn Dụng | same card, full-width `data-field="dung-reason"` | `@1.5` `short_reason` | Yes | **KEEP** (required on `/result`) |
| S02 — Thế cục / compact ngũ hành | removed from indicators | duplicated by Strength + Five Elements | No | **MERGE** into Strength / Phân bố Ngũ hành |
| S03 — Tứ trụ – Bát Tự | `ChartDetailCard` | `s03` pillars + Full Report overlay (tàng can / nạp âm) | Yes | **KEEP** (primary) |
| S04 — Phân bố Ngũ hành | `FiveElementsCard` | `data.five_elements.counts` | Yes | **KEEP** |
| S04 — radar | `RadarChartCard` | same structural counts | Yes, visualization zone | **KEEP** (secondary chart of S04, not a new analysis) |
| S05 — Điểm thân | `StrengthAnalysisCard` | `strength.strength_score` + customer label | Yes | **KEEP** (primary) |
| S06 — Thập thần nổi bật | `TenGodsAnalysisCard` | prominence: Lộ rõ / Ẩn nổi bật | Yes | **KEEP** |
| S07 — Thần sát | `ShenShaCard` | canonical ShenSha entries | When entries exist | **KEEP** |
| S08 — Luận giải tổng thể | `InterpretationZone` | NarrativeResult sections | Yes | **KEEP** |
| S09 — Cung Phi full Bagua | compact in `ContextZone` only | `feng_shui` / calendar | Compact yes; full S09 desktop module not mounted | **KEEP** compact / **HIDE** full S09 on Result body |
| S10 — Cân Xương | desktop `S10BoneWeightFortune` | not in production pipeline | Not mounted on Result Page | **HIDE** / **LEGACY** |
| S11 — Báo cáo / tổng kết | `/reports` + Full Report HTML | same stored `data` | Nav only, not Result body | **LEGACY** (secondary nav) |
| Recommendations | `RecommendationZone` | NarrativeResult recommendations | When present | **KEEP** |
| Knowledge / technical appendix | `KnowledgeZone` | identity metadata, not analytics | Accordion | **KEEP** (diagnostics, not core result) |
| Empty / version / history chrome | `ResultPageStatusGate` + history banner | G2-01R boot | Gate or banner | **KEEP** |

Do not remove KEEP rows for aesthetics. MERGE/HIDE only where duplicated or obsolete.
