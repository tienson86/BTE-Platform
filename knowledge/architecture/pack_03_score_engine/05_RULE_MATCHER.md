# 05_RULE_MATCHER.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

Component: Rule Matcher

---

# 1. Purpose

The Rule Matcher is responsible for evaluating every canonical rule against the current AnalysisContext.

It determines whether a rule matches the current BaZi chart.

The Rule Matcher never performs scoring.

The Rule Matcher never performs interpretation.

The Rule Matcher never resolves conflicts.

---

# 2. Position in Runtime

AnalysisContext

↓

Rule Loader

↓

Rule Matcher

↓

MatchResult Collection

↓

Evidence Engine

↓

Priority Engine

↓

AnalysisResult

---

# 3. Matcher Philosophy

The Rule Matcher evaluates facts.

It does not evaluate conclusions.

Its responsibility is only to determine whether rule conditions are satisfied.

Every evaluation must be deterministic.

---

# 4. Responsibilities

The Rule Matcher is responsible for

✓ Rule evaluation

✓ Condition evaluation

✓ Fact extraction

✓ Evidence generation

✓ Match confidence calculation

✓ Execution trace

The Rule Matcher is NOT responsible for

✗ Priority

✗ Scoring

✗ Interpretation

✗ Report generation

---

# 5. Matching Pipeline

Rule

↓

Parse Conditions

↓

Extract Facts

↓

Evaluate Conditions

↓

Generate MatchResult

↓

Evidence Engine

---

# 6. Rule Input

Each Rule contains

Rule ID

Conditions

Priority

Metadata

Evidence Template

No executable business logic.

---

# 7. Runtime Input

The Rule Matcher consumes

AnalysisContext

AnalysisContext contains

- BaziChart

- RuleSet

- Runtime Metadata

- Execution Context

No downstream information.

---

# 8. Match States

Every rule evaluation returns one state.

MATCHED

Condition fully satisfied.

PARTIAL_MATCH

Some conditions satisfied.

NOT_MATCHED

Conditions not satisfied.

SKIPPED

Rule intentionally skipped.

ERROR

Evaluation failed.

Match State is mandatory.

---

# 9. Condition Evaluation

Supported condition types

Equality

Comparison

Existence

Range

Collection

Relationship

Logical AND

Logical OR

Logical NOT

Nested Conditions

All conditions are declarative.

---

# 10. Fact Extraction

The matcher extracts

Day Master

Season

Elements

Relationships

Hidden Stems

Growth Phases

Na Yin

Ten Gods

Shen Sha

Facts remain immutable.

---

# 11. MatchResult

Each successful evaluation returns

Match ID

Rule ID

Match State

Matched Facts

Evidence

Confidence Hint

Execution Duration

Execution Order

Warnings

Metadata

MatchResult is immutable.

---

# 12. Partial Matching

Some rules may partially match.

Example

Three Harmony

Members Present

Yin

Wu

Members Missing

Xu

Result

PARTIAL_MATCH

Partial matches are recorded.

---

# 13. Confidence Hint

The matcher provides

confidence_hint

Range

0.0

↓

1.0

This is not the final confidence.

Final confidence belongs to

Confidence Calculator.

---

# 14. Evidence Template

Every MatchResult includes

Evidence Template

Example

Month Branch = Yin

Season = Spring

Fire Count = 5

Metal Root = Weak

Templates are canonical.

---

# 15. Match Trace

Every evaluation records

Rule

Condition

Facts

Result

Duration

Warnings

Trace ID

Supports debugging.

---

# 16. Error Handling

Possible errors

ConditionError

RuleError

FactError

KnowledgeError

RuntimeError

Errors return

MatchResult(ERROR)

Pipeline continues when possible.

---

# 17. Performance

Target

10,000 Rules

↓

<150 ms

Matcher supports parallel execution.

---

# 18. Thread Safety

The Rule Matcher is

✓ Stateless

✓ Immutable

✓ Deterministic

✓ Thread-safe

Parallel evaluation supported.

---

# 19. Rule Ordering

Rules are evaluated

independently.

Matching order

never changes

the MatchResult.

Ordering belongs to

Priority Engine.

---

# 20. Downstream Contract

Rule Matcher produces

MatchResult Collection

Evidence Engine consumes

MatchResult Collection

No downstream Engine

re-evaluates rule conditions.

---

# 21. Acceptance Criteria

The Rule Matcher is complete when

✓ Every rule evaluated

✓ Match States generated

✓ Evidence produced

✓ Match Trace recorded

✓ Partial Matches supported

✓ Confidence Hint generated

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT