# Portal Data Model

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Model name: `PortalResultModel`

---

## 1. Purpose

`PortalResultModel` is the in-memory shape after the Presentation Adapter runs.

It is isomorphic to `bte.portal.result_ui.v2`.  
React (future) receives this model only.

---

## 2. Root

```
PortalResultModel
  contract_id: string
  contract_version: string
  page: PageModel
  hero: HeroModel | null
  summary: SummaryModel | null
  recommendations: RecommendationModel[]
  warnings: WarningModel[]
  domains: DomainMapModel
  charts: ChartModel[]
  technical: TechnicalModel
  knowledge: KnowledgeModel[]
  appendix: AppendixModel | null
  cta: CtaModel
  nav: NavModel
  chrome: ChromeModel
```

`chrome` holds resolved Vietnamese labels from `i18n.*` (already formatted). Components do not look up i18n themselves unless a later sprint says otherwise. Default: adapter resolves chrome into the model.

---

## 3. PageModel

```
PageModel
  state: loading | ready | partial_ready | error | empty | offline | printing | exporting
  partial: boolean
  error_code: string | null          # adapter code, not stack trace
  error_message: string | null       # Vietnamese, user-safe
```

---

## 4. HeroModel

```
HeroModel
  name: string
  headline: string
  one_line_summary: string
  status: ready | partial | in_progress | error
  status_label: string               # Vietnamese via i18n
```

---

## 5. SummaryModel

```
SummaryModel
  title: string                      # i18n resolved
  bullets: string[]                  # 1..5
```

---

## 6. RecommendationModel

```
RecommendationModel
  id: string
  domain: career | wealth | relationship | health | luck
  domain_label: string               # i18n resolved
  title: string
  reason: string
  expected_result: string
  action: string
  detail: string | null
  expanded: boolean                  # UI state, default false
```

---

## 7. WarningModel

```
WarningModel
  title: string
  body: string
  mitigation: string | null
  severity: attention | critical
  expanded: boolean
```

---

## 8. DomainMapModel

```
DomainMapModel
  career: DomainModel
  wealth: DomainModel
  relationship: DomainModel
  health: DomainModel
  luck: DomainModel

DomainModel
  key: string
  title: string
  available: boolean
  intro: string | null
  recommendation_ids: string[]
  analysis_preview: string | null
  analysis_detail: string | null
  analysis_expanded: boolean
```

All five keys always present in the model.  
Unavailable domains use empty strategy — not omitted keys (order stability).  
Warnings omit the section entirely when the array is empty (different rule).

---

## 9. ChartModel / TechnicalModel / KnowledgeModel / AppendixModel

```
ChartModel
  title: string
  caption: string
  asset_ref: string
  table: object | null
  table_expanded: boolean

TechnicalModel
  collapsed: boolean                 # default true
  calendar: string | null
  pillars: string | null
  timezone: string | null
  schema: string | null
  ids: string | null
  metadata: object | null
  available: boolean

KnowledgeModel
  title: string
  teaser: string
  body: string | null
  expanded: boolean

AppendixModel
  scope: string | null
  reread: string | null
  limits: string | null
```

---

## 10. CtaModel / NavModel

```
CtaModel
  primary_label: string
  primary_enabled: boolean
  secondary_label: string | null
  secondary_enabled: boolean

NavModel
  items: { target_ui_id: string, label: string, visible: boolean }[]
```

Nav labels = exact PX-1 section titles.  
Items for hidden sections have `visible=false` and are not rendered.

---

## 11. What this model must not contain

- Engine class names  
- AnalysisResult / DecisionResult / LuckResult / InterpretationResult  
- `module_id` as display  
- Artifact `content`  
- Pipeline traces / audits  
- Package ids  
- Raw `source_refs`  

---

## 12. Stop line

`PortalResultModel` is the only runtime object Result components bind.

END
