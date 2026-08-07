# PACK_03_COMPONENT_STANDARD.md

Version: 1.0
Status: OFFICIAL
Owner: BTE UI Architecture

Depends on

- PACK_01_DESIGN_PRINCIPLES.md
- PACK_02_LAYOUT_SYSTEM.md

---

# 1. Purpose

This document defines the official component standard for the BTE Platform.

Every reusable UI component must follow this specification.

No component may define its own visual language.

All applications across the BTE ecosystem must reuse these standards.

---

# 2. Component Philosophy

Components are building blocks.

A component should solve one problem only.

A component should never contain business logic.

Business logic belongs to the Engine.

Presentation belongs to the Component.

---

# 3. Component Hierarchy

Application

↓

Page

↓

Section

↓

Layout

↓

Card

↓

Component

↓

Primitive

---

# 4. Component Categories

The BTE Platform defines the following categories.

Layout

Navigation

Display

Input

Feedback

Data Visualization

Analysis

Report

Utility

---

# 5. Layout Components

Official layout components

AppLayout

Header

Sidebar

ContentArea

Section

Grid

CardContainer

Divider

Spacer

---

# 6. Navigation Components

Navigation components

Sidebar Menu

Top Navigation

Breadcrumb

Tabs

Pagination

Step Indicator

Action Toolbar

---

# 7. Display Components

Display components

Card

Badge

Tag

Avatar

Label

Statistic

Score

Progress

Timeline

Metric

Highlight

Insight

---

# 8. Input Components

Text Input

Textarea

Number Input

Select

Multi Select

Date Picker

Checkbox

Radio

Toggle

Slider

Search Box

---

# 9. Feedback Components

Alert

Toast

Dialog

Modal

Notification

Loading

Skeleton

Empty State

Error State

Success State

---

# 10. Data Components

Table

List

Tree

Accordion

Key Value

Description List

Comparison Table

Property Grid

---

# 11. Analysis Components

These are BTE-specific.

Analysis Card

Score Card

Strength Card

Useful God Card

Pattern Card

Ten Gods Card

Luck Card

Recommendation Card

Interpretation Card

Knowledge Card

These components should not exist outside BTE.

---

# 12. Report Components

Executive Summary

Chapter

Paragraph

Reference

Footnote

Quote

Recommendation Block

Conclusion

---

# 13. Component Anatomy

Every component contains

Container

↓

Header

↓

Body

↓

Footer (optional)

↓

Actions (optional)

↓

Metadata (optional)

---

# 14. Component States

Every interactive component supports

Default

Hover

Focus

Active

Disabled

Loading

Error

Success

Empty

---

# 15. Component Sizes

Official size scale

XS

S

M

L

XL

No custom sizing.

---

# 16. Border Radius

Official radius

Small

6px

Medium

10px

Large

14px

Round

9999px

---

# 17. Elevation

Level 0

Flat

Level 1

Card

Level 2

Dropdown

Level 3

Dialog

Level 4

Modal

Avoid excessive shadows.

---

# 18. Typography

Title

Subtitle

Body

Caption

Label

Code

Number

Only official typography styles may be used.

---

# 19. Icons

Icons communicate meaning.

Never decorate.

Maximum icon sizes

16

20

24

32

---

# 20. Buttons

Button types

Primary

Secondary

Ghost

Danger

Icon

Link

Loading

Disabled

---

# 21. Cards

Every card contains

Header

↓

Content

↓

Optional Footer

Cards never scroll horizontally.

Cards never resize because of content.

---

# 22. Badges

Badges represent status.

Never use badges as buttons.

Official colors only.

---

# 23. Score Components

Every score displays

Numeric Score

↓

Level

↓

Color

↓

Meaning

↓

Trend (optional)

---

# 24. Tables

Tables support

Sorting

Filtering

Pagination

Sticky Header

Responsive Collapse

No horizontal overflow whenever possible.

---

# 25. Timeline

Timeline contains

Date

↓

Event

↓

Description

↓

Status

---

# 26. Insight Components

Insight Card contains

Icon

↓

Headline

↓

Summary

↓

Read More

Never display long paragraphs.

---

# 27. Recommendation Components

Contains

Priority

↓

Action

↓

Reason

↓

Expected Benefit

---

# 28. Empty State

Contains

Illustration

↓

Title

↓

Description

↓

Action

---

# 29. Skeleton

Skeleton dimensions must exactly match final layout.

No layout jumping.

---

# 30. Error Component

Contains

Error Title

↓

Reason

↓

Recovery

↓

Retry

---

# 31. Loading Component

Contains

Spinner or Skeleton

↓

Status Message

Never freeze the interface.

---

# 32. Expandable Components

Expandable components support

Collapsed

↓

Preview

↓

Expanded

↓

Collapse

Never auto-expand.

---

# 33. Responsive Rules

Components must adapt by

Width

Spacing

Typography

Never by changing purpose.

---

# 34. Accessibility

Every component supports

Keyboard Navigation

Focus Ring

Screen Reader Labels

ARIA Roles

Contrast Requirements

---

# 35. Reusability Rules

Components must

Be reusable

Be composable

Be independent

Contain no business logic

Receive data only through props

Never fetch data directly

---

# 36. Anti-Patterns

Never

❌ Put API calls inside components

❌ Mix layout with logic

❌ Hardcode colors

❌ Hardcode spacing

❌ Hardcode typography

❌ Duplicate components

❌ Create similar components with different names

❌ Allow unlimited content expansion

---

# 37. Component Naming

Official naming

Card

Badge

Button

Section

Panel

Table

Timeline

Insight

Recommendation

Avoid

Widget

Box

Container1

Container2

CustomCard

SpecialCard

---

# 38. Relationship

Layout

↓

PACK_02_LAYOUT_SYSTEM

Presentation

↓

PACK_04_UI_PRESENTATION_STANDARD

Accessibility

↓

PACK_05_ACCESSIBILITY

---

# 39. Acceptance Criteria

A component complies if

✓ Single responsibility

✓ Reusable

✓ Responsive

✓ Accessible

✓ Independent

✓ Uses official spacing

✓ Uses official typography

✓ Uses official colors

✓ Uses official states

✓ No business logic

✓ Compatible with Presentation Layer

---

END OF DOCUMENT