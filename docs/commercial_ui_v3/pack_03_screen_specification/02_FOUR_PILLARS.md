# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 02_FOUR_PILLARS.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

Related Documents

- Pack 01 Product Vision
- Pack 02 Design System
- 00_SCREEN_SPEC_STANDARD.md

==============================================================================
1. BUSINESS GOAL
==============================================================================

The Four Pillars screen explains
the structural foundation
of the BaZi chart.

Its objective is not prediction.

Its objective is to help users understand

how their chart is constructed,

what each pillar represents,

and

why the Day Pillar is the center
of the entire interpretation.

==============================================================================

2. USER GOAL
==============================================================================

Users want to know

• What are my Four Pillars?

• Which pillar is the Day Master?

• What does each pillar represent?

• What hidden information exists inside each pillar?

==============================================================================

3. READING GOAL
==============================================================================

After reading this screen
users should understand

✓ Four Pillars

✓ Heavenly Stem

✓ Earthly Branch

✓ Hidden Stems

✓ Ten Gods relationship

✓ Na Yin

✓ Twelve Life Stages

without requiring interpretation.

==============================================================================

4. SUCCESS CRITERIA
==============================================================================

The screen succeeds only when

users can correctly identify

Year Pillar

↓

Month Pillar

↓

Day Pillar

↓

Hour Pillar

and recognize
the Day Pillar
as the visual center.

==============================================================================

5. USER QUESTIONS ANSWERED
==============================================================================

Q1

How is my chart structured?

↓

Four Pillars

--------------------------------------------------

Q2

Which pillar represents me?

↓

Day Pillar

--------------------------------------------------

Q3

What is inside each pillar?

↓

Stem

↓

Branch

↓

Hidden Stems

↓

Ten Gods

↓

Na Yin

↓

Life Stage

==============================================================================

6. INFORMATION PRIORITY
==============================================================================

Priority 0

Day Pillar

--------------------------------------------------

Priority 1

Four Pillars

--------------------------------------------------

Priority 2

Hidden Stems

--------------------------------------------------

Priority 3

Ten Gods

--------------------------------------------------

Priority 4

Na Yin

Life Stage

==============================================================================

7. EXPECTED READING TIME
==============================================================================

20–40 seconds

The objective is

structural understanding,

not detailed analysis.

==============================================================================

8. ASCII LAYOUT
==============================================================================

+--------------------------------------------------------------------------+

                         FOUR PILLARS

+------------+ +------------+ +==================+ +------------+

| Year       | | Month      | | Day (Center)     | | Hour       |

| Heavenly   | | Heavenly   | | Heavenly         | | Heavenly   |

| Stem       | | Stem       | | Stem             | | Stem       |

|------------| |------------| |------------------| |------------|

| Earthly    | | Earthly    | | Earthly          | | Earthly    |

| Branch     | | Branch     | | Branch           | | Branch     |

|------------| |------------| |------------------| |------------|

| Hidden     | | Hidden     | | Hidden           | | Hidden     |

| Stems      | | Stems      | | Stems            | | Stems      |

|------------| |------------| |------------------| |------------|

| Ten Gods   | | Ten Gods   | | Ten Gods         | | Ten Gods   |

|------------| |------------| |------------------| |------------|

| Na Yin     | | Na Yin     | | Na Yin           | | Na Yin     |

|------------| |------------| |------------------| |------------|

| Life Stage | | Life Stage | | Life Stage       | | Life Stage |

+------------+ +------------+ +==================+ +------------+

==============================================================================

9. COMPONENT TREE
==============================================================================

FourPillarsWorkspace

├── PillarColumn (Year)

├── PillarColumn (Month)

├── PillarColumn (Day)

├── PillarColumn (Hour)

Each PillarColumn

├── HeavenlyStem

├── EarthlyBranch

├── HiddenStemGroup

├── TenGodBadge

├── NaYinLabel

└── LifeStageLabel

==============================================================================

10. GRID MAPPING
==============================================================================

Desktop

4 equal columns

Day Pillar emphasized.

Tablet

4 columns

or

2 × 2

depending on width.

Mobile

Vertical stack.

==============================================================================

11. SPACING MAPPING
==============================================================================

Uses only

Spacing Tokens

space.section

space.block

space.inline

==============================================================================

12. TYPOGRAPHY ROLES
==============================================================================

Section Title

↓

Pillar Title

↓

Stem

↓

Branch

↓

Metadata

==============================================================================

13. COLOR INTENT
==============================================================================

Semantic colors only.

No Five Element colors
unless defined
by Design Tokens.

The Day Pillar emphasis
comes from hierarchy,

not decoration.

==============================================================================

14. SURFACE ROLE
==============================================================================

One Reading Surface.

Four visual columns.

No independent cards.

No dashboard widgets.

==============================================================================

15. MOTION INTENT
==============================================================================

Reveal

↓

Focus

Hover is optional.

Expand / Collapse
for metadata only.

==============================================================================

16. INTERACTION RULES
==============================================================================

Hover

Highlight current pillar.

Click / Tap

Expand metadata.

Keyboard

Tab navigation
through pillars.

==============================================================================

17. BINDING CONTRACT
==============================================================================

Consumes only

chart.year

chart.month

chart.day

chart.hour

chart.hidden_stems

chart.ten_gods

chart.nayin

chart.life_stage

No calculations.

No inference.

==============================================================================

18. DATA DEPENDENCIES
==============================================================================

Required

Four Pillars

Stem

Branch

Optional

Na Yin

Life Stage

Hidden Stems

==============================================================================

19. LOADING STATE
==============================================================================

Display

Four pillar skeletons

Maintain layout stability.

==============================================================================

20. EMPTY STATE
==============================================================================

If chart data
is unavailable

Display

"BaZi chart data is unavailable."

Provide

Retry

or

Return to Input.

==============================================================================

21. UNAVAILABLE STATE
==============================================================================

Missing values

display

Unavailable

Never display

null

undefined

or placeholder keys.

==============================================================================

22. ERROR STATE
==============================================================================

Show

Friendly explanation

Retry action

Diagnostic identifier

==============================================================================

23. RESPONSIVE BEHAVIOUR
==============================================================================

Desktop

Four columns.

Tablet

Four columns

or

2 × 2.

Mobile

Single column.

Reading order
must remain

Year

↓

Month

↓

Day

↓

Hour

==============================================================================

24. ACCESSIBILITY
==============================================================================

Keyboard navigation.

Screen reader labels.

Semantic headings.

Visible focus.

WCAG AA compliance.

==============================================================================

25. PERFORMANCE BUDGET
==============================================================================

Render

< 100 ms

No layout shift.

Lazy rendering
only for expandable metadata.

==============================================================================

26. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Four Pillars clearly distinguished.

✓ Day Pillar immediately recognizable.

✓ Metadata organized consistently.

✓ Reading order intuitive.

✓ Layout resembles a structured report.

FAIL

✗ Day Pillar not emphasized.

✗ Table-like appearance.

✗ Excessive borders.

✗ Nested cards.

✗ Visual clutter.

==============================================================================

27. FUTURE EXTENSIONS
==============================================================================

May support

Interactive highlighting

Cross-pillar relationships

Animated focus

AI explanations

without changing
the structural contract.

==============================================================================

28. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Structure

Hierarchy

Binding

Reading Behaviour

It does NOT define

HTML

CSS

React

Framework implementation.

==============================================================================

29. FREEZE
==============================================================================

After approval

Four Pillars becomes
the canonical structural view
of the BaZi chart.

All future implementations

must preserve

Business Goal

Reading Goal

Information Priority

Binding Contract

and Reading Hierarchy.

# ============================================================================
# END OF DOCUMENT
# ============================================================================