# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# 05_VISUAL_HIERARCHY.md
# ============================================================================
#
# Version : 1.0.0
# Status  : FOUNDATION (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted visual hierarchy
# for Commercial UI V3.
#
# It governs:
#
# • Attention hierarchy
# • Typography hierarchy
# • Component prominence
# • Visual priority
# • Focus management
# • Cognitive load
#
# This document overrides all visual implementation decisions.
#
# ============================================================================

# 1. PURPOSE

Visual Hierarchy determines

WHAT USERS SEE FIRST.

The interface is successful only when
users naturally notice the intended information
without conscious effort.

Visual hierarchy is more important than decoration.

Good hierarchy reduces thinking.

Bad hierarchy creates noise.

------------------------------------------------------------------------------

# 2. GOLDEN RULE

Every viewport has

ONE

primary focus.

Everything else supports it.

Never create multiple competing focal points.

------------------------------------------------------------------------------

# 3. VISUAL PRIORITY LEVELS

Commercial UI V3 defines eight priority levels.

P0

Identity

P1

Overall Verdict

P2

First Recommendation

P3

Executive Insight

P4

Four Pillars

P5

Explainable Analysis

P6

Consultation Report

P7

Appendix

Nothing may visually exceed
its assigned priority.

------------------------------------------------------------------------------

# 4. VIEWPORT HIERARCHY

First Screen

Focus

Day Master

↓

Overall Verdict

↓

First Recommendation

↓

Supporting Metrics

Users must never
look at charts first.

------------------------------------------------------------------------------

Second Screen

Focus

Four Pillars

↓

Executive Insight

↓

Strength

↓

Weakness

Charts remain secondary.

------------------------------------------------------------------------------

Third Screen

Focus

Analysis Conclusion

↓

Explanation

↓

Evidence

↓

Rule

Never start with Rule.

------------------------------------------------------------------------------

Fourth Screen

Focus

Consultation Reading

Typography dominates.

No dashboard appearance.

------------------------------------------------------------------------------

Fifth Screen

Focus

Evidence

↓

Reference

↓

Appendix

Lowest visual priority.

------------------------------------------------------------------------------

# 5. TYPOGRAPHY HIERARCHY

Typography creates hierarchy.

Not colors.

Not borders.

Not shadows.

Level H1

Page identity.

Level H2

Major chapter.

Level H3

Section title.

Level H4

Analysis block.

Body

Reading.

Caption

Metadata.

Small

Reference.

Never skip levels.

------------------------------------------------------------------------------

# 6. COLOR HIERARCHY

Color communicates meaning.

Never importance.

Primary

Main conclusions.

Neutral

Reading.

Muted

Metadata.

Success

Positive confirmation.

Warning

Attention.

Danger

Critical warning.

Never use color
only to attract attention.

------------------------------------------------------------------------------

# 7. BORDER HIERARCHY

Borders exist only to clarify structure.

Never to create emphasis.

Allowed

Hairline divider.

Callout container.

Input controls.

Not allowed

Heavy cards everywhere.

Nested borders.

Decorative outlines.

------------------------------------------------------------------------------

# 8. CARD HIERARCHY

Cards are exceptions.

Not the default.

Cards may be used only for

Executive Hero

Important Recommendation

Critical Warning

Callout

Everything else

should rely on

Typography

Whitespace

Alignment

------------------------------------------------------------------------------

# 9. ICON HIERARCHY

Icons assist reading.

Icons never become
visual anchors.

Maximum one icon
per information group.

No icon walls.

------------------------------------------------------------------------------

# 10. BADGE HIERARCHY

Badges are metadata.

Never conclusions.

Never recommendations.

Never headlines.

Maximum

two badges

per visible block.

------------------------------------------------------------------------------

# 11. CHART HIERARCHY

Charts explain.

Charts do not conclude.

Charts support text.

Text always comes first.

Charts never exceed

40%

of a section's visual weight.

------------------------------------------------------------------------------

# 12. IMAGE HIERARCHY

Illustrations are optional.

Images support understanding.

Images never replace
analysis.

No decorative graphics.

------------------------------------------------------------------------------

# 13. WHITESPACE HIERARCHY

Whitespace is a component.

Whitespace separates ideas.

Whitespace creates rhythm.

Whitespace reduces stress.

Never fill empty space
without purpose.

------------------------------------------------------------------------------

# 14. INFORMATION DENSITY

Every screen has

one dominant message.

Maximum

three supporting ideas.

Everything else

must wait.

------------------------------------------------------------------------------

# 15. EMPHASIS RULES

Emphasis is achieved by

Order

↓

Size

↓

Weight

↓

Whitespace

↓

Contrast

Never by

Multiple colors

Large borders

Animations

Many badges

------------------------------------------------------------------------------

# 16. ANIMATION HIERARCHY

Animation guides attention.

Animation never entertains.

Allowed

Fade

Expand

Collapse

Scroll progress

Not allowed

Bounce

Flash

Continuous movement

Distracting transitions

------------------------------------------------------------------------------

# 17. SECTION RHYTHM

Every major section follows

Headline

↓

Summary

↓

Content

↓

Supporting Information

↓

Reference

Never mix these layers.

------------------------------------------------------------------------------

# 18. COGNITIVE LOAD

Readers should process

one concept

at a time.

Reduce

choices.

Reduce

noise.

Reduce

competition.

Increase

clarity.

------------------------------------------------------------------------------

# 19. VISUAL ANTI-PATTERNS

Commercial UI V3 must never become

A wall of cards.

A wall of badges.

A wall of charts.

A wall of borders.

A wall of icons.

A wall of metrics.

Every anti-pattern
increases cognitive load.

------------------------------------------------------------------------------

# 20. IMPLEMENTATION RULES

Frontend implementation

shall preserve

priority order.

Responsive layouts

shall preserve

focus order.

Dark mode

shall preserve

contrast hierarchy.

Themes

shall never change

visual priority.

------------------------------------------------------------------------------

# 21. ACCEPTANCE CRITERIA

Visual Hierarchy passes only when

Users know
where to look first.

Users understand
the most important conclusion
within seconds.

No visual competition exists.

Typography dominates.

Borders disappear.

Whitespace guides reading.

Charts support text.

Cards become rare.

The report feels calm.

The report feels premium.

------------------------------------------------------------------------------

# 22. FREEZE

This hierarchy becomes immutable
after approval.

Future UI redesigns

may improve aesthetics

but

shall never change

visual priority.

# ============================================================================
# END OF DOCUMENT
# ============================================================================