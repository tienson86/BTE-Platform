# RESULT_PAGE_LAYOUT_GALLERY.md

Version: 1.0

Status: OFFICIAL

Owner: BTE UI Architecture

Depends on

- PACK_06_RESULT_PAGE_LAYOUT_STANDARD.md
- PACK_07_RESULT_PAGE_BLUEPRINT.md

---

# Purpose

This document contains all officially approved layout patterns used throughout the BTE Platform.

Developers and Cursor should reuse these patterns instead of inventing new layouts.

Each pattern has

- Purpose
- Blueprint
- Recommended Usage
- Do
- Don't

These patterns form the official Layout Pattern Library.

---

# Pattern 01

Executive Summary

Purpose

Display the most important conclusions.

Blueprint

┌──────────────┬──────────────┬──────────────┐
│              │              │              │
│ Executive    │ Indicators   │ Direction    │
│ Summary      │              │              │
│              │              │              │
└──────────────┴──────────────┴──────────────┘

Columns

4 + 4 + 4

Height

M

Reading Time

30 seconds

Suitable For

Result Overview

Report Overview

Dashboard Overview

Rules

Equal Height

No Paragraphs

Maximum 4 lines

No scrolling
---

# Pattern 02

KPI Grid

┌──────┬──────┬──────┬──────┐
│ KPI  │ KPI  │ KPI  │ KPI  │
└──────┴──────┴──────┴──────┘

Columns

3+3+3+3

Height

S

Maximum

4 KPIs

Never

6 KPIs

Never

Auto Height
---

# Pattern 03

Triple Analysis

┌──────────────┬──────────────┬──────────────┐
│ Five Element │ Strength     │ Ten Gods     │
└──────────────┴──────────────┴──────────────┘

Columns

4+4+4

Height

XL

Rules

Equal Height

Same Density

Preview Only
---

# Pattern 04

Visualization

┌──────────────────────┬──────────────────────┐
│ Radar                │ Timeline             │
└──────────────────────┴──────────────────────┘

Columns

6+6

Height

XL

Rules

Text Summary Required

Fixed Height

No Stretch
---

# Pattern 05

Recommendation

┌──────────────────────────────────────────┐
│                                          │
│          Recommendation                  │
│                                          │
└──────────────────────────────────────────┘

Columns

12

Height

L

Contains

Priority

Action

Reason

Benefit
---

# Pattern 06

Interpretation

┌──────────────────────────────────────────┐
│                                          │
│            Interpretation                │
│                                          │
└──────────────────────────────────────────┘

Columns

12

Height

AUTO

Rules

Preview

Expand

Collapse
---

# Pattern 07

Knowledge

┌──────────────────────────────────────────┐
│                                          │
│               Knowledge                  │
│                                          │
└──────────────────────────────────────────┘

Height

AUTO

Accordion

Supported
---

# Pattern 08

┌──────────────────────┬──────────────────────┐
│                      │                      │
│                      │                      │
└──────────────────────┴──────────────────────┘

Columns

6+6

Height

Same

Use

Comparison

Chart

Statistics

Never

Different Heights
---

# Pattern 09

┌──────┬──────┬──────┬──────┐
│Stat  │Stat  │Stat  │Stat  │
└──────┴──────┴──────┴──────┘

Height

S

Columns

3+3+3+3

Use

Metrics

Scores

KPIs
---

# Pattern 10

┌────────────────────────────────────────────┐
│                                            │
│              Report Viewer                 │
│                                            │
└────────────────────────────────────────────┘

Columns

12

Height

AUTO

Only

Report

Interpretation

Appendix
# Layout Decision Matrix

| Content Type | Pattern |
|--------------|---------|
| Executive Summary | Pattern 01 |
| KPI | Pattern 02 |
| Analysis | Pattern 03 |
| Charts | Pattern 04 |
| Recommendation | Pattern 05 |
| Interpretation | Pattern 06 |
| Knowledge | Pattern 07 |
| Comparison | Pattern 08 |
| Statistics | Pattern 09 |
| Report | Pattern 10 |
# Cursor Decision Rules

Before creating a layout

Cursor MUST

1.

Identify Content Type

↓

2.

Select Official Pattern

↓

3.

Apply Blueprint

↓

4.

Fill ViewModel

↓

5.

Render

Cursor MUST NOT

Invent new layouts

Invent new spacing

Invent new heights

Invent new grids

Combine multiple patterns into one row without approval.