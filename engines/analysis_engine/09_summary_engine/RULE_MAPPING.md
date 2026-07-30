# Summary Engine Rule Mapping

**Module:** `engines/analysis_engine/09_summary_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Rule Mapping Specification)

---

# 1. Purpose

This document defines how Summary Engine maps upstream analytical outputs into consolidated summary structures.

Summary Engine does not consume domain Knowledge Modules for recomputation.

Mapping is structural aggregation of published StageResults.

---

# 2. Mapping Principle

```text
Upstream StageResult  →  Summary View  →  SummaryResult field
```

---

# 3. Stage → Summary Mapping

| Upstream Result | Summary View | SummaryResult Section |
|-----------------|--------------|----------------------|
| StrengthResult | StrengthSummaryView | strength_summary |
| TemperatureResult | TemperatureSummaryView | temperature_summary |
| PatternResult | PatternSummaryView | pattern_summary |
| UsefulGodResult | UsefulGodSummaryView | useful_god_summary |
| TenGodsResult | TenGodsSummaryView | ten_gods_summary |
| CombinationResult | CombinationSummaryView | combination_summary |
| ShenShaResult | ShenShaSummaryView | shensha_summary |
| LuckResult | LuckSummaryView | luck_summary |

Exact field names remain backward compatible within V1.x once published.

---

# 4. Evidence Mapping

| Source | Target |
|--------|--------|
| Upstream KnowledgeReferences | EvidenceIndex entries |
| Upstream RuleEvidence | EvidenceIndex entries |
| Upstream confidence fields | ConsolidatedConfidenceSummary inputs |

Evidence is preserved by reference; upstream evidence payloads are not altered.

---

# 5. Consistency Mapping

Cross-stage consistency rules map to:

- CrossStageConsistencyReport status
- diagnostics entries when inconsistencies are detected

---

# 6. Non-Mapping Rules

Summary Engine must not:

- map to domain Knowledge Modules for rule re-execution
- map narrative sentence libraries
- map report templates
- override upstream stage semantics

---

# 7. Acceptance Criteria

Rule Mapping is accepted when stage-to-summary mapping, evidence mapping, and non-mapping rules are complete.
