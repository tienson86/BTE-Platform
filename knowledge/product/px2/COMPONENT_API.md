# Component API

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Scope: Logical API — not React files

---

## 1. Law

Each component receives **only** its owned slice of `PortalResultModel` plus chrome it must display.

No engine types. No sibling private state.

---

## 2. ResultPage

**Owns:** `page`, `nav`, composition order.

### Props

| Prop | Type | Required |
|------|------|----------|
| `page` | PageModel | yes |
| `hero` | HeroModel \| null | yes |
| `summary` | SummaryModel \| null | yes |
| `recommendations` | RecommendationModel[] | yes |
| `warnings` | WarningModel[] | yes |
| `domains` | DomainMapModel | yes |
| `charts` | ChartModel[] | yes |
| `technical` | TechnicalModel | yes |
| `knowledge` | KnowledgeModel[] | yes |
| `appendix` | AppendixModel \| null | yes |
| `cta` | CtaModel | yes |
| `nav` | NavModel | yes |
| `chrome` | ChromeModel | yes |

### Events

| Event | Payload |
|-------|---------|
| `onPrimaryCta` | `{ source: "recommendation_region" }` |
| `onSecondaryCta` | `{ source: "recommendation_region" }` |
| `onNavigate` | `{ target_ui_id }` |
| `onRetry` | `{ scope: "page" \| section }` |

### Slots

`skipLink` · `pageChrome` · `inPageNav` · `main` · `footer`

### Children

Hero · ExecutiveSummary · Recommendation · ImportantWarnings · DomainSection×5 · Charts · TechnicalInfo · Knowledge · Appendix

### Ownership

Page lifecycle and one Primary CTA instance.

---

## 3. Hero

### Props

| Prop | Type |
|------|------|
| `name` | string |
| `headline` | string |
| `oneLineSummary` | string |
| `status` | enum |
| `statusLabel` | string |

### Events

None required.

### Slots

`identity` · `headline` · `summary` · `status`

### Children

Identity · Headline · OneLineSummary · ConsultationStatus

### Ownership

`report.identity.*` only.

---

## 4. ExecutiveSummary

### Props

| Prop | Type |
|------|------|
| `title` | string |
| `bullets` | string[] |

### Events

| Event | Payload |
|-------|---------|
| `onJumpToRecommendations` | `{}` |

### Slots

`title` · `list`

### Children

SummaryBullet×n (≤5)

---

## 5. Recommendation (region)

### Props

| Prop | Type |
|------|------|
| `title` | string |
| `groups` | { domain, domainLabel, items: RecommendationModel[] }[] |
| `cta` | CtaModel |
| `empty` | boolean |
| `emptyMessage` | string \| null |

### Events

| Event | Payload |
|-------|---------|
| `onPrimaryCta` | `{}` |
| `onSecondaryCta` | `{}` |
| `onToggleItem` | `{ id, expanded }` |

### Slots

`title` · `groups` · `primaryCta` · `secondaryCta` · `empty`

### Children

RecommendationGroup×5 · RecommendationCard · PrimaryButton · SecondaryButton

---

## 6. RecommendationCard

### Props

| Prop | Type |
|------|------|
| `id` | string |
| `domainLabel` | string |
| `title` | string |
| `reason` | string |
| `expectedResult` | string |
| `action` | string |
| `detail` | string \| null |
| `expanded` | boolean |
| `labels` | { why, expected, action, expand, collapse } |

### Events

| Event | Payload |
|-------|---------|
| `onToggle` | `{ id, expanded }` |

### Slots

`tag` · `title` · `why` · `expected` · `action` · `expand` · `detail`

No Primary button on the card.

---

## 7. ImportantWarnings

### Props

| Prop | Type |
|------|------|
| `title` | string |
| `items` | WarningModel[] |

If `items.length === 0`, parent does not mount this component (hidden).

### Events

`onToggleItem { index, expanded }`

### Children

WarningCard[]

---

## 8. DomainSection

### Props

| Prop | Type |
|------|------|
| `domain` | DomainModel |
| `recommendations` | RecommendationModel[] (resolved by ids) |
| `emptyMessage` | string \| null |

### Events

`onToggleAnalysis` · `onToggleRecommendation`

### Slots

`intro` · `recommendations` · `analysis` · `empty`

### Children

DomainIntro · RecommendationCard[] · AnalysisCard · EmptyStateCard

---

## 9. Charts

### Props

`title` · `items: ChartModel[]`

Mount only if `items.length > 0`.

### Events

`onToggleTable { index }`

### Children

ChartCard[]

---

## 10. TechnicalInfo

### Props

`title` · `collapsed` · `model: TechnicalModel` · `toggleLabels`

### Events

`onToggle { collapsed }`

### Slots

`header` · `panel`

Default collapsed.

---

## 11. Knowledge

### Props

`title` · `collapsed` · `items: KnowledgeModel[]` · `toggleLabels`

Mount: if no items, do not mount (hidden).  
If items exist, default section collapsed.

### Events

`onToggleSection` · `onToggleItem`

### Children

KnowledgeCard[]

---

## 12. Appendix

### Props

`title` · `scope` · `reread` · `limits`

Mount only if any field non-null.

### Events

None.

---

## 13. EmptyStateCard / ErrorStateCard

### Empty props

`title` · `body` · `nextLabel?` · `nextTarget?`

### Error props

`title` · `body` · `retryLabel?` · `retryScope?`

### Events

Empty: `onNext`  
Error: `onRetry`

---

## 14. Stop line

APIs are experience contracts. No implementation types.

END
