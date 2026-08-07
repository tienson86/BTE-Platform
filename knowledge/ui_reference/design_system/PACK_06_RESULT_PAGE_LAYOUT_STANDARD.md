# PACK_06_RESULT_PAGE_LAYOUT_STANDARD.md

Version: 1.0

Status: OFFICIAL

Owner: BTE UI Architecture

Depends on

- PACK_01_DESIGN_PRINCIPLES.md
- PACK_02_LAYOUT_SYSTEM.md
- PACK_03_COMPONENT_STANDARD.md
- PACK_04_UI_PRESENTATION_STANDARD.md
- PACK_05_ACCESSIBILITY.md

---

# 1. Purpose

This document defines the official screen architecture of the BTE Result Page.

Unlike the Design System, which defines reusable UI rules, this specification defines how a complete Result Page is assembled.

It specifies

- screen hierarchy
- reading flow
- row structure
- card arrangement
- visual priority
- responsive behavior

Every Result Page within the BTE Platform must follow this specification.

---

# 2. Screen Philosophy

The Result Page is not a dashboard.

It is an analytical reading experience.

Users should gradually move from

Overview

↓

Understanding

↓

Analysis

↓

Interpretation

↓

Recommendation

↓

Knowledge

The interface should never overwhelm users with raw data.

The page should guide users through an analytical journey.

---

# 3. Reading Journey

The official reading order is

Executive Summary

↓

Core Indicators

↓

Chart Overview

↓

Core Analysis

↓

Recommendations

↓

Detailed Interpretation

↓

Knowledge Reference

↓

Appendix

Users should understand the overall conclusion before reading detailed explanations.

The screen should behave like a professional analytical report rather than a collection of independent widgets.

---

# 4. Result Page Architecture

The Result Page consists of independent layout zones.

```

Header

↓

Context

↓

Summary Zone

↓

Analysis Zone

↓

Interpretation Zone

↓

Recommendation Zone

↓

Knowledge Zone

↓

Footer

```

Each zone has one responsibility only.

Zones should never overlap responsibilities.

The overall architecture should remain stable regardless of the amount of analytical data.
---

# 5. Row Architecture

The Result Page is organized into independent horizontal layout rows.

Each row has a dedicated responsibility.

Rows should never mix unrelated analytical content.

Rows are the highest-level layout units after the screen itself.

---

## 5.1 Official Row Structure

The Result Page consists of the following rows.

```
Row 01

Context Information

↓

Row 02

Executive Summary

↓

Row 03

Core Analysis

↓

Row 04

Charts & Indicators

↓

Row 05

Recommendations

↓

Row 06

Detailed Interpretation

↓

Row 07

Knowledge Reference

↓

Footer
```

Rows should always appear in this order.

---

## 5.2 Row Independence

Each row is independent.

A row must never influence

height

spacing

alignment

of another row.

Rows communicate only through reading order.

---

## 5.3 Row Responsibilities

Each row answers exactly one user question.

Example

Context

Who is this report for?

↓

Summary

What is the conclusion?

↓

Analysis

Why?

↓

Recommendation

What should I do?

↓

Knowledge

How can I learn more?

---

# 6. Card Placement Matrix

Cards should not be positioned arbitrarily.

Every card has an official location.

Moving cards between rows is prohibited unless the Design System is updated.

---

## 6.1 Row 01

Context Zone

Contains

User Information

Birth Information

Report Information

Analysis Status

Version

Sharing

---

## 6.2 Row 02

Executive Summary

Contains

Life Overview

Core Indicators

Useful God

Pattern

Destiny Direction

Feng Shui Summary

This row provides a complete overview.

---

## 6.3 Row 03

Analysis Zone

Contains

BaZi

Five Elements

Strength

Ten Gods

Pattern

Luck

This row explains the reasoning.

---

## 6.4 Row 04

Visualization Zone

Contains

Charts

Radar

Timeline

Distribution

Element Balance

Visualizations should support analysis rather than replace it.

---

## 6.5 Row 05

Recommendation Zone

Contains

Recommendations

Warnings

Actions

Priority Tasks

Future Opportunities

Users should understand what to do next.

---

## 6.6 Row 06

Interpretation Zone

Contains

Detailed Interpretation

Expanded Analysis

Relationships

Career

Health

Wealth

Family

This is the longest reading section.

---

## 6.7 Row 07

Knowledge Zone

Contains

Definitions

Traditional References

Classical Texts

Terminology

Appendix

This information supports learning.

---

# 7. Grid Specification

Every row follows a predefined grid.

The grid belongs to the row.

Cards do not create their own grids.

---

## 7.1 Grid Width

Desktop

12 Columns

Tablet

8 Columns

Mobile

4 Columns

Official gaps follow PACK_02_LAYOUT_SYSTEM.

---

## 7.2 Column Rules

Cards span predefined columns.

Example

Summary

4 Columns

Analysis

6 Columns

Recommendation

3 Columns

Knowledge

12 Columns

Avoid arbitrary column widths.

---

## 7.3 Card Alignment

Cards inside the same row

must

share

Top Alignment

Bottom Alignment

Vertical Rhythm

Baseline

Misaligned cards are considered layout defects.

---

## 7.4 Equal Height Grid

Cards inside the same row

must use identical height classes.

Example

```
320

320

320
```

Never

```
220

510

330
```

---

## 7.5 Empty Columns

Unused space should remain empty.

Never stretch neighboring cards simply to fill space.

Whitespace is intentional.

---

# 8. Row Height Matrix

Rows determine vertical rhythm.

Cards adapt to the row.

The row never adapts to the card.

---

## 8.1 Official Height Classes

| Row | Height Class |
|------|--------------|
| Context | S |
| Summary | L |
| Analysis | XL |
| Visualization | XL |
| Recommendation | L |
| Interpretation | AUTO |
| Knowledge | AUTO |

AUTO height is permitted only for reading-oriented rows.

Dashboard-style rows must remain fixed.

---

## 8.2 Fixed Height Rows

Rows

Context

Summary

Analysis

Visualization

Recommendation

must always maintain fixed height.

Dynamic content should be handled using

Preview

Expand

Internal Scroll

---

## 8.3 Flexible Reading Rows

Interpretation

Knowledge

Appendix

may expand vertically because users intentionally enter reading mode.

These rows should never appear before Summary.

---

## 8.4 Vertical Rhythm

Official spacing

Between Rows

32px

Between Cards

24px

Inside Cards

16px

Spacing should remain constant across the entire page.
---

# 9. Card Priority Matrix

Every card displayed on the Result Page belongs to an official priority level.

Priority determines

- visual importance
- screen position
- rendering order
- loading order
- responsive behavior

Cards with higher priority must always appear before lower-priority cards.

---

## 9.1 Priority Levels

Priority 1

Executive Information

Priority 2

Core Analysis

Priority 3

Supporting Analysis

Priority 4

Detailed Interpretation

Priority 5

Knowledge & References

---

## 9.2 Priority Matrix

| Priority | Card Category | Purpose |
|-----------|---------------|----------|
| P1 | Executive Summary | Overall conclusion |
| P1 | Core Indicators | Key metrics |
| P1 | Destiny Direction | Decision support |
| P2 | BaZi Chart | Core analysis |
| P2 | Five Elements | Core analysis |
| P2 | Strength Analysis | Core analysis |
| P2 | Ten Gods | Core analysis |
| P3 | Pattern Analysis | Supporting analysis |
| P3 | Luck Cycle | Supporting analysis |
| P3 | ShenSha | Supporting analysis |
| P4 | Interpretation | Detailed explanation |
| P4 | Recommendation | Action guidance |
| P5 | Knowledge | Learning |
| P5 | Classical References | Reference |
| P5 | Appendix | Supporting information |

---

## 9.3 Rendering Order

Cards are rendered according to priority.

Priority 1

↓

Priority 2

↓

Priority 3

↓

Priority 4

↓

Priority 5

Rendering order must remain identical across every Result Page.

---

## 9.4 Responsive Priority

On smaller screens

Priority 5

↓

Collapse First

Priority 4

↓

Expandable

Priority 3

↓

Compact

Priority 2

↓

Visible

Priority 1

↓

Always Visible

Critical information should never disappear.

---

# 10. Summary Zone Standard

The Summary Zone is the most important section of the Result Page.

Users should understand the overall result within 30 seconds.

---

## 10.1 Purpose

The Summary Zone answers

Who is this person?

↓

What is the overall result?

↓

What deserves immediate attention?

---

## 10.2 Allowed Cards

Official cards

Executive Summary

Core Indicators

Life Direction

Useful God

Pattern Summary

Destiny Overview

No detailed explanations are allowed.

---

## 10.3 Layout

Desktop

Three-column layout

Tablet

Two-column layout

Mobile

Single-column layout

The Summary Zone should always remain above the fold whenever possible.

---

## 10.4 Content Rules

Every card should contain

Headline

↓

Key Value

↓

Short Explanation

↓

Optional Action

Long paragraphs are prohibited.

---

## 10.5 Card Height

Summary cards

must use

Height Class

M

Equal height is mandatory.

---

## 10.6 Reading Time

The entire Summary Zone

should be readable

within

30–45 seconds.

If more time is required,

the information density is too high.

---

# 11. Analysis Zone Standard

The Analysis Zone explains how the conclusions were reached.

It provides analytical evidence rather than recommendations.

---

## 11.1 Purpose

The Analysis Zone answers

Why?

What factors contribute?

What evidence supports the conclusion?

---

## 11.2 Allowed Cards

BaZi Chart

Five Elements

Strength

Ten Gods

Pattern

Luck

Season

Structure

Only analytical cards belong here.

---

## 11.3 Layout

Desktop

3-column grid

Tablet

2-column grid

Mobile

1-column stack

Cards should maintain equal height within each row.

---

## 11.4 Analysis Rules

Every Analysis Card contains

Title

↓

Key Finding

↓

Evidence

↓

Preview

↓

Expand

Never display the complete analysis immediately.

---

## 11.5 Card Density

One Analysis Card

should answer

one analytical question only.

Examples

How strong is the Day Master?

How balanced are the Five Elements?

What is the dominant Pattern?

Avoid combining unrelated analyses.

---

## 11.6 Visual Hierarchy

Within each Analysis Card

Highlight

↓

Key Metrics

↓

Summary

↓

Details

↓

Expand

Users should identify the key finding within five seconds.

---

# 12. Visualization Zone Standard

Visualization supports analytical understanding.

Charts never replace textual interpretation.

---

## 12.1 Purpose

Visualizations should

simplify

compare

summarize

highlight

analytical information.

They should not introduce new conclusions.

---

## 12.2 Allowed Components

Five Elements Distribution

Strength Gauge

Luck Timeline

Radar Chart

Progress Indicators

Heatmap

Comparison Chart

No decorative charts are allowed.

---

## 12.3 Chart Rules

Every chart contains

Title

↓

Visualization

↓

Summary

↓

Optional Expand

Charts without explanation are prohibited.

---

## 12.4 Visualization Density

One chart

should communicate

one message.

Avoid combining multiple unrelated datasets into a single visualization.

---

## 12.5 Height Rules

Visualization cards

use

Height Class

XL

Charts should never resize dynamically.

---

## 12.6 Empty Visualization

If visualization data is unavailable,

display

Illustration

↓

Reason

↓

Suggested Action

Never leave empty chart containers.

---

## 12.7 Accessibility

Every visualization must provide

Text Summary

↓

Important Values

↓

Interpretation

Users should understand the chart even without relying solely on graphics.
---

# 13. Recommendation Zone Standard

The Recommendation Zone transforms analytical conclusions into actionable guidance.

Users should immediately understand what actions are recommended based on the completed analysis.

Recommendations should be concise, prioritized, and practical.

---

## 13.1 Purpose

The Recommendation Zone answers

What should I do?

↓

What should I avoid?

↓

What deserves immediate attention?

---

## 13.2 Allowed Cards

Official cards

Action Recommendations

Risk Warnings

Priority Actions

Opportunity Suggestions

Timing Advice

Future Considerations

No analytical reasoning belongs in this zone.

---

## 13.3 Layout

Desktop

Two-column layout

Recommendation Summary

↓

Detailed Recommendations

Tablet

Single-column layout

Mobile

Single-column expandable layout

---

## 13.4 Recommendation Structure

Each recommendation contains

Priority Badge

↓

Title

↓

Short Explanation

↓

Expected Benefit

↓

Optional Expand

Long explanations belong to the expanded view.

---

## 13.5 Recommendation Count

Preferred

3–5 recommendations

Maximum

8 recommendations

Additional recommendations should appear under "View All".

---

## 13.6 Priority Order

Recommendations should always be ordered

Critical

↓

High

↓

Medium

↓

Low

The highest-priority action must always appear first.

---

# 14. Interpretation Zone Standard

The Interpretation Zone provides detailed narrative explanations.

This is the primary reading section of the Result Page.

Unlike the Summary Zone, this section is designed for deeper understanding.

---

## 14.1 Purpose

The Interpretation Zone answers

Why does this result occur?

↓

How does it affect life?

↓

How should it be understood?

---

## 14.2 Allowed Cards

Detailed Interpretation

Career Interpretation

Relationship Interpretation

Health Interpretation

Financial Interpretation

Luck Interpretation

Only narrative explanations belong here.

---

## 14.3 Reading Structure

Every interpretation follows

Observation

↓

Explanation

↓

Impact

↓

Suggestion

The structure should remain identical across all interpretation cards.

---

## 14.4 Reading Length

Recommended

150–300 words

Maximum

500 words

Longer content should be divided into subsections.

---

## 14.5 Expand Strategy

Default

Preview

↓

Expand

↓

Collapse

Users should never encounter long uninterrupted paragraphs on first load.

---

## 14.6 Height Policy

Interpretation cards may expand vertically.

This is the only reading-oriented zone where flexible height is permitted.

---

# 15. Knowledge Zone Standard

The Knowledge Zone provides educational content that supports interpretation.

Knowledge should enhance understanding but should never interrupt the primary reading flow.

---

## 15.1 Purpose

The Knowledge Zone answers

What does this concept mean?

↓

Where does this rule come from?

↓

How can I learn more?

---

## 15.2 Allowed Cards

Terminology

Classical References

Traditional Theory

Technical Notes

Appendix

Related Knowledge

Knowledge content should always appear after interpretation.

---

## 15.3 Layout

Desktop

Two-column layout

Tablet

Single-column layout

Mobile

Accordion layout

Knowledge is secondary content.

---

## 15.4 Presentation Rules

Each Knowledge Card contains

Title

↓

Short Definition

↓

Reference

↓

Optional Expand

Knowledge should never dominate the screen.

---

## 15.5 Knowledge Hierarchy

Definitions

↓

Theory

↓

Historical References

↓

Additional Reading

Users should understand the definition before reading deeper material.

---

# 16. Responsive Result Layout

The Result Page must preserve the same reading journey across all devices.

Only the layout changes.

The information hierarchy must remain unchanged.

---

## 16.1 Desktop

12-column layout

Maximum information density

Multi-column presentation

---

## 16.2 Tablet

8-column layout

Balanced spacing

Reduced columns

Cards remain grouped by zone.

---

## 16.3 Mobile

Single-column layout

Priority-based rendering

Expandable content

The reading order remains identical to the desktop version.

---

## 16.4 Responsive Priority

Always visible

Executive Summary

↓

Core Analysis

↓

Recommendations

↓

Interpretation

↓

Knowledge

Lower-priority content may collapse but must never disappear.

---

## 16.5 Stable Layout

Responsive behavior must never

change analytical order

move cards between zones

change priority

break the reading journey

Screen composition must remain consistent across all devices.
---

# 17. Cursor Implementation Rules

This chapter defines the mandatory implementation protocol for every Result Page within the BTE Platform.

Cursor and all developers must implement the Result Page according to the official Screen Architecture defined in this specification.

No implementation may introduce an alternative screen composition.

---

## 17.1 Mandatory Rendering Pipeline

The Result Page shall always be constructed using the following hierarchy.

```
Result Page

↓

Zone

↓

Row

↓

Grid

↓

Card

↓

Component

↓

ViewModel

↓

Presentation Adapter

↓

Business Engine
```

The implementation order shall never be reversed.

Business data must never determine the screen structure.

---

## 17.2 Layout Authority

The screen architecture owns

Zone structure

Row order

Grid definition

Card placement

Spacing

Alignment

Responsive behaviour

Business data owns

Values

Analysis

Interpretation

Recommendations

Knowledge

Presentation never depends on business data.

---

## 17.3 Cursor MUST

Cursor MUST

✓ Build every Result Page according to official Zones.

✓ Keep Row order unchanged.

✓ Keep Grid structure fixed.

✓ Use official Card components.

✓ Consume only ViewModels.

✓ Use Presentation Adapter.

✓ Preserve equal-height rows.

✓ Preserve official spacing.

✓ Preserve official typography.

✓ Preserve responsive hierarchy.

✓ Preserve visual rhythm.

✓ Keep Summary Zone above the fold whenever possible.

✓ Preserve reading flow.

---

## 17.4 Cursor MUST NOT

Cursor MUST NOT

✗ Move cards between Zones.

✗ Create new Row structures.

✗ Allow dynamic content to resize cards.

✗ Allow Grid to be controlled by data.

✗ Stretch neighbouring cards.

✗ Render unlimited paragraphs.

✗ Render raw Engine Models.

✗ Mix interpretation with recommendations.

✗ Mix knowledge with analysis.

✗ Duplicate cards.

✗ Introduce horizontal scrolling.

✗ Introduce nested scrolling.

---

## 17.5 Card Placement Rules

Every card has one official location.

Example

Executive Summary

↓

Summary Zone

Five Elements

↓

Analysis Zone

Recommendation

↓

Recommendation Zone

Knowledge Reference

↓

Knowledge Zone

Cards must never migrate between Zones.

---

## 17.6 Dynamic Content Rules

Long content should be handled using

Preview

↓

Expand

↓

Collapse

Card dimensions should remain stable.

The page should never reflow because of dynamic content.

---

## 17.7 Responsive Rules

Responsive layouts may

change column count

change spacing

change stacking order within a row

Responsive layouts may not

change reading order

change Zone order

change analytical priority

hide critical information

---

## 17.8 Future Extension

Future analytical modules should be added

inside existing Zones

whenever possible.

Creating a new Zone requires

Design System approval

architecture review

documentation update

before implementation.

---

# 18. Acceptance Criteria & Screen Compliance

This chapter defines the official validation checklist for every Result Page.

No screen should be accepted until all requirements are satisfied.

---

## 18.1 Screen Architecture

✓ Correct Zone sequence.

✓ Correct Row sequence.

✓ Correct Grid layout.

✓ Correct Card placement.

✓ Stable layout.

---

## 18.2 Summary Zone

✓ Executive Summary displayed first.

✓ Core Indicators visible.

✓ Life Direction visible.

✓ No detailed interpretation.

✓ Reading time below one minute.

---

## 18.3 Analysis Zone

✓ Analytical cards grouped correctly.

✓ Equal-height rows.

✓ One purpose per card.

✓ Preview before detail.

✓ No duplicated information.

---

## 18.4 Visualization Zone

✓ Charts support analysis.

✓ Text summary available.

✓ Fixed card height.

✓ No decorative charts.

✓ No empty visual containers.

---

## 18.5 Recommendation Zone

✓ Recommendations prioritised.

✓ Maximum five primary recommendations.

✓ Critical actions visible.

✓ Expand available for additional guidance.

---

## 18.6 Interpretation Zone

✓ Structured narrative.

✓ Expandable reading.

✓ Clear paragraph hierarchy.

✓ No wall of text.

---

## 18.7 Knowledge Zone

✓ Definitions separated from interpretation.

✓ References appear after analysis.

✓ Educational content grouped logically.

✓ Knowledge does not interrupt reading flow.

---

## 18.8 Responsive Behaviour

✓ Desktop compliant.

✓ Tablet compliant.

✓ Mobile compliant.

✓ Reading order preserved.

✓ No horizontal scrolling.

---

## 18.9 Accessibility

✓ Keyboard navigation.

✓ Visible focus.

✓ Readable typography.

✓ Sufficient contrast.

✓ Screen reader compatible.

---

## 18.10 Performance

✓ Stable rendering.

✓ No layout shift.

✓ Skeleton loading.

✓ Shared components.

✓ Reusable ViewModels.

---

## 18.11 Visual Quality

✓ Equal-height rows.

✓ Consistent spacing.

✓ Balanced whitespace.

✓ Stable alignment.

✓ Predictable visual rhythm.

✓ Professional appearance.

---

## 18.12 Design System Compliance

The Result Page is considered compliant only when

✓ PACK_01_DESIGN_PRINCIPLES is satisfied.

✓ PACK_02_LAYOUT_SYSTEM is satisfied.

✓ PACK_03_COMPONENT_STANDARD is satisfied.

✓ PACK_04_UI_PRESENTATION_STANDARD is satisfied.

✓ PACK_05_ACCESSIBILITY is satisfied.

✓ PACK_06_RESULT_PAGE_LAYOUT_STANDARD is satisfied.

---

## 18.13 Definition of Done

A Result Page is officially complete only when

✓ All Zones are implemented.

✓ All Rows follow the official architecture.

✓ All Cards follow the official placement matrix.

✓ Presentation Adapter is used.

✓ ViewModels are consumed.

✓ Responsive behaviour is verified.

✓ Accessibility validation passes.

✓ Layout remains stable with dynamic data.

✓ No Design System violations are present.

Only after all items above are satisfied may the implementation be merged into the main branch.

---

END OF DOCUMENT