# 06_EVIDENCE_ENGINE.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

Component: Evidence Engine

---

# 1. Purpose

The Evidence Engine is responsible for transforming matched analytical rules into structured reasoning evidence.

It provides the factual foundation for every analytical conclusion.

Every conclusion in the Score Engine must be supported by evidence.

No analytical result may exist without traceable evidence.

---

# 2. Position in Runtime

AnalysisContext

↓

Rule Loader

↓

Rule Matcher

↓

Evidence Engine

↓

Conflict Resolver

↓

Priority Engine

↓

Score Calculator

↓

AnalysisResult

---

# 3. Evidence Philosophy

Evidence represents facts.

Evidence never represents interpretation.

Evidence never represents opinion.

Evidence answers

WHY

a rule matched.

---

# 4. Responsibilities

The Evidence Engine is responsible for

✓ Building Evidence

✓ Grouping Evidence

✓ Weighting Evidence

✓ Linking Evidence

✓ Building Reasoning Chains

✓ Preserving Fact Snapshot

The Evidence Engine never

✗ Calculates Scores

✗ Resolves Conflicts

✗ Produces Interpretation

---

# 5. Runtime Flow

MatchResult Collection

↓

Evidence Builder

↓

Evidence Grouping

↓

Evidence Weighting

↓

Evidence Linking

↓

Reasoning Chain

↓

Evidence Collection

---

# 6. Input

Input

MatchResult Collection

Each MatchResult contains

- Rule ID
- Match State
- Fact Snapshot
- Confidence Hint
- Metadata

---

# 7. Evidence Model

Every Evidence contains

Evidence ID

Rule ID

Category

Evidence Type

Fact Snapshot

Evidence Weight

Priority Hint

Metadata

Reasoning Node

Evidence is immutable.

---

# 8. Evidence Categories

Supported categories

Strength

Pattern

Useful God

Ten Gods

Five Elements

Shen Sha

Luck

Overall

Future categories may be added.

---

# 9. Evidence Types

Supported evidence types

Direct Evidence

Indirect Evidence

Supporting Evidence

Conflicting Evidence

Derived Evidence

Context Evidence

Every Evidence has one type.

---

# 10. Fact Snapshot

Every Evidence stores

the exact facts

used during matching.

Example

Day Master

Month Branch

Season

Element Counts

Relationships

Hidden Stems

Growth Phase

The Snapshot never changes.

---

# 11. Evidence Weight

Every Evidence contains

Weight

Range

0.0

↓

1.0

Weight measures

analytical importance.

Weight is not the final score.

---

# 12. Reasoning Chain

Evidence is connected into

Reasoning Chains.

Example

Season

↓

Weak Root

↓

Low Metal Support

↓

Weak Day Master

↓

Strength Analysis

Every node remains traceable.

---

# 13. Evidence Linking

Evidence may reference

Supporting Evidence

Parent Evidence

Child Evidence

Related Evidence

Relationship links never create cycles.

---

# 14. Evidence Collection

EvidenceCollection contains

All Evidence

Grouped Evidence

Reasoning Chains

Metadata

Collection is immutable.

---

# 15. Evidence Metadata

Every Evidence stores

Evidence Version

Builder

Timestamp

Execution Order

Rule Version

Knowledge Source

Metadata supports auditing.

---

# 16. Evidence Trace

Every Evidence records

Origin Rule

Matched Facts

Builder

Execution Duration

Warnings

Trace ID

Evidence Trace supports debugging.

---

# 17. Error Handling

Possible errors

EvidenceBuildError

EvidenceLinkError

SnapshotError

MetadataError

RuntimeError

Errors return

Result.Error

---

# 18. Performance

Target

10,000 Evidence Objects

↓

<50 ms

Evidence generation supports parallel execution.

---

# 19. Thread Safety

The Evidence Engine is

✓ Stateless

✓ Deterministic

✓ Immutable

✓ Thread-safe

Parallel execution supported.

---

# 20. Downstream Contract

The Evidence Engine produces

EvidenceCollection

Consumed by

Conflict Resolver

Priority Engine

Analysis Builder

Interpretation Engine

No downstream Engine recreates evidence.

---

# 21. Acceptance Criteria

The Evidence Engine is complete when

✓ Every MatchResult produces Evidence

✓ Fact Snapshot preserved

✓ Evidence Weight assigned

✓ Evidence Links created

✓ Reasoning Chains completed

✓ Metadata preserved

✓ Thread-safe

✓ Deterministic

✓ Performance targets achieved

✓ Documentation approved

---

END OF DOCUMENT