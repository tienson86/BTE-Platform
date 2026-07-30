# Summary Engine Algorithm

**Module:** `engines/analysis_engine/09_summary_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document defines the logical algorithm of Summary consolidation.

It does not provide implementation source code.

---

# 2. Algorithm Principles

- Deterministic
- Non-mutating
- Non-recomputing
- Consistency-aware
- Explainability-preserving
- Fail-closed on incomplete upstream sets

---

# 3. Logical Algorithm

```text
1. Validate AnalysisContext
2. Read all eight upstream StageResults
3. Verify completeness of mandatory stage results
4. Run cross-stage consistency checks
5. Build StrengthSummaryView from StrengthResult
6. Build TemperatureSummaryView from TemperatureResult
7. Build PatternSummaryView from PatternResult
8. Build UsefulGodSummaryView from UsefulGodResult
9. Build TenGodsSummaryView from TenGodsResult
10. Build CombinationSummaryView from CombinationResult
11. Build ShenShaSummaryView from ShenShaResult
12. Build LuckSummaryView from LuckResult
13. Consolidate confidence across stages
14. Build unified EvidenceIndex from upstream evidence
15. Assemble SummaryResult with diagnostics
16. Return immutable result
```

---

# 4. Aggregation Rules

- Summary views are projections/indexes, not recomputations.
- Upstream semantic values are referenced, not overridden.
- Conflicting upstream classifications are surfaced in consistency report; they are not silently resolved by rewriting upstream data.
- Missing mandatory upstream result aborts aggregation.

---

# 5. Cross-Stage Consistency

Consistency checks validate declared relationships among published stage outcomes.

Examples of logical consistency classes (contract-level, not implementation):

- structural facts referenced by multiple stages align
- no contradictory required identity claims across stages
- confidence/evidence references remain traceable

Exact consistency rules are defined in VALIDATION.md.

---

# 6. Confidence Consolidation

Consolidated confidence aggregates upstream confidence indicators using deterministic summary policy.

Summary confidence does not replace stage-level confidence inside upstream results.

---

# 7. Evidence Index

EvidenceIndex collects KnowledgeReferences / RuleEvidence from all upstream stages without deduplication that loses traceability.

---

# 8. Complexity Constraints

Aggregation is linear in the number of upstream stages and evidence entries.

Unbounded recomputation or re-matching of domain rules is forbidden.

---

# 9. Acceptance Criteria

Algorithm is accepted when logical steps, aggregation rules, and non-recomputation guarantees are complete and implementation-free.
