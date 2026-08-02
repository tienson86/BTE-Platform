# 18 — BINDING INDEX (Complete UI Slot Map)

| Field | Value |
|-------|--------|
| **Document** | `18_BINDING_INDEX.md` |
| **Version** | `1.1.0` |
| **Status** | **Normative — Blueprint V1.1 Final** |
| **Rule** | UI binds only listed paths / aliases. No invented fields. Missing → [Empty/Unavailable](16_EMPTY_UNAVAILABLE_STATES.md). |

---

## Purpose

Single complete **UI Slot → Payload binding** index for Customer Portal Result (and related entry points).  
Aliases may be resolved by `ReportViewModelAdapter` / SummaryBuilder; **new business keys must not be invented in UI**.

Notation:

- `a|b|c` = first present wins  
- `[]` = array  
- `MISS` = Unavailable / `--` per Empty contract  

---

## 0. Page / chrome

| UI Slot ID | UI location | Binding | If missing |
|------------|-------------|---------|------------|
| `page.payload` | ResultPage | ResultStore `loadForView().data` | PAGE_EMPTY |
| `page.input` | ResultChrome meta | `loadForView().input` | meta limited |
| `chrome.birth_datetime` | ResultChrome | `input.year,month,day,hour,minute` | MISS |
| `chrome.gender` | ResultChrome | `input.gender` | MISS / unspecified label |
| `chrome.actions.reports` | ResultChrome | route `/reports` | — |
| `chrome.actions.analyze` | ResultChrome | route `/analyze` | — |

---

## 1. Tier Executive — Hero

| UI Slot ID | UI | Binding (priority) | If missing |
|------------|----|--------------------|------------|
| `hero.eyebrow` | Eyebrow | i18n only | — |
| `hero.day_master.stem` | DayMasterDisplay | `bazi.day_master` \| `bazi.dayMaster` \| `bazi.nhat_chu` \| `bazi.day_pillar.stem` \| `thien_can` | UNAVAILABLE |
| `hero.day_master.element` | DayMasterDisplay | `bazi.day_master_element` \| stem→element map (display-only) | `--` |
| `hero.day_master.yin_yang` | DayMasterDisplay | payload \| stem→yy map (display-only) | `--` |
| `hero.quality_verdict` | QualityVerdictCaption | See Addendum A.2: `score.grade` → else `score.total_score`\|`overall_score` → else confidence caption → else UNAVAILABLE | UNAVAILABLE |
| `hero.quality_value` | SummaryMetric Quality | `score.grade` \| `score.total_score` \| `overall_score` \| `interpretation.confidence` | `--` |
| `hero.sentence` | Summary sentence | Composed from present DM/pattern/useful only (no new facts) | fallback i18n |
| `hero.than` | Metric Thân | `pattern.than_vuong_nhuoc` \| `strength` \| `strength_level` \| `body_strength` \| `vuong_nhuoc` \| `day_master_strength` \| `pattern.than` | UNAVAILABLE |
| `hero.dung_than` | Metric Dụng | `pattern.dung_than` \| `useful_god` \| `yong_shen` \| `useful_god.*` primary | UNAVAILABLE |
| `hero.hy_than` | Metric Hỷ | `pattern.hy_than` \| `xi_shen` \| `favorable_god` \| useful_god.favorable | UNAVAILABLE |
| `hero.ky_than` | Metric Kỵ | `pattern.ky_than` \| `ji_shen` \| `unfavorable_god` | UNAVAILABLE |
| `hero.cach_cuc` | Metric Cách | `pattern.cach_cuc` \| `pattern_name` \| `ge_ju` \| `main_pattern` (+ label format) | UNAVAILABLE |
| `hero.strengths` | Panel | `score.strengths` \| `uu_diem` \| `pros` (list) | empty list display |
| `hero.weaknesses` | Panel | `score.weaknesses` \| `nhuoc_diem` \| `cons` \| `warnings` | empty list display |
| `hero.first_recommendation` | FirstRecommendation | `score.recommendations[0]` \| split `score.recommendation` \| interp chapter `advice`/`conclusion` first sentence | UNAVAILABLE |

---

## 2. Tier Bazi — Pillars

For each pillar `year|month|day|hour` (keys `year_pillar`, `month_pillar`, `day_pillar`, `hour_pillar` + alts):

| UI Slot ID | Binding | If missing |
|------------|---------|------------|
| `pillar.{p}.stem` | `stem` \| `thien_can` \| `can` | `--` |
| `pillar.{p}.branch` | `branch` \| `dia_chi` \| `chi` | `--` |
| `pillar.{p}.hidden` | pillar `hidden_stems`\|`tang_can`\|`hidden` \| sliced `bazi.hidden_stems` | `--` |
| `pillar.{p}.ten_god` | pillar `ten_god` \| catalog position | `--` |
| `pillar.{p}.chang_sheng` | `truong_sinh` \| `chang_sheng` \| `changsheng` | `--` |
| `pillar.{p}.nap_am` | `nap_am` \| `nayin` \| `na_yin` | `--` |
| `pillar.day.is_day` | index === day | highlight |

---

## 3. Tier Charts

| UI Slot ID | Binding | If missing |
|------------|---------|------------|
| `chart.elements.series` | Prefer `score.wuxing_series` / named element scores; else **display-only** count from pillar stems+branches | CHART_EMPTY |
| `chart.elements.radar` | same series | CHART_EMPTY |
| `chart.elements.bars` | same series | CHART_EMPTY |
| `chart.strength.gauge` | numeric `score.strength_score` \| `body_strength_score` \| `than_score` only | text = `hero.than` (no invented number) |
| `chart.ten_gods.bars` | named ten-god scores if present; else frequency from pillar ten_gods | CHART_EMPTY |
| `chart.wuxing_score_scalar` | optional single `wuxing_score` | ignore if series exists |

---

## 4. Tier Analysis

| UI Slot ID | Binding | If missing |
|------------|---------|------------|
| `analysis.elements.body` | chart.elements.series + optional short explain from interp five_elements section text if present | chart + UNAVAILABLE explain |
| `analysis.ten_gods.body` | chart.ten_gods / checklist from bazi.ten_gods | UNAVAILABLE |
| `analysis.pattern.body` | `hero.cach_cuc`, `pattern.tong_cach`, `hero.than` | UNAVAILABLE cells |
| `analysis.useful.body` | dung/hy/ky + `pattern.dieu_hau` | UNAVAILABLE cells |
| `analysis.relations.hop` | `pattern.hop` \| `bazi.hop` \| `he` \| `combinations` | UNAVAILABLE row |
| `analysis.relations.xung` | `xung` \| `chong` \| `conflicts` | UNAVAILABLE row |
| `analysis.relations.hinh` | `hinh` | UNAVAILABLE row |
| `analysis.relations.hai` | `hai` | UNAVAILABLE row |
| `analysis.relations.pha` | `pha` | UNAVAILABLE row |
| `analysis.shensha` | `bazi.shensha` \| `than_sat` \| `shen_sha` | UNAVAILABLE |
| `analysis.knowledge_status` | `data.knowledge_expert` object | UNAVAILABLE |
| `analysis.priority_rules` | Only if payload provides explicit priority/rule **display text**; else do not invent — fold into knowledge_status badges | UNAVAILABLE / omit essay |

**Short explain source (G12 closed):** Prefer matching `interpretation.sections` text for that theme; else caption-only under chart — never LLM-invented in UI sprint.

---

## 5. Tier Interpretation (document)

| UI Slot ID | Binding | If missing |
|------------|---------|------------|
| `interp.confidence` | `interpretation.confidence` | hide caption |
| `interp.toc` | derived from chapter availability | hide if <2 available |
| `interp.chapter.highlights` | sections id/title map: overview, summary, tong_quan | UNAVAILABLE body |
| `interp.chapter.career` | career, su_nghiep | UNAVAILABLE body |
| `interp.chapter.wealth` | wealth, tai_van | UNAVAILABLE body |
| `interp.chapter.marriage` | marriage, hon_nhan | UNAVAILABLE body |
| `interp.chapter.health` | health, suc_khoe | UNAVAILABLE body |
| `interp.chapter.personality` | bazi, personality, five_elements, ten_gods (first hit) | UNAVAILABLE body |
| `interp.chapter.advice` | conclusion, recommendations, useful_god, ket_luan | UNAVAILABLE body |
| `interp.callout` | optional: first sentence of highlights if present | omit |
| `interp.references` | citation lines if section/metadata provides; else link affordance to Knowledge | omit list |

Chapter **titles always visible**.

---

## 6. Tier Knowledge

| UI Slot ID | Binding | If missing |
|------------|---------|------------|
| `knowledge.status` | `data.knowledge_expert` | UNAVAILABLE panel |
| `knowledge.evidence.rows` | From discussion response `summary`, `validation`, `discussion.*` when user asked; pre-ask may be empty | empty honest / UNAVAILABLE |
| `knowledge.evidence.source_type` | mapped: rule/classical/reasoning/status | `unknown` |
| `knowledge.evidence.reference` | classical titles / reasoning conclusions — never CSV paths | omit |
| `knowledge.evidence.confidence` | `discussion.confidence` \| validation | omit |
| `knowledge.expert.question` | user input | — |
| `knowledge.expert.request` | POST existing `/api/v1/discussion` with birth fields + question | EXPERT_ERROR |
| `knowledge.expert.answer` | `data.discussion.answer` | EXPERT_ERROR / empty |
| `knowledge.expert.sources_pane` | summary + validation + badges | SOURCES_EMPTY copy |
| `knowledge.narrative_fallback` | `data.narrative` \| `data.report` | omit details |

**Engine names:** not bound to consumer UI (default).

---

## 7. Navigation

| UI Slot ID | Binding |
|------------|---------|
| `nav.tiers` | Fixed list — not from payload |
| `nav.active` | ScrollSpy |
| `nav.progress` | scroll ratio / highest tier |

---

## 8. Secondary screens (minimal)

| UI Slot ID | Binding | If missing |
|------------|---------|------------|
| `dashboard.recent` | ResultStore history | EmptyState |
| `dashboard.stats` | history-derived counts | `--` |
| `dashboard.health` | `/healthz` + API health if called | down badge |
| `dashboard.cta.analyze` | always visible | — |
| `analyze.form.*` | form fields → POST `/api/v1/analyze` | validation errors |
| `history.list` | history | EmptyState |
| `history.open` | selectForView → `/result` | — |
| `reports.list` | history items with narrative/report | EmptyState |
| `reports.preview` | selected narrative/report | empty preview |
| `profile.user` | auth me / session | EmptyState |
| `login.credentials` | form → auth | errors |

---

## 9. Non-goals (explicitly unbound)

Do not create UI slots for:

- Fabricated Đại vận years  
- Fabricated Hợp/Xung  
- Internal rule id catalogues for consumers  
- Engine class names  
- Mobile layouts  

---

## Version

`1.1.0`
