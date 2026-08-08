# 02 — Data Mapping Report

**Epic:** BTE Stabilization V1  
**Date:** 2026-08-08  
**Primary UI:** Result Page via Canonical Desktop adapter  
**Unavailable copy:** `Chưa đủ dữ liệu để đưa ra kết luận.`

---

## Mapping convention

```
Result Page field
  → ResultPageViewModel
  → CanonicalDesktopViewModel (adapter)
  → API AnalysisDataDto / Engine view
  → Knowledge / Rule source
```

If a commercial narrative source cannot be identified → **UNMAPPED** (display unavailable).

---

## Context Zone

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| Title | `context.title` | `s00.title` | Structural | UI copy |
| Profile name | `context.profileName` | `s00.profile.name` | `customer.full_name` / request | Customer input |
| Birth solar | `context.birthDate` | `s00.birth.date` | request / calendar | Calendar |
| Birth lunar | `context.birthLunar` | `s00.birth.lunar` | `calendar.*_can_chi` | Calendar + Bazi |
| Birth time | `context.birthTime` | `s00.birth.time` | request | Customer input |
| Chart id | `context.chartId` | `s00.chartId` | request id | Runtime |
| Status | `context.status` | `s00.status` | pipeline status | Runtime |
| Analyzed at | `context.analyzedAt` | `s00.analyzedAt` | runtime stamp | Runtime |

---

## Executive Summary

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| Title | `executive.title` | Fixed "TÓM TẮT ĐIỀU HÀNH" | — | UI |
| Headline | `executive.headline` | `s08.executive.body` | Interpretation section (Tính cách / Kết luận / Tổng quan) or `score.recommendation` | Sentence/rule DB via Interpretation |
| Points (strengths) | `executive.points` | `s08.strengths` | Interpretation `Điểm mạnh` | Interpretation |
| Points (warnings) | `executive.points` | `s08.warnings` | Interpretation `Điểm cần lưu ý` / `Lưu ý` | Interpretation |

Technical rule bodies are gated → unavailable when not commercial.

---

## Core Indicators

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| Ngũ hành nổi | `indicators.items` | `s02` | `score.wuxing_series` | Score rules |
| Âm dương | `indicators.items` | `s02` | `bazi.day_master_yin_yang` | Bazi |
| Thế cục | `indicators.items` | `s02` | `pattern.than_vuong_nhuoc` | Pattern / Strength |
| Dụng thần | `indicators.items` | `s02` | `useful_god.useful_god` / `pattern.dung_than` | Useful God rules |
| Hỷ thần | `indicators.items` | `s02` | `useful_god.favorable_gods` / `pattern.hy_than` | Useful God |
| Kỵ thần | `indicators.items` | `s02` | `useful_god.unfavorable_gods` / `pattern.ky_than` | Useful God |

---

## Destiny Direction

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| BẠN LÀ AI? | `destiny.items[0]` | `s01.decisions[0]` | Interpretation Tính cách / Tổng quan; else Nhật chủ + cách cục facts | Interpretation / Bazi / Pattern |
| THẾ MẠNH? | `destiny.items[1]` | `s01.decisions[1]` | Interpretation Điểm mạnh; else pattern facts | Interpretation / Pattern |
| BẠN NÊN LÀM GÌ? | `destiny.items[2]` | `s01.decisions[2]` | Interpretation Dụng thần / Kết luận; else useful god + score.recommendation | Interpretation / Useful God / Score |
| CTA | `destiny.cta` | `s01.cta` | Structural | UI |

---

## Analysis cards

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| Five elements rows | `fiveElements.rows` | `s04.rows` | `score.wuxing_series` | Score Wuxing |
| Five elements summary | `fiveElements.summary` | `s04.summary` | Derived + `score.grade` | Score |
| Strength level/score | `strength.*` | `s05` | `score.strength_score` / `strength.*` | Strength rules |
| Strength insight | `strength.insight` | `s05.insight` | `strength.reasoning` (gated) | Strength |
| Ten gods | `tenGods.gods` | `s06.gods` | `score.ten_god_series` or `bazi.ten_gods` | Score / Bazi |

---

## Visualization

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| Radar axes | `radar.axes` | `s04.rows` | `score.wuxing_series` | Score |
| Radar summary | `radar.summary` | `s04.summary` | Derived | Score |
| Timeline Tiền vận | `timeline.stages[0]` | (was s10) | **UNMAPPED** — no luck/bone engine | — |
| Timeline Trung/Hậu/Định hướng | `timeline.stages[1..]` | `s08` strengths/warnings/actions | Interpretation / Score | Interpretation |
| Timeline summary | `timeline.summary` | — | **UNMAPPED** (bone-weight) | — |

---

## Recommendations

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| Action | `recommendations.items.action` | `s11.recommendations` ← `s08.actions` | Interpretation Dụng thần/Kết luận or useful god / score.recommendation | Interpretation / Useful God / Score |
| Reason | `recommendations.items.reason` | `s08.warnings` / executive | Interpretation warnings | Interpretation |
| Benefit | `recommendations.items.benefit` | `s08.strengths` / s11 executive | Interpretation strengths | Interpretation |

---

## Interpretation Zone

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| Overview block | `interpretation.blocks[0]` | `s08` + `s01` + `s04` | Interpretation + Score summary | Interpretation / Score |
| Caution block | `interpretation.blocks[1]` | `s08.warnings` + `s05` + `s11` | Interpretation + Strength | Interpretation / Strength |
| Direction block | `interpretation.blocks[2]` | `s01.decisions` + `s08.actions` | Interpretation + Useful God | Interpretation |

---

## Knowledge Zone

| Field | ViewModel | Adapter | Engine / API | Knowledge source |
|-------|-----------|---------|--------------|------------------|
| Terminology | `knowledge.sections` | day master / dụng / thế cục from s01/s02 | Bazi / Pattern / Useful God | Chart facts (not Knowledge Engine retrieval) |
| References | `knowledge.sections` | s04 + s08 snippets | Score / Interpretation | Partial |
| Theory | `knowledge.sections` | s04 / s05 | Score / Strength | Partial |
| Appendix | `knowledge.sections` | s00 metadata + footer | Runtime | Runtime |

**UNMAPPED:** Knowledge Engine document retrieval / classical citation IDs.

---

## Parallel BaZi Result screen (secondary)

| Field | Mapping after stabilization |
|-------|-----------------------------|
| Pillars / elements / ten gods / strength | API → `baziResultAdapter` |
| Executive Dụng/Hỷ/Kỵ/pattern/grade | pattern + useful_god + score |
| Interpretation paragraphs | `interpretation.sections` (commercial-gated) |
| Shen Sha | `bazi.shensha` |
| Spirit gods row | useful_god / pattern (not mock) |
| Bone-weight metric | **UNMAPPED** → unavailable |

---

## Summary counts

| Category | Count |
|----------|-------|
| Mapped fields | 40+ |
| UNMAPPED (engine gap) | Bone-weight, early luck timeline, Knowledge CMS |
| Gated technical interpretation | Multiple section bodies (rule prose) |

---

END
