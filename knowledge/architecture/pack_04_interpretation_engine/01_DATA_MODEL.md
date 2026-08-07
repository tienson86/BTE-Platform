# 01_DATA_MODEL.md

Version: 1.0

Status: CANONICAL

Pack: 04

Engine: Interpretation Engine

---

# 1. Purpose

This document defines the canonical data model of the Interpretation Engine.

The Interpretation Engine exposes one canonical output model.

InterpretationResult

InterpretationResult is the Aggregate Root of the interpretation domain.

Every downstream rendering engine consumes this Aggregate.

---

# 2. Design Principles

InterpretationResult follows these principles.

- Immutable
- Strongly Typed
- Canonical
- Versioned
- Localizable
- Explainable
- Traceable
- Serializable

The Interpretation Engine never modifies analytical conclusions.

---

# 3. Canonical Input

Input

AnalysisResult

Produced by

Score Engine

AnalysisResult is immutable.

The Interpretation Engine never modifies AnalysisResult.

---

# 4. Canonical Output

Output

InterpretationResult

InterpretationResult is immutable.

It becomes the single narrative source for downstream rendering.

---

# 5. Aggregate Root

InterpretationResult

contains

InterpretationMetadata

OverviewSection

StrengthSection

PatternSection

UsefulGodSection

TenGodSection

FiveElementSection

ShenShaSection

LuckSection

SummarySection

NarrativeTree

ReferenceCollection

TraceCollection

---

# 6. InterpretationMetadata

Metadata describing the interpretation process.

| Field | Type | Description |
|--------|------|-------------|
| interpretation_id | UUID | Unique identifier |
| analysis_id | UUID | Source AnalysisResult |
| version | string | Schema version |
| engine_version | string | Interpretation Engine version |
| language | string | Active language |
| generated_at | datetime | Generation timestamp |
| duration_ms | number | Runtime duration |

---

# 7. Interpretation Sections

Each analytical domain becomes one section.

Supported sections

Overview

Strength

Pattern

Useful God

Ten Gods

Five Elements

Shen Sha

Luck

Summary

Sections remain independent.

---

# 8. Narrative Tree

NarrativeTree is the canonical narrative structure.

Hierarchy

Section

↓

Paragraph

↓

Sentence

↓

Fragment

NarrativeTree replaces plain text.

---

# 9. Section Model

Every Section contains

Section ID

Title

Paragraphs

Summary

References

Metadata

Visibility

Sections are immutable.

---

# 10. Paragraph Model

Every Paragraph contains

Paragraph ID

Sentences

Importance

Display Order

References

Metadata

Paragraphs never contain analysis logic.

---

# 11. Sentence Model

Every Sentence contains

Sentence ID

Template ID

Rendered Text

Placeholder Values

Evidence References

Analysis References

Confidence

Metadata

Sentence is the smallest narrative unit.

---

# 12. Fragment Model

Fragments represent reusable text pieces.

Examples

Day Master

Useful God

Pattern Name

Season

Five Elements

Fragments support localization.

---

# 13. Placeholder Collection

Stores all runtime placeholder values.

Examples

{{day_master}}

{{pattern_name}}

{{useful_god}}

{{strength}}

{{season}}

Placeholder values remain structured.

---

# 14. Reference Collection

Stores references to

Analysis Nodes

Evidence

Rule Trace

Confidence

References support explainability.

---

# 15. Trace Collection

Stores

Sentence Trace

Template Trace

Placeholder Trace

Builder Trace

Runtime Trace

Every generated sentence is traceable.

---

# 16. Localization Model

Supports

Language

Locale

Writing Style

Terminology Profile

Localization never changes meaning.

---

# 17. Serialization

Supported formats

JSON

YAML

MessagePack

Serialization preserves every Aggregate member.

---

# 18. Versioning

Major

Breaking schema changes.

Minor

Backward-compatible additions.

Patch

Bug fixes.

InterpretationResult compatibility must be preserved.

---

# 19. Extension Rules

Future sections may be added.

Examples

Career

Marriage

Health

Education

Children

Personality

Extensions never break existing sections.

---

# 20. Downstream Contract

The following Engines consume

InterpretationResult

Report Engine

Desktop UI

Tablet UI

Mobile UI

Voice Engine

AI Rewrite Engine

No downstream Engine regenerates interpretation.

---

# 21. Aggregate Diagram

AnalysisResult

↓

Interpretation Engine

↓

+--------------------------------------+
|      InterpretationResult            |
|--------------------------------------|
| InterpretationMetadata               |
| OverviewSection                      |
| StrengthSection                      |
| PatternSection                       |
| UsefulGodSection                     |
| TenGodSection                        |
| FiveElementSection                   |
| ShenShaSection                       |
| LuckSection                          |
| SummarySection                       |
| NarrativeTree                        |
| ReferenceCollection                  |
| TraceCollection                      |
+--------------------------------------+

↓

Report Engine

---

# 22. Source of Truth

InterpretationResult is the only narrative representation within the BTE Platform.

Every downstream rendering engine consumes InterpretationResult.

No downstream component regenerates interpretation.

The Interpretation Engine is the canonical source of narrative output.

---

END OF DOCUMENT