# 03_PUBLIC_API.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

---

# 1. Purpose

This document defines the canonical Public API of the Score Engine.

The Score Engine exposes one official service responsible for transforming a canonical BaziChart into a canonical AnalysisResult.

All analytical processing remains internal.

---

# 2. API Philosophy

The Score Engine exposes one public service.

Consumers never execute:

- Rule Loader
- Rule Matcher
- Evidence Engine
- Conflict Resolver
- Priority Engine
- Score Calculator

directly.

All analytical logic is encapsulated inside the Engine.

---

# 3. Public Service

Canonical Service

ScoreEngine

Responsibilities

- Validate input
- Execute inference pipeline
- Produce AnalysisResult
- Return structured execution result

---

# 4. Public Entry Point

ScoreEngine.run()

Input

BaziChart

↓

Output

Result<AnalysisResult>

This is the only supported public API.

---

# 5. Input Contract

Input Model

BaziChart

Produced only by

BaZi Engine

Requirements

✓ Canonical

✓ Immutable

✓ Fully validated

The Score Engine never accepts

- JSON
- Dictionary
- Anonymous Objects

Only canonical BaziChart.

---

# 6. Output Contract

Output

Result<AnalysisResult>

Possible states

Success

↓

AnalysisResult

Warning

↓

AnalysisResult + Warnings

Failure

↓

Structured Error

Partial analysis is never returned.

---

# 7. Result Model

Result<T>

contains

success

value

warnings

error

metadata

trace

Result<T> is immutable.

Null is never returned.

---

# 8. Public Aggregate

AnalysisResult

contains

AnalysisMetadata

StrengthAnalysis

PatternAnalysis

UsefulGodAnalysis

TenGodAnalysis

FiveElementAnalysis

ShenShaAnalysis

LuckAnalysis

OverallAnalysis

EvidenceCollection

RuleTrace

ConfidenceSummary

No downstream Engine may modify AnalysisResult.

---

# 9. Internal Components

The following components are private.

AnalysisContextBuilder

RuleLoader

RuleMatcher

EvidenceCollector

ConflictResolver

PriorityEngine

ScoreCalculator

ConfidenceCalculator

AnalysisBuilder

ValidationEngine

These components are implementation details.

They are never exposed outside the Score Engine.

---

# 10. Dependency Rules

Allowed

BaziChart

Canonical Rule Database

Utilities

Forbidden

Calendar Engine

BaZi Builder Components

Interpretation Engine

Report Engine

Desktop UI

Mobile UI

The Score Engine consumes only BaziChart and Rule Database.

---

# 11. Runtime Ownership

The Score Engine owns

- Rule execution
- Evidence collection
- Conflict resolution
- Priority resolution
- Score calculation
- Confidence calculation
- Analysis construction

No downstream Engine recalculates analytical logic.

---

# 12. Error Model

Possible errors

ValidationError

RuleLoadError

RuleMatchError

EvidenceError

PriorityError

ScoringError

AnalysisError

InternalError

Every error contains

- code
- stage
- component
- message
- timestamp
- engine_version
- trace_id

---

# 13. Warning Model

Warnings do not terminate execution.

Examples

- Deprecated rule
- Low confidence
- Multiple valid candidates
- Ambiguous pattern

Warnings are attached to Result<AnalysisResult>.

---

# 14. Traceability

Every execution produces

Execution Trace

including

- Loaded Rules
- Matched Rules
- Ignored Rules
- Conflict Resolution
- Priority Decisions
- Final Scores

Trace data supports debugging and auditing.

---

# 15. Thread Safety

The Score Engine is

✓ Stateless

✓ Deterministic

✓ Thread-safe

✓ Immutable

Parallel execution is fully supported.

---

# 16. Performance

Target

Single Analysis

<150 ms

100 Analyses

<2 seconds

1000 Analyses

<15 seconds

No external network dependency.

---

# 17. Semantic Versioning

The Public API follows Semantic Versioning.

Major

Breaking API changes

Minor

Backward-compatible additions

Patch

Bug fixes

Breaking changes require Architecture Review.

---

# 18. Integration Example

BaziChart

↓

ScoreEngine.run()

↓

Result<AnalysisResult>

↓

InterpretationEngine.run()

↓

Result<InterpretationResult>

The Score Engine never invokes downstream Engines.

---

# 19. Extension Rules

Future internal components may be added.

Examples

- AI Rule Engine
- Dynamic Rule Engine
- School Adapter
- Optimization Engine

Extensions remain internal.

The Public API remains unchanged.

---

# 20. API Stability

The Public API is considered stable when

Input remains

BaziChart

Output remains

Result<AnalysisResult>

Internal implementation may evolve without affecting consumers.

---

# 21. Acceptance Criteria

The Public API is complete when

✓ One public service

✓ One public entry point

✓ One canonical input

✓ One canonical output

✓ AnalysisResult Aggregate returned

✓ Internal components hidden

✓ Strong typing enforced

✓ Thread-safe

✓ Fully documented

---

END OF DOCUMENT