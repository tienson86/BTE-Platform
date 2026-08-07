# 07_PRIORITY_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

Component: Priority Engine

---

# 1. Purpose

The Priority Engine is responsible for resolving competing analytical evidence before score calculation.

It determines which analytical conclusions have precedence when multiple valid rules produce different outcomes.

The Priority Engine never performs rule matching.

The Priority Engine never calculates scores.

The Priority Engine never generates interpretation.

---

# 2. Position in Runtime

AnalysisContext

↓

Rule Matcher

↓

Evidence Engine

↓

Priority Engine

↓

Score Calculator

↓

AnalysisResult

---

# 3. Priority Philosophy

Multiple rules may match simultaneously.

The Priority Engine decides

which evidence

is

Applied

Suppressed

Deferred

Merged

Every decision must be deterministic.

---

# 4. Responsibilities

The Priority Engine is responsible for

✓ Conflict detection

✓ Rule prioritization

✓ Evidence prioritization

✓ Merge strategy

✓ Suppression strategy

✓ Decision trace

The Priority Engine is NOT responsible for

✗ Rule Matching

✗ Score Calculation

✗ Interpretation

✗ Report Rendering

---

# 5. Runtime Flow

Evidence Collection

↓

Conflict Detection

↓

Priority Resolution

↓

Merge

↓

Decision Trace

↓

Prioritized Evidence

---

# 6. Input

Consumes

EvidenceCollection

Each Evidence contains

Rule

Weight

Priority Hint

Fact Snapshot

Reasoning Chain

Metadata

---

# 7. Output

Produces

PrioritizedEvidenceCollection

Each Evidence receives

Applied

Suppressed

Merged

Deferred

Every decision is preserved.

---

# 8. Priority Dimensions

Priority is evaluated using multiple dimensions.

Rule Priority

Knowledge Priority

Evidence Weight

Evidence Quality

Rule Specificity

Context Specificity

Confidence Hint

Domain Priority

No single factor determines priority.

---

# 9. Conflict Detection

Supported conflicts

Strength

Pattern

Useful God

Ten Gods

Five Elements

Shen Sha

Luck

Overall Analysis

Every conflict is recorded.

---

# 10. Resolution Strategies

Supported strategies

KEEP

Discard lower priority evidence.

MERGE

Combine evidence.

DEFER

Keep for downstream processing.

SUPPRESS

Keep trace but remove analytical influence.

Every strategy is explicit.

---

# 11. Priority Rules

Priority rules are loaded from

Priority Rule Database.

Examples

Follow Pattern

>

Normal Pattern

Season Rule

>

Minor Rule

Core Rule

>

Supplementary Rule

Priority rules are versioned.

---

# 12. Decision Trace

Every decision records

Decision ID

Evidence IDs

Winning Rule

Suppressed Rules

Resolution Strategy

Reason

Timestamp

Trace ID

Every decision is auditable.

---

# 13. Merge Policy

Merge is allowed only when

Evidence is compatible.

Merged Evidence

preserves

all source Evidence IDs.

No Evidence is discarded silently.

---

# 14. Suppression Policy

Suppressed Evidence

remains inside

Decision Trace.

Suppressed Evidence

never affects scoring.

Suppression is reversible for debugging.

---

# 15. Deferred Evidence

Deferred Evidence

is preserved

for downstream inspection.

Deferred Evidence

does not influence the current analysis.

---

# 16. Priority Metadata

Every decision stores

Priority Version

Decision Engine Version

Execution Time

Applied Strategy

Knowledge Version

Metadata supports auditing.

---

# 17. Error Handling

Possible errors

ConflictResolutionError

PriorityRuleError

MergeError

MetadataError

InternalError

Errors return

Result.Error

---

# 18. Performance

Target

10,000 Evidence Objects

↓

Priority Resolution

<50 ms

Supports parallel execution.

---

# 19. Thread Safety

The Priority Engine is

✓ Stateless

✓ Deterministic

✓ Immutable

✓ Thread-safe

---

# 20. Downstream Contract

Produces

PrioritizedEvidenceCollection

Consumed by

Score Calculator

Analysis Builder

No downstream component

re-evaluates priority.

---

# 21. Acceptance Criteria

The Priority Engine is complete when

✓ Conflicts detected

✓ Priorities resolved

✓ Merge supported

✓ Suppression supported

✓ Decision Trace preserved

✓ Metadata complete

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT