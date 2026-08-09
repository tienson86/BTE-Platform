# Component Tree — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-1  
Scope: Logical experience components — not React files

---

## 1. Purpose

Define the complete logical hierarchy of the Result Experience.

Names below are **design identifiers**.  
User-visible titles remain Vietnamese per `LANGUAGE_GUIDE.md`.

This tree is not an implementation folder map.

---

## 2. Full tree

```
ResultPage
├── SkipToContent
├── PageChrome
│   └── ProductNav                    (product shell, not Hero)
├── InPageNav                         (optional TOC · Vietnamese labels)
│
├── Hero
│   ├── Identity
│   │   ├── DisplayName
│   │   └── ProfileAnchor             (human, not ID)
│   ├── Headline
│   ├── OneLineSummary
│   └── ConsultationStatus
│
├── ExecutiveSummary                  (title: Tóm tắt tư vấn)
│   └── SummaryList
│       └── SummaryBullet             (max 5 · one sentence each)
│
├── Recommendation                    (title: Định hướng chính)
│   ├── RecommendationGroupCareer
│   ├── RecommendationGroupWealth
│   ├── RecommendationGroupRelationship
│   ├── RecommendationGroupHealth
│   └── RecommendationGroupLuck
│       └── RecommendationCard
│           ├── DomainTag
│           ├── RecTitle
│           ├── Why
│           ├── ExpectedResult
│           ├── Action
│           ├── ExpandControl
│           └── RecDetail             (collapsed)
│
├── ImportantWarnings                 (title: Lưu ý quan trọng)
│   └── WarningCard
│       ├── WarningTitle
│       ├── WarningBody
│       ├── Mitigation
│       └── ExpandControl
│
├── DomainCareer                      (title: Sự nghiệp)
├── DomainWealth                      (title: Tài chính)
├── DomainRelationship                (title: Quan hệ)
├── DomainHealth                      (title: Sức khỏe)
├── DomainLuck                        (title: Vận trình)
│   └── DomainSection
│       ├── DomainIntro
│       ├── DomainRecommendationList
│       │   └── RecommendationCard
│       └── AnalysisPreview           (optional)
│           ├── AnalysisCard
│           └── ExpandControl
│
├── Charts                            (title: Biểu đồ minh họa)
│   └── ChartCard
│       ├── ChartTitle
│       ├── ChartFigure
│       ├── ChartCaption
│       └── ChartTableExpand          (optional · collapsed if heavy)
│
├── TechnicalInfo                     (title: Chi tiết kỹ thuật · collapsed)
│   ├── TechnicalToggle
│   └── TechnicalPanel
│       ├── CalendarBlock
│       ├── PillarsBlock
│       ├── TimezoneBlock
│       ├── SchemaBlock
│       ├── IdentifiersBlock
│       └── MetadataBlock
│
├── Knowledge                         (title: Kiến thức bổ sung · collapsed)
│   ├── KnowledgeToggle
│   └── KnowledgeList
│       └── KnowledgeCard
│           ├── KnowledgeTitle
│           ├── KnowledgeTeaser
│           └── ReadMoreControl
│
├── Appendix                          (title: Phụ lục)
│   ├── ScopeNote
│   ├── RereadNote
│   └── LimitsNote
│
└── Footer
    └── ProductFooter
```

---

## 3. Cross-cutting components

These may appear inside multiple parents. They are not sections.

```
Shared
├── EmptyStateCard
├── ErrorStateCard
├── ExpandCollapseControl
├── PrimaryButton
├── SecondaryButton
├── TextButton
├── Tag
├── Note
└── StatusBadge                     (Vietnamese only)
```

---

## 4. Ownership rules

| Component | Owns | Must not own |
|-----------|------|--------------|
| Hero | Session identity and one-line essence | IDs, schema, timestamps, charts |
| ExecutiveSummary | First understanding | Full plans, charts |
| Recommendation | Top actions | Technical apparatus |
| ImportantWarnings | Decision-changing risk | Exhaustive caveats |
| DomainSection | Depth for one life area | Page-level Hero / global charts |
| Charts | Visual confirmation | Primary advice |
| TechnicalInfo | Apparatus | Consulting headline |
| Knowledge | Optional learning | Upsell theatre |
| Appendix | Closure | New primary CTA |
| Footer | Product chrome | Analysis |

---

## 5. Instantiation rules

- One `ResultPage` per consultation view  
- One `Hero`  
- One `ExecutiveSummary`  
- One `Recommendation` region (may contain 0–n cards across five groups)  
- Five domain sections in fixed order, even if some are empty  
- One `TechnicalInfo` (collapsed)  
- One `Knowledge` (collapsed)  
- At most one Primary CTA instance visually dominant on the page  

---

## 6. Mapping note for future implementation

When code is authorized later:

- Map this tree onto Design System **Zone → Row → Grid → Card** primitives  
- Do not invent a parallel component system  
- Do not leak Engine models into these components  
- Keep public UI copy Vietnamese  

PACK_06/07 V1 row order is not the V2 reading order.  
Future implementation follows this tree’s sequence.

---

## 7. Stop line

Component tree V2 is the logical hierarchy for Result Experience.

END
