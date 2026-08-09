# Expansion State Model

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Aligns with: PX-1 `EXPANSION_MODEL.md`

---

## 1. Stored flags (view state only)

| Flag | Default | Owner |
|------|---------|-------|
| `RecommendationModel.expanded` | false | RecommendationCard |
| `WarningModel.expanded` | false | WarningCard |
| `DomainModel.analysis_expanded` | false | AnalysisCard |
| `ChartModel.table_expanded` | false | ChartCard |
| `TechnicalModel.collapsed` | **true** | TechnicalInfo |
| Knowledge section collapsed | **true** | Knowledge |
| `KnowledgeModel.expanded` | false | KnowledgeCard |

These flags are **not** Report fields. They are UI state keyed by `id` / index.

---

## 2. Must stay open (not expandable away)

- Hero fields  
- Summary bullets  
- Rec Why / Expected Result / Action  
- Warning title + body  

---

## 3. Must start collapsed / hidden

- Rec detail  
- Analysis detail  
- Chart tables  
- Entire Technical section  
- Entire Knowledge section  

---

## 4. Independence

Opening one rec does not close others.  
Opening Technical does not open Knowledge.  
Expand never auto-opens on first load except mandated open surfaces.

---

## 5. Persistence

Not specified for PX-2. Default: reset on Dispose / page leave.

---

## 6. Accessibility

Every toggle exposes Vietnamese label + expanded/collapsed state (`COMPONENT_EVENT_MODEL.md`, PX-1 a11y).

---

## 7. Stop line

Expansion is view state. It does not mutate `report.*`.

END
