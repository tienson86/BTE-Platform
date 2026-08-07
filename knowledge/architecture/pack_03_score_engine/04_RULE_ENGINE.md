# 04_RULE_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

Component: Rule Engine

---

# 1. Purpose

The Rule Engine is responsible for executing the canonical analytical knowledge of the BTE Platform.

Its responsibility is to evaluate the canonical Rule Database against a canonical BaziChart and produce structured rule execution results.

The Rule Engine never performs interpretation.

The Rule Engine never renders reports.

The Rule Engine never modifies the BaziChart.

---

# 2. Position in Runtime

BaziChart

↓

Analysis Context

↓

Rule Engine

↓

Matched Rules

↓

Evidence Engine

↓

Priority Engine

↓

AnalysisResult

---

# 3. Rule Engine Philosophy

The Rule Engine executes knowledge.

It never stores business logic inside source code.

Knowledge belongs to the Rule Database.

The Engine only executes.

---

# 4. Responsibilities

The Rule Engine is responsible for

✓ Loading rules

✓ Validating rules

✓ Matching rules

✓ Producing RuleMatchResult

✓ Recording execution trace

✓ Recording execution metadata

The Rule Engine is NOT responsible for

✗ Priority resolution

✗ Score calculation

✗ Interpretation

✗ Report generation

---

# 5. Rule Lifecycle

Every rule follows the same lifecycle.

Load

↓

Validate

↓

Match

↓

Generate Evidence

↓

Return RuleMatchResult

Rules never skip lifecycle stages.

---

# 6. Canonical Rule Structure

Every rule contains

Rule ID

Rule Name

Rule Category

Priority

Conditions

Actions

Evidence Template

Metadata

Version

Rules are immutable.

---

# 7. Rule Categories

The canonical Rule Database contains

Strength Rules

Pattern Rules

Useful God Rules

Ten God Rules

Five Element Rules

Shen Sha Rules

Luck Rules

Special Rules

Future rule categories may be added.

---

# 8. Rule Loader

Responsibilities

Load canonical rules.

Validate schema.

Cache immutable rules.

Prepare execution context.

The Rule Loader never evaluates rules.

---

# 9. Rule Validator

Every rule must satisfy

✓ Valid identifier

✓ Valid category

✓ Valid condition tree

✓ Valid evidence template

✓ Valid priority

✓ Version information

Invalid rules are rejected before execution.

---

# 10. Rule Matcher

The Rule Matcher evaluates every rule.

Possible outcomes

Matched

Not Matched

Skipped

Error

No scoring occurs here.

---

# 11. RuleMatchResult

Every matched rule produces

Rule ID

Match Status

Evidence

Matched Facts

Priority

Confidence Hint

Execution Order

Execution Duration

RuleMatchResult is immutable.

---

# 12. Rule Conditions

Conditions are declarative.

Examples

DayMaster == Metal

MonthBranch == Yin

Season == Spring

Element.Fire.Count > 4

Relationship.Exists("three_harmony")

Conditions must never contain implementation code.

---

# 13. Rule Actions

Actions never produce interpretation.

Actions only generate

Evidence

Tags

Flags

Candidate Scores

Metadata

Actions never modify the BaziChart.

---

# 14. Rule Metadata

Every rule contains

Author

Version

Created Date

Updated Date

Knowledge Source

School

Priority

Confidence Weight

Metadata supports auditing.

---

# 15. Rule Versioning

Semantic Versioning

Major

Breaking knowledge changes.

Minor

New compatible rules.

Patch

Corrections.

Every RuleMatchResult records the rule version used.

---

# 16. Rule Execution Order

Load Rules

↓

Validate Rules

↓

Match Rules

↓

Generate RuleMatchResult

↓

Evidence Engine

Execution order is deterministic.

---

# 17. Error Handling

Possible errors

RuleLoadError

RuleValidationError

RuleExecutionError

ConditionError

MetadataError

Errors return

Result.Error

No partial rule execution.

---

# 18. Performance

Target

10,000 Rules

↓

<100 ms loading

↓

<150 ms execution

Rule execution must support caching.

---

# 19. Thread Safety

Rule Engine is

✓ Stateless

✓ Deterministic

✓ Immutable

✓ Thread-safe

Parallel execution is supported.

---

# 20. Rule Cache

Rules are loaded once.

The Rule Cache is immutable.

Rule execution never modifies cached rules.

Cache invalidation occurs only when the Rule Database version changes.

---

# 21. Downstream Contract

The Rule Engine produces

RuleMatchResult

The Evidence Engine consumes RuleMatchResult.

The Rule Engine never communicates directly with

Priority Engine

Interpretation Engine

Report Engine

---

# 22. Acceptance Criteria

The Rule Engine is complete when

✓ Rules loaded

✓ Rules validated

✓ Rules matched

✓ RuleMatchResult generated

✓ Rule metadata preserved

✓ Execution trace recorded

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT