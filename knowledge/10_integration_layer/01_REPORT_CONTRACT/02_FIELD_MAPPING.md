# ReportResponse Field Mapping

**Location**

```
knowledge/10_integration_layer/01_REPORT_CONTRACT/02_FIELD_MAPPING.md
```

---

# Purpose

This document defines the canonical mapping between every ReportResponse section and its upstream data sources.

It is the Single Source of Truth (SSOT) for data ownership across the BTE Platform.

Every ReportResponse field must have:

- exactly one owner
- one primary source
- one builder
- one presentation responsibility

---

# Status

Document Type

Architecture Specification

Status

Frozen after Contract Approval

Commercial Version

RC1

Owner

BTE Architecture

---

# Mapping Principles

Every field shall define

- Source Engine
- Builder
- Integration Responsibility
- Portal Consumer
- Required/Optional
- Traceability
- Export Support

---

# End-to-End Data Lineage

```
Customer Input

↓

Calendar Engine

↓

BaZi Engine

↓

Analysis Engine

↓

Interpretation Engine

↓

Commercial Knowledge

↓

Integration Layer

↓

ReportResponse

↓

Customer Portal
```

---

# Field Mapping Matrix

| ReportResponse Section | Primary Source | Secondary Source | Builder | Required | Portal | PDF | Traceable |
|------------------------|----------------|------------------|----------|----------|--------|-----|-----------|
| metadata | Applications API | - | Report Builder | YES | NO | YES | NO |
| customer | Input Layer | - | Report Builder | YES | YES | YES | YES |
| chart | BaZi Engine | Calendar Engine | Report Builder | YES | YES | YES | YES |
| executive_summary | Interpretation Engine | Commercial Knowledge | Executive Builder | YES | YES | YES | YES |
| identity | Commercial Knowledge | Interpretation | Identity Builder | YES | YES | YES | YES |
| strengths | Analysis Engine | Commercial Knowledge | Strength Builder | YES | YES | YES | YES |
| weaknesses | Analysis Engine | Commercial Knowledge | Weakness Builder | YES | YES | YES | YES |
| useful_god | Analysis Engine | Commercial Knowledge | UsefulGod Builder | YES | YES | YES | YES |
| recommendations | Interpretation Engine | Commercial Knowledge | Recommendation Builder | YES | YES | YES | YES |
| domains | Commercial Knowledge | Interpretation | Domain Builder | OPTIONAL | YES | YES | YES |
| evidence | Analysis Engine | Rule Database | Evidence Builder | YES | Expand | YES | YES |
| charts | Analysis Engine | Chart Engine | Chart Builder | OPTIONAL | YES | YES | NO |
| knowledge | Commercial Knowledge | Knowledge DB | Knowledge Builder | OPTIONAL | Expand | YES | YES |
| appendix | Report Builder | - | Appendix Builder | OPTIONAL | NO | YES | NO |
| diagnostics | Integration Layer | Validation | Diagnostics Builder | OPTIONAL | NO | NO | YES |

---

# Builder Ownership

| Builder | Owns |
|----------|------|
| Executive Builder | executive_summary |
| Identity Builder | identity |
| Strength Builder | strengths |
| Weakness Builder | weaknesses |
| UsefulGod Builder | useful_god |
| Recommendation Builder | recommendations |
| Domain Builder | domains |
| Evidence Builder | evidence |
| Chart Builder | charts |
| Knowledge Builder | knowledge |
| Appendix Builder | appendix |
| Diagnostics Builder | diagnostics |

Every section has exactly one Builder.

---

# Engine Responsibilities

## Calendar Engine

Produces

- calendar information

Never produces

- interpretation
- recommendation

---

## BaZi Engine

Produces

- pillars
- stems
- branches

Never produces

- commercial advice

---

## Analysis Engine

Produces

- evidence
- strength
- pattern
- useful god
- scores

Never produces

- narrative
- recommendations

---

## Interpretation Engine

Produces

- executive summary
- interpretation
- recommendation reasoning

Never performs

- calculation

---

## Commercial Knowledge

Produces

- identity
- practical guidance
- domain consultation
- consulting wording

Never performs

- chart analysis

---

## Report Builder

Produces

```
ReportResponse
```

Never performs

- calculation
- rule matching
- knowledge retrieval

---

# Portal Consumption

| Portal Section | ReportResponse |
|----------------|----------------|
| Hero | customer |
| Identity | identity |
| Executive Summary | executive_summary |
| Strength | strengths |
| Weakness | weaknesses |
| Useful God | useful_god |
| Career | domains.career |
| Finance | domains.finance |
| Marriage | domains.marriage |
| Health | domains.health |
| Recommendation | recommendations |
| Evidence | evidence |
| Charts | charts |
| Knowledge | knowledge |

Portal never consumes internal engine models.

---

# PDF Consumption

PDF Export consumes exactly the same ReportResponse.

No separate export model exists.

---

# API Contract

Applications API exposes

```
POST /api/v1/analyze

↓

ReportResponse
```

No API returns AnalysisResult or InterpretationResult directly to customer applications.

---

# Traceability Rules

Every commercial section must preserve

```
evidence_refs

interpretation_refs

knowledge_refs

rule_refs
```

Traceability may never be removed during Report Builder assembly.

---

# Required Sections

Mandatory

- metadata
- customer
- chart
- executive_summary
- identity
- recommendations

Recommended

- strengths
- weaknesses
- useful_god
- evidence

Optional

- domains
- charts
- knowledge
- appendix
- diagnostics

---

# Dependency Rules

Allowed

```
Report Builder

↓

AnalysisResult

↓

InterpretationResult

↓

Commercial Bundle
```

Forbidden

- Portal → Analysis Engine
- Portal → Knowledge DB
- PDF → Analysis Engine
- Builder → Rule Database
- Builder → Calendar Engine

---

# Validation Checklist

Every mapping must satisfy

✓ One owner

✓ One primary source

✓ One builder

✓ One presentation target

✓ One traceability chain

✓ Backward compatibility

---

# Relationship to Other Documents

| Document | Purpose |
|----------|---------|
| README.md | Integration Layer overview |
| 00_SYSTEM_FLOW.md | System pipeline |
| 00A_ARCHITECTURE_DECISIONS.md | Architecture decisions |
| 01_REPORT_RESPONSE_SPEC.md | Canonical contract |
| 01A_REPORT_SCHEMA_DIAGRAM.md | Structural hierarchy |
| 02_FIELD_MAPPING.md | Data lineage (this document) |
| 03_VERSIONING.md | Contract evolution |

---

# Official Status

Document

Canonical Field Mapping

Status

Architecture Freeze Candidate

Commercial Version

RC1

Owner

BTE Architecture