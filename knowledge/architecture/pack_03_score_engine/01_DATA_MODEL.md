# 01_DATA_MODEL.md

Version: 1.0

Status: CANONICAL

Pack: 03

Engine: Score Engine

---

# 1. Purpose

This document defines the canonical data model of the Score Engine.

The Score Engine exposes one canonical output model:

AnalysisResult

AnalysisResult is the Aggregate Root of the analytical domain.

All downstream Engines consume this Aggregate.

---

# 2. Design Principles

The AnalysisResult model follows these principles.

- Immutable
- Strongly Typed
- Canonical
- Versioned
- Explainable
- Traceable
- Serializable

Every analytical conclusion must be reproducible.

---

# 3. Canonical Input

Input

BaziChart

Produced by

BaZi Engine

BaziChart is immutable.

The Score Engine never modifies BaziChart.

---

# 4. Canonical Output

Output

AnalysisResult

AnalysisResult is immutable.

It becomes the single source of truth for every downstream Engine.

---

# 5. Aggregate Root

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

---

# 6. AnalysisMetadata

Metadata describing the analytical process.

| Field | Type | Description |
|--------|------|-------------|
| analysis_id | UUID | Unique analysis identifier |
| chart_id | UUID | Source BaziChart |
| version | string | Schema version |
| engine_version | string | Score Engine version |
| generated_at | datetime | Analysis time |
| duration_ms | number | Runtime duration |

---

# 7. StrengthAnalysis

Represents Day Master strength.

Contains

- Value
- Score
- Confidence
- Evidence
- Matched Rules

Possible Values

- Strong
- Weak
- Balanced
- Follow Strong
- Follow Weak

No interpretation text.

---

# 8. PatternAnalysis

Represents Pattern (Cách Cục).

Contains

- Pattern Name
- Pattern Category
- Score
- Confidence
- Evidence
- Rule Trace

Supports multiple candidate patterns.

Final selection is explicit.

---

# 9. UsefulGodAnalysis

Contains

Useful God

Favorable Elements

Unfavorable Elements

Seasonal Adjustment

Supporting Evidence

No natural language.

---

# 10. TenGodAnalysis

Contains analytical results for

- Direct Officer
- Seven Killings
- Direct Wealth
- Indirect Wealth
- Direct Resource
- Indirect Resource
- Eating God
- Hurting Officer
- Friend
- Rob Wealth

Each item contains

Value

Score

Confidence

Evidence

---

# 11. FiveElementAnalysis

Contains

Wood

Fire

Earth

Metal

Water

For every element

- Structural Score
- Seasonal Score
- Final Score
- Confidence

---

# 12. ShenShaAnalysis

Contains

Detected Shen Sha

Activation Status

Priority

Evidence

No interpretation.

---

# 13. LuckAnalysis

Contains structural analysis for

- Luck Cycle
- Annual Influence
- Current Context

Only analytical values.

No prediction text.

---

# 14. OverallAnalysis

Contains

Overall Score

Overall Confidence

Summary Code

Priority Summary

Risk Summary

OverallAnalysis is structured only.

---

# 15. EvidenceCollection

Stores all evidence generated during analysis.

Each Evidence contains

| Field | Description |
|--------|-------------|
| evidence_id | Unique identifier |
| source | Rule source |
| category | Strength / Pattern / etc. |
| description | Canonical explanation |
| weight | Numerical contribution |
| priority | Resolution priority |

Evidence is immutable.

---

# 16. RuleTrace

Stores execution trace.

Each record contains

- Rule ID
- Rule Version
- Matched
- Priority
- Applied
- Ignored
- Execution Order

RuleTrace allows complete auditability.

---

# 17. ConfidenceSummary

Contains confidence metrics.

Per analysis

Overall

Minimum

Maximum

Average

Confidence is normalized to

0.0 – 1.0

---

# 18. Model Relationships

BaziChart

↓

Rule Matching

↓

Evidence

↓

Priority

↓

Score

↓

AnalysisResult

The pipeline is deterministic.

---

# 19. Serialization

Supported formats

- JSON
- YAML
- MessagePack

Serialization must preserve every Aggregate member.

---

# 20. Versioning

Major

Breaking schema changes.

Minor

Backward-compatible additions.

Patch

Bug fixes.

AnalysisResult compatibility must be preserved.

---

# 21. Extension Rules

Future analysis modules may be added.

Examples

- CareerAnalysis
- MarriageAnalysis
- HealthAnalysis
- EducationAnalysis
- PersonalityAnalysis

Existing members must remain stable.

---

# 22. Downstream Contract

The following Engines consume

AnalysisResult

Interpretation Engine

Report Engine

AI Advisory Engine

No downstream Engine recalculates

Strength

Pattern

Useful God

Evidence

Scores

AnalysisResult is the canonical analytical source.

---

# 23. Aggregate Diagram

BaziChart

↓

Score Engine

↓

+--------------------------------------+
|          AnalysisResult              |
|--------------------------------------|
| AnalysisMetadata                     |
| StrengthAnalysis                     |
| PatternAnalysis                      |
| UsefulGodAnalysis                    |
| TenGodAnalysis                       |
| FiveElementAnalysis                  |
| ShenShaAnalysis                      |
| LuckAnalysis                         |
| OverallAnalysis                      |
| EvidenceCollection                   |
| RuleTrace                            |
| ConfidenceSummary                    |
+--------------------------------------+

↓

Interpretation Engine

↓

Report Engine

---

# 24. Source of Truth

AnalysisResult is the only analytical representation within the BTE Platform.

Every downstream Engine consumes AnalysisResult.

No downstream Engine reconstructs analytical conclusions independently.

The Score Engine is the canonical source of analytical truth.

---

END OF DOCUMENT