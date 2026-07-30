# Useful God Engine Algorithm

**Module:** `engines/analysis_engine/04_useful_god_engine`  
**Version:** V1.0.0  
**Status:** Frozen (Algorithm Specification)

---

# 1. Purpose

This document specifies the analytical algorithm executed by the Useful God Engine.

The algorithm is deterministic and rule-driven.

---

# 2. Algorithm Objectives

The algorithm shall:

- evaluate strength, climate, and pattern requirements as Useful God inputs;
- generate and evaluate Useful God candidates;
- resolve conflicts and priority contests;
- determine Yong Shen, Xi Shen, Ji Shen, and Xian Shen;
- calculate confidence;
- produce a reproducible UsefulGodResult.

---

# 3. Processing Algorithm

```text
Receive AnalysisContext

↓

Validate Context

↓

Read StrengthResult from AnalysisContext

↓

Read TemperatureResult from AnalysisContext

↓

Read PatternResult from AnalysisContext

↓

Load Useful God Rules

↓

Generate Candidates

↓

Evaluate Candidates

↓

Resolve Priority

↓

Determine Yong Shen

↓

Determine Xi Shen

↓

Determine Ji Shen

↓

Determine Xian Shen

↓

Calculate Confidence

↓

Build Immutable UsefulGodResult

↓

Publish UsefulGodResult
```

---

# 4. Analytical Dimensions

Each dimension is evaluated independently before candidate aggregation.

Dimensions include:

- Strength Balance
- Climate Balance
- Pattern Requirements
- Five-Element Equilibrium
- Supporting and Controlling Relationships
- Adjustment Priorities
- Primary Candidates
- Secondary Candidates
- Alternative Candidates

No dimension may directly modify another.

---

# 5. Candidate Generation

The algorithm shall generate candidates from all applicable Useful God categories.

Candidate generation shall:

1. Collect eligible matches from each category analyzer.
2. Preserve candidate rank class (primary, secondary, alternative).
3. Preserve matched-rule evidence.
4. Form an immutable UsefulGodCandidateSet.

---

# 6. Candidate Evaluation

The algorithm shall evaluate each candidate using:

- Useful God Rules
- Strength balance evidence
- Climate balance evidence
- Pattern requirement evidence
- Equilibrium and relation evidence
- Upstream StrengthResult, TemperatureResult, and PatternResult evidence where required

Evaluation produces deterministic CandidateEvaluation records.

---

# 7. Priority and Conflict Resolution

The algorithm shall:

1. Apply Conflict Resolution Rules.
2. Apply Candidate Priority Rules.
3. Select Yong Shen, Xi Shen, Ji Shen, and Xian Shen assignments.
4. Record rejected candidates and resolution evidence.

Resolution order shall remain stable.

---

# 8. Confidence Algorithm

Confidence is determined using:

- Rule coverage
- Data completeness
- Rule consistency
- Analytical agreement
- Candidate separation quality
- Upstream StrengthResult, TemperatureResult, and PatternResult completeness where required by Useful God Rules

Confidence shall be independent of narrative interpretation.

---

# 9. Tie Resolution

When multiple rule outcomes or candidates have equal priority:

1. Apply the official Candidate Priority Rules.
2. Preserve deterministic ordering.
3. Record the resolution path.

---

# 10. Explainability

Every output decision shall reference:

- contributing analyzers and determiners;
- matched rules;
- rejected candidates;
- score contributions;
- supporting evidence;
- upstream StrengthResult, TemperatureResult, and PatternResult evidence when consumed.

---

# 11. Complexity Targets

Target characteristics:

- Linear processing with respect to the number of applicable rules and candidates.
- Stateless execution.
- Minimal memory allocation.
- Cache-friendly rule access.

---

# 12. Algorithm Constraints

The algorithm shall never:

- infer undocumented rules;
- modify Useful God Rule Database Knowledge Module contents;
- recompute Strength, Temperature, or Pattern;
- invoke downstream engines;
- produce non-deterministic results;
- hard-code a physical repository path to the Rule Database.

---

# 13. Acceptance Criteria

The algorithm is accepted when:

- identical inputs produce identical outputs;
- all analytical dimensions execute successfully;
- competing candidates are evaluated and resolved;
- Yong Shen, Xi Shen, Ji Shen, and Xian Shen are determined;
- confidence is calculated;
- rejected candidates are recorded;
- all matched rules are traceable;
- UsefulGodResult is reproducible.
