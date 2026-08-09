# Component Map — Result Experience V2

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-1

Maps logical components to sections and card types.  
Not a React file map.

---

## Section → components → card type

| Section (VI) | Components | Card type |
|--------------|------------|-----------|
| Hero | Identity, Headline, OneLineSummary, ConsultationStatus | CardHero |
| Tóm tắt tư vấn | ExecutiveSummary, SummaryList, SummaryBullet | CardSummary |
| Định hướng chính | Recommendation + five RecommendationGroups + RecommendationCard | CardRecommendation |
| Lưu ý quan trọng | ImportantWarnings, WarningCard | CardRecommendation pattern / Warning variant |
| Sự nghiệp | DomainCareer → DomainSection | CardRecommendation + CardAnalysis |
| Tài chính | DomainWealth | CardRecommendation + CardAnalysis |
| Quan hệ | DomainRelationship | CardRecommendation + CardAnalysis |
| Sức khỏe | DomainHealth | CardRecommendation + CardAnalysis |
| Vận trình | DomainLuck | CardRecommendation + CardAnalysis |
| Biểu đồ minh họa | Charts, ChartCard | CardChart |
| Chi tiết kỹ thuật | TechnicalInfo, TechnicalPanel blocks | CardTechnical |
| Kiến thức bổ sung | Knowledge, KnowledgeCard | CardKnowledge |
| Phụ lục | Appendix notes | Body / Note — not a loud card |
| — | EmptyStateCard / ErrorStateCard | CardEmpty / CardError |

---

## Shared controls

| Control | Appears in |
|---------|------------|
| PrimaryButton | Định hướng chính (once) |
| SecondaryButton | Optional milestone / domain deepen |
| ExpandCollapseControl | Rec, analysis, charts table, technical, knowledge |
| Tag | Domain + status |
| InPageNav | Optional all breakpoints |
| SkipToContent | All breakpoints |

---

## Priority overlay

| Component | Priority band |
|-----------|---------------|
| Hero, ExecutiveSummary, Recommendation | P1 |
| Warnings + Domain* | P2 |
| Charts | P3 |
| TechnicalInfo, Knowledge, Appendix | P4 |

---

## Future code mapping note

When implementation is authorized, bind these names to Design System Zone → Row → Grid → Card primitives.

Do not create a second visual system.

---

END
