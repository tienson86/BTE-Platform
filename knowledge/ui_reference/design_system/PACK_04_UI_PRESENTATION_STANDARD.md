# PACK_04_UI_PRESENTATION_STANDARD.md

Version: 1.0
Status: OFFICIAL
Owner: BTE UI Architecture

Depends on

- PACK_01_DESIGN_PRINCIPLES.md
- PACK_02_LAYOUT_SYSTEM.md
- PACK_03_COMPONENT_STANDARD.md

---

# 1. Purpose

This document defines the official UI Presentation Standard of the BTE Platform.

Unlike the Layout System and Component Standard, this specification controls how dynamic data is transformed into user-facing content.

The objective is to ensure that all analytical results remain readable, visually balanced, and consistent regardless of the size or complexity of the underlying data.

This specification applies to every screen that renders analysis results, reports, dashboards, recommendations, interpretations, or any dynamically generated content.

---

# 2. Presentation Philosophy

The Presentation Layer is responsible for transforming analytical output into human-readable information.

Business Engines generate knowledge.

Presentation Layer organizes knowledge.

UI Components render knowledge.

The responsibilities must remain completely separated.

Never allow business logic inside presentation.

Never allow presentation logic inside engines.

---

## Core Principle

Analysis Engine

↓

Presentation Adapter

↓

View Model

↓

React Components

↓

Rendered UI

The UI must never render raw engine output directly.

Every piece of data must first pass through the Presentation Layer.

---

# 3. Presentation Objectives

The Presentation Layer must achieve the following goals.

## 3.1 Readability

Present information in a way that users can understand within seconds.

Long analytical content should always be summarized before detailed explanations.

---

## 3.2 Consistency

The same analytical result must always be presented using the same visual pattern.

Example

Overall Score

↓

Score Card

Strength Analysis

↓

Analysis Card

Recommendations

↓

Recommendation Card

Never invent new layouts for identical information.

---

## 3.3 Stability

Rendering additional data must never break page layout.

Cards should remain visually stable regardless of content length.

---

## 3.4 Scalability

The Presentation Layer must support future engines without requiring redesign.

Adding new analysis modules should only require new View Models, not new layout systems.

---

## 3.5 Progressive Understanding

Users should receive information in the following order.

Summary

↓

Key Findings

↓

Analysis

↓

Interpretation

↓

Recommendations

↓

Detailed Knowledge

Never display detailed information before users understand the summary.
---

# 4. Presentation Pipeline

The Presentation Layer is the mandatory bridge between Business Engines and User Interface.

No UI component is allowed to consume raw engine output directly.

The Presentation Pipeline is defined as follows.

```
Business Engine
        │
        ▼
Raw Result
        │
        ▼
Presentation Adapter
        │
        ▼
View Model
        │
        ▼
React Components
        │
        ▼
Rendered Screen
```

Each layer has one responsibility only.

Business Engine

- Calculate
- Analyze
- Infer
- Produce structured knowledge

Presentation Adapter

- Organize information
- Summarize
- Prioritize
- Limit content
- Prepare rendering model

View Model

- UI-friendly structure
- Fixed schema
- Component-ready

React Components

- Pure rendering
- No business logic
- No data transformation

---

## 4.1 Layer Responsibilities

Business Engine must never know

- screen layout
- card size
- typography
- spacing
- responsive behavior

Presentation Layer must never perform

- calculations
- rule evaluation
- scoring
- prediction

UI Components must never

- manipulate business data
- filter engine output
- calculate values

---

## 4.2 Pipeline Rules

Every analytical result must pass through every stage.

Raw Engine Output

↓

Presentation Adapter

↓

ViewModel

↓

UI Components

Skipping any stage is prohibited.

---

## 4.3 Pipeline Objectives

The Presentation Pipeline exists to ensure

✓ Stable layouts

✓ Predictable rendering

✓ Consistent presentation

✓ Reusable UI

✓ Future scalability

---

# 5. UI Rendering Flow

The UI Rendering Flow defines how information becomes visible to users.

The flow is always identical regardless of engine type.

```
Raw Data
    │
    ▼
Summary
    │
    ▼
Highlights
    │
    ▼
Analysis
    │
    ▼
Recommendations
    │
    ▼
Detailed Interpretation
```

The UI should never begin with detailed paragraphs.

Users should first understand the conclusion before reading the reasoning.

---

## 5.1 Rendering Order

Every Result Page follows this order.

Executive Summary

↓

Key Metrics

↓

Key Findings

↓

Core Analysis

↓

Recommendations

↓

Detailed Interpretation

↓

Knowledge References

Never change this order.

---

## 5.2 Information Priority

Priority 1

Immediate decision information

Examples

Overall Score

Strength

Useful God

Pattern

Risk Level

Priority 2

Supporting analysis

Examples

Ten Gods

Elements

Season

Luck

Priority 3

Detailed explanation

Examples

Paragraphs

References

Definitions

Knowledge Base

The UI must always render Priority 1 first.

---

## 5.3 Rendering Strategy

Every section follows

Headline

↓

Summary

↓

Supporting Details

↓

Expand

Never display detailed paragraphs immediately.

---

## 5.4 Rendering Constraints

Rendering must never

expand layout

change card size

break grid alignment

cause layout shift

generate nested scrolling

create horizontal scrolling

---

# 6. ViewModel Architecture

ViewModels are the only data structures consumed by UI Components.

React Components must never read engine models directly.

---

## 6.1 Purpose

ViewModels convert complex analytical structures into presentation-friendly objects.

They remove unnecessary information while preserving meaning.

---

## 6.2 ViewModel Principles

Every ViewModel must

be immutable

contain only rendering data

contain no business logic

contain no calculation

contain no engine dependency

---

## 6.3 ViewModel Categories

SummaryViewModel

AnalysisViewModel

ScoreViewModel

RecommendationViewModel

InsightViewModel

TimelineViewModel

ChartViewModel

TableViewModel

InterpretationViewModel

MetadataViewModel

Each UI Component receives exactly one ViewModel.

---

## 6.4 ViewModel Responsibilities

ViewModels prepare

formatted titles

formatted values

icons

colors

badges

display order

preview text

expanded text

status

visibility

Components should never generate these values themselves.

---

## 6.5 ViewModel Rules

ViewModels may

truncate text

sort items

group information

merge fields

prepare previews

prepare display labels

ViewModels may not

change business meaning

calculate scores

evaluate rules

predict results

---

## 6.6 Future Compatibility

Every new Engine introduced into the BTE Platform must provide a Presentation Adapter capable of producing official ViewModels.

This guarantees that new engines automatically integrate into the existing UI without redesigning components.

ViewModels are therefore considered the official contract between Business Engines and the User Interface.

---

# 7. Card Height Matrix

Card height must be determined by the Design System, not by content.

Every card belongs to one predefined height category.

Dynamic content must adapt to the card.

The card must never adapt to unlimited content.

---

## 7.1 Official Height Classes

| Class | Height | Typical Usage |
|--------|---------|---------------|
| XS | 160px | Status, Badge, KPI |
| S | 220px | Summary, Statistics |
| M | 320px | Analysis, Insight |
| L | 420px | Recommendation, Timeline |
| XL | 560px | Table, Chart |
| AUTO | Reserved | Reports only |

AUTO height is prohibited for Dashboard pages.

---

## 7.2 Card Type Mapping

The following mapping is mandatory.

| Card Type | Height Class |
|------------|--------------|
| Summary Card | S |
| Score Card | S |
| Statistic Card | S |
| Insight Card | M |
| Analysis Card | M |
| Recommendation Card | M |
| Timeline Card | L |
| Table Card | XL |
| Chart Card | XL |
| Report Viewer | AUTO |

No custom height is allowed.

---

## 7.3 Equal Height Rule

Cards placed in the same grid row must use the same height class.

Correct

```
M     M     M
```

Correct

```
S     S     S
```

Incorrect

```
S     XL    M
```

Uneven rows reduce readability and visual rhythm.

---

## 7.4 Height Stability

Card height must remain unchanged during

Loading

Rendering

Filtering

Refreshing

Expanding Preview

Only dedicated expandable pages may increase height.

Dashboard cards must remain fixed.

---

## 7.5 Overflow Policy

When content exceeds the available height

Priority 1

Line Clamp

↓

Priority 2

Internal Scroll

↓

Priority 3

Expand

Never increase card height automatically.

---

# 8. Content Density Rules

Content density defines how much information may appear inside one card.

The objective is to maximize understanding rather than maximize data.

---

## 8.1 Information Budget

Each card has a limited information budget.

Too much information increases cognitive load.

A card should answer one question only.

---

## 8.2 Maximum Text

Official limits

| Element | Maximum |
|----------|----------|
| Title | 2 lines |
| Subtitle | 2 lines |
| Summary | 4 lines |
| Description | 6 lines |
| Note | 3 lines |

Anything longer must be truncated.

---

## 8.3 Maximum Lists

Official limits

| Component | Maximum |
|------------|----------|
| Bullet List | 5 items |
| Recommendation | 3 items |
| Insight | 5 items |
| Warning | 3 items |
| Tags | 8 items |

Additional items should be hidden behind

View All

or

Expand.

---

## 8.4 Maximum Numbers

Do not display excessive metrics.

Preferred

3–5 KPIs

Acceptable

6 KPIs

Avoid

More than 8 KPIs inside one card.

---

## 8.5 Reading Time

Every card should be understandable within

5–10 seconds.

If users need longer,

the content should be divided into multiple cards.

---

## 8.6 One Purpose Rule

Every card must answer exactly one question.

Bad Example

Summary

Score

Recommendation

History

Knowledge

inside one card.

Good Example

Separate cards.

---

# 9. Dynamic Content Rules

Dynamic content must never control layout.

Presentation Layer is responsible for adapting content to the available space.

---

## 9.1 Preview First

Long content is displayed as

Preview

↓

Expand

↓

Full Content

Never render entire paragraphs immediately.

---

## 9.2 Line Clamp Rules

Official rules

Title

2 lines

Summary

4 lines

Description

6 lines

Recommendation

3 items

Timeline

6 events

Everything beyond the limit should be hidden.

---

## 9.3 Expand Pattern

Expandable components follow

Preview

↓

Expand

↓

Collapse

The initial state is always Preview.

---

## 9.4 Scroll Strategy

Preferred

Page Scroll

Allowed

Internal Card Scroll

Avoid

Nested Scroll

Never

Horizontal Scroll

---

## 9.5 List Strategy

Lists longer than the official limit must display

First Items

↓

"+ N More"

↓

View All

Never render unlimited lists.

---

## 9.6 Paragraph Strategy

Long analytical paragraphs should be divided into

Executive Summary

↓

Key Findings

↓

Detailed Interpretation

Never display a wall of text.

---

## 9.7 Rendering Priority

The UI always renders

Critical Information

↓

Important Information

↓

Supporting Information

↓

References

Users should understand the conclusion before reading details.

---

## 9.8 Stable Rendering

Refreshing data must never

change card height

change grid alignment

move surrounding cards

cause layout jumping

Stable rendering is mandatory.

---

## 9.9 Presentation Responsibility

Presentation Layer is responsible for

summarizing

truncating

sorting

grouping

prioritizing

formatting

preparing previews

UI Components are responsible only for rendering.

Business Engines are responsible only for analysis.

Responsibilities must never overlap.

---

# 10. Typography Presentation Rules

Typography is the primary communication tool of the BTE Platform.

Users should understand information through typography before relying on color, icons, or graphics.

Typography must communicate hierarchy, not decoration.

---

## 10.1 Typography Hierarchy

Official hierarchy

| Level | Usage |
|--------|-------|
| H1 | Page Title |
| H2 | Section Title |
| H3 | Card Title |
| H4 | Group Title |
| Body | Main Content |
| Caption | Supporting Information |
| Label | UI Labels |
| Code | Technical Values |

Never invent additional typography levels.

---

## 10.2 Reading Priority

Typography should guide users in the following order.

Headline

↓

Score

↓

Summary

↓

Supporting Analysis

↓

Detailed Interpretation

↓

Metadata

The user should immediately recognize what deserves attention.

---

## 10.3 Number Presentation

Numerical values must be visually emphasized.

Examples

Overall Score

Strength

Risk Level

Luck Score

Compatibility Score

Numbers should always appear before supporting explanations.

---

## 10.4 Paragraph Rules

Paragraphs should be concise.

Preferred length

2–4 sentences.

Maximum

6 sentences.

Long explanations should be divided into multiple paragraphs.

Never display large uninterrupted text blocks.

---

## 10.5 Highlight Rules

Important conclusions should be highlighted using

Bold typography

Status badge

Insight block

Recommendation block

Avoid excessive use of bold text.

---

# 11. List & Table Presentation Rules

Lists and tables organize structured information.

They should maximize readability rather than data density.

---

## 11.1 List Rules

Preferred list length

3–5 items.

Maximum

8 items.

Longer lists must be collapsed.

---

## 11.2 Bullet Hierarchy

Recommended order

Primary Finding

↓

Supporting Point

↓

Additional Note

Avoid more than two nesting levels.

---

## 11.3 Table Rules

Tables should contain

Title

↓

Header

↓

Rows

↓

Optional Summary

Avoid large unstructured tables.

---

## 11.4 Table Size

Dashboard

Maximum

10 rows.

Detailed Report

20–30 rows.

Large datasets

Use pagination or virtualization.

---

## 11.5 Column Priority

Columns should appear in the following order.

Identifier

↓

Primary Value

↓

Status

↓

Trend

↓

Details

Do not place supporting information before critical values.

---

## 11.6 Empty Table

Empty tables should display

Illustration

↓

Message

↓

Suggested Action

Never show an empty grid.

---

# 12. Analysis & Recommendation Presentation Rules

Analysis is the core value of the BTE Platform.

Presentation must guide users from understanding toward action.

---

## 12.1 Analysis Structure

Every analysis follows

Summary

↓

Evidence

↓

Reasoning

↓

Conclusion

Do not skip reasoning.

---

## 12.2 Recommendation Structure

Every recommendation contains

Priority

↓

Recommended Action

↓

Reason

↓

Expected Benefit

↓

Optional Risk

Users should understand not only what to do but also why.

---

## 12.3 Priority Levels

Recommendations use four priority levels.

Critical

High

Medium

Low

Priority determines visual emphasis.

---

## 12.4 Recommendation Count

Preferred

3 recommendations.

Maximum

5 recommendations.

Additional recommendations belong in the expanded view.

---

## 12.5 Analysis Grouping

Related findings should be grouped together.

Examples

Strength Analysis

Weakness Analysis

Useful God Analysis

Luck Analysis

Career Analysis

Relationship Analysis

Never mix unrelated topics inside one card.

---

## 12.6 Action-Oriented Presentation

Every completed analysis should answer

What happened?

↓

Why?

↓

What should I do?

↓

What happens next?

If one of these questions is missing,

the presentation is incomplete.

---

# 13. Insight & Interpretation Presentation Rules

Insights transform analytical results into understandable knowledge.

Interpretation explains meaning.

Presentation should prioritize clarity over completeness.

---

## 13.1 Insight Structure

Every Insight Card contains

Headline

↓

Summary

↓

Supporting Explanation

↓

Optional Expand

Insights should be immediately understandable.

---

## 13.2 Interpretation Structure

Interpretation follows

Observation

↓

Explanation

↓

Impact

↓

Recommendation

This sequence should remain consistent throughout the platform.

---

## 13.3 Executive Summary

Every Result Page begins with an Executive Summary.

The summary should answer

Overall Status

↓

Most Important Finding

↓

Most Important Recommendation

The user should understand the overall result within 30 seconds.

---

## 13.4 Interpretation Length

Preferred

150–300 words.

Long interpretations should be divided into sections.

Avoid displaying one continuous narrative.

---

## 13.5 Knowledge References

Definitions

Historical Notes

Classical References

Technical Details

should always appear after the interpretation.

Knowledge should support understanding,

not interrupt it.

---

## 13.6 Expand Strategy

Only the following content may expand.

Detailed Interpretation

Knowledge References

Historical Background

Technical Explanation

Executive Summary

Insights

Recommendations

must remain concise.

---

## 13.7 Reading Flow

The official reading sequence is

Executive Summary

↓

Core Findings

↓

Analysis

↓

Interpretation

↓

Recommendations

↓

Knowledge References

↓

Appendix

This order is mandatory for all analytical result pages.
---

# 14. Loading, Empty & Error Presentation

Presentation must remain stable under every application state.

The user experience should remain predictable whether data is loading, unavailable, empty, or failed.

---

# 14.1 Loading State

Loading is part of the normal user experience.

Loading should communicate progress rather than uncertainty.

The layout must already exist before data arrives.

---

## 14.2 Skeleton First

Every page must render Skeleton components instead of blank space.

Skeleton dimensions must exactly match the final layout.

Example

Header

↓

Summary Cards

↓

Analysis Cards

↓

Recommendation Cards

↓

Charts

↓

Tables

Never display layout jumps after loading completes.

---

## 14.3 Progressive Loading

Load information according to priority.

Priority 1

Executive Summary

↓

Priority 2

Score Cards

↓

Priority 3

Analysis

↓

Priority 4

Recommendations

↓

Priority 5

Knowledge References

Critical information should always appear first.

---

## 14.4 Empty State

Empty state is not an error.

Every empty state contains

Illustration

↓

Title

↓

Explanation

↓

Suggested Action

Never leave empty containers.

---

## 14.5 Empty State Examples

No Analysis Yet

No Recommendations

No Search Results

No Report

No History

Each case should provide a meaningful next action.

---

## 14.6 Error State

Error pages should explain

What happened

↓

Why it happened (if known)

↓

How to recover

↓

Retry

Users should never feel blocked.

---

## 14.7 Error Severity

Official severity levels

Information

Warning

Recoverable Error

Critical Error

Each severity has a predefined visual style.

---

# 15. Responsive Presentation Rules

The Presentation Layer must adapt content without changing information hierarchy.

Only layout changes.

Information does not.

---

## 15.1 Responsive Principle

Desktop

Most detailed presentation

Tablet

Balanced presentation

Mobile

Essential presentation

Users should always receive the same meaning.

---

## 15.2 Responsive Content

Desktop

Summary

Analysis

Recommendations

Knowledge

Tablet

Summary

Analysis

Recommendations

Mobile

Summary

Key Findings

Recommendations

Detailed interpretation moves behind Expand.

---

## 15.3 Card Behaviour

Desktop

Multi-column

Tablet

Two-column

Mobile

Single-column

Never reduce readability.

---

## 15.4 Responsive Typography

Typography scales slightly.

Hierarchy never changes.

H1 remains H1.

Body remains Body.

Only size changes.

---

## 15.5 Responsive Tables

Desktop

Table

Tablet

Condensed Table

Mobile

Card List

Never require horizontal scrolling.

---

## 15.6 Responsive Charts

Large charts

↓

Medium charts

↓

Compact charts

↓

Summary only

If space is insufficient,

summarize rather than shrink excessively.

---

# 16. Animation & Transition Rules

Animation should support understanding.

Never distract users.

---

## 16.1 Animation Principles

Animations should

Guide

Explain

Confirm

Never entertain.

---

## 16.2 Allowed Animations

Fade

Slide

Expand

Collapse

Loading Skeleton

Progress

Avoid excessive movement.

---

## 16.3 Duration

Short

100–150ms

Normal

200–300ms

Long

400ms maximum

No animation should exceed 500ms.

---

## 16.4 Motion Hierarchy

Highest priority

State Change

Medium

Expansion

Lowest

Decorative Animation

Decorative animation is discouraged.

---

## 16.5 Layout Stability

Animations must never

move surrounding cards

change grid alignment

change page height unexpectedly

Stable layout is mandatory.

---

# 17. Presentation Adapter Specification

The Presentation Adapter is the official bridge between Business Engines and UI Components.

Every engine must expose its results through an official Presentation Adapter.

---

## 17.1 Responsibilities

Presentation Adapter

Receives

↓

Raw Engine Result

Produces

↓

Official ViewModel

The adapter is responsible for presentation only.

---

## 17.2 Adapter Responsibilities

Prepare

Titles

Summaries

Preview Text

Display Labels

Icons

Badges

Status

Priority

Visibility

Expand Content

Ordering

Grouping

Formatting

No calculations are allowed.

---

## 17.3 Adapter Output

Each adapter returns standardized ViewModels.

Examples

SummaryViewModel

ScoreViewModel

AnalysisViewModel

RecommendationViewModel

InsightViewModel

InterpretationViewModel

TimelineViewModel

ChartViewModel

TableViewModel

Every ViewModel follows official UI contracts.

---

## 17.4 Adapter Rules

Adapters may

Group information

Sort items

Prepare previews

Limit content

Generate display metadata

Adapters may not

Change engine conclusions

Calculate scores

Evaluate rules

Predict outcomes

Modify business meaning

---

## 17.5 Adapter Pipeline

Engine

↓

Presentation Adapter

↓

ViewModel

↓

Component

↓

Rendered UI

Every engine must follow this identical pipeline.

---

## 17.6 Shared Adapter Library

The Presentation Adapter should be implemented as a shared library.

Suggested structure

presentation/

├── adapters/

├── view_models/

├── formatters/

├── mappers/

├── preview/

├── grouping/

├── sorting/

├── truncation/

└── constants/

This library becomes the single presentation layer shared across the entire BTE Platform.

---

## 17.7 Compatibility

Every future engine

Analysis Engine

Interpretation Engine

Report Engine

Knowledge Engine

AI Rewrite Engine

must integrate through the Presentation Adapter.

UI Components should never know which engine generated the data.

The Presentation Adapter is the official contract between Business Logic and User Interface.
---

# 18. Cursor Implementation Rules

This section defines mandatory implementation rules for Cursor and all developers working on the BTE Platform.

These rules are implementation constraints rather than design recommendations.

Violation of these rules is considered a Design System violation.

---

## 18.1 Cursor MUST

Cursor MUST

✓ Use the official Presentation Adapter

✓ Consume only ViewModels

✓ Follow the official Layout System

✓ Follow the official Component Standard

✓ Keep card heights fixed

✓ Preserve equal-height grid rows

✓ Apply official spacing scale

✓ Apply official typography hierarchy

✓ Use line-clamp where required

✓ Use Preview before Expand

✓ Preserve layout stability

✓ Render loading skeletons

✓ Render meaningful empty states

✓ Preserve responsive hierarchy

✓ Reuse existing components whenever possible

---

## 18.2 Cursor MUST NOT

Cursor MUST NOT

✗ Read raw Engine Models directly

✗ Render raw JSON

✗ Calculate business values

✗ Create custom spacing

✗ Create custom typography

✗ Create custom card heights

✗ Stretch cards because of content

✗ Introduce horizontal scrolling

✗ Introduce nested scrolling

✗ Hardcode colors

✗ Duplicate existing components

✗ Create new layout systems

✗ Mix business logic into UI

---

## 18.3 Rendering Rules

Every screen must follow

Presentation Adapter

↓

ViewModel

↓

Component

↓

Render

Skipping any stage is prohibited.

---

## 18.4 Refactoring Rules

When modifying existing screens

Cursor should

improve consistency

reduce duplication

reuse shared components

preserve visual hierarchy

avoid unnecessary redesign

The objective is improvement rather than replacement.

---

## 18.5 Future Development

Every new feature

must reuse

existing components

existing layout

existing typography

existing spacing

Only when no official component exists may a new component be introduced.

New components must first be added to

PACK_03_COMPONENT_STANDARD.md

before implementation.

---

# 19. Anti-Patterns & Best Practices

This chapter documents common implementation mistakes and the official solution.

---

## 19.1 Anti-Pattern

Dynamic Card Height

Problem

Long text stretches cards.

Result

Broken grid alignment.

Correct Solution

Clamp

↓

Preview

↓

Expand

Never resize the card.

---

## 19.2 Anti-Pattern

Wall of Text

Problem

Large uninterrupted paragraphs.

Result

Poor readability.

Correct Solution

Summary

↓

Key Findings

↓

Detailed Interpretation

---

## 19.3 Anti-Pattern

Mixed Information

Problem

One card contains

Summary

Analysis

Recommendations

Knowledge

History

Correct Solution

Split into independent cards.

One card

One purpose.

---

## 19.4 Anti-Pattern

Nested Scrolling

Problem

Scroll inside

Scroll inside

Scroll inside

Result

Poor user experience.

Correct Solution

Prefer page scrolling.

Use internal scrolling only where officially defined.

---

## 19.5 Anti-Pattern

Visual Inconsistency

Problem

Random spacing

Random typography

Random colors

Random buttons

Correct Solution

Use official Design System only.

---

## 19.6 Anti-Pattern

Component Duplication

Problem

Three cards

perform identical functions

with different implementations.

Correct Solution

One reusable component.

Shared everywhere.

---

## 19.7 Best Practices

Recommended workflow

Business Engine

↓

Presentation Adapter

↓

ViewModel

↓

Official Components

↓

Official Layout

↓

Stable UI

This workflow should be followed by every feature.

---

## 19.8 Golden Rule

The UI should never surprise users.

Users should always know

where information is

what is important

what action comes next.

Consistency is more important than creativity.

---

# 20. Acceptance Criteria & Compliance Checklist

This chapter defines the official compliance checklist for every UI implementation.

Every screen must satisfy these requirements before approval.

---

## 20.1 Layout

✓ Official Grid

✓ Official Spacing

✓ Official Alignment

✓ Equal-height Cards

✓ Stable Layout

---

## 20.2 Components

✓ Official Components

✓ Official States

✓ Official Typography

✓ Official Colors

✓ No Duplicate Components

---

## 20.3 Presentation

✓ Presentation Adapter

✓ ViewModel

✓ Preview Strategy

✓ Expand Strategy

✓ Stable Rendering

✓ Progressive Disclosure

---

## 20.4 Dynamic Content

✓ Line Clamp

✓ Overflow Strategy

✓ Scroll Strategy

✓ Content Density Rules

✓ Fixed Card Heights

---

## 20.5 User Experience

✓ Executive Summary First

✓ Key Findings Visible

✓ Recommendations Clear

✓ Reading Flow Correct

✓ No Information Overload

---

## 20.6 Responsive Design

✓ Desktop

✓ Tablet

✓ Mobile

✓ No Horizontal Scroll

✓ Preserved Hierarchy

---

## 20.7 Accessibility

✓ Keyboard Navigation

✓ Focus State

✓ Color Contrast

✓ Readable Typography

✓ Screen Reader Support

---

## 20.8 Performance

✓ Stable Rendering

✓ No Layout Shift

✓ Skeleton Loading

✓ Lazy Rendering where appropriate

✓ Optimized Component Reuse

---

## 20.9 Maintainability

✓ Shared Components

✓ Shared Layout

✓ Shared Presentation Adapter

✓ Shared ViewModels

✓ No Business Logic inside UI

---

## 20.10 Final Compliance

A screen is considered compliant only when

✓ It satisfies PACK_01_DESIGN_PRINCIPLES

✓ It satisfies PACK_02_LAYOUT_SYSTEM

✓ It satisfies PACK_03_COMPONENT_STANDARD

✓ It satisfies PACK_04_UI_PRESENTATION_STANDARD

Any violation requires correction before merge.

---

END OF DOCUMENT