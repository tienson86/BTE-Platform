# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# 02_INFORMATION_ARCHITECTURE.md
# ============================================================================
#
# Version : 1.0.0
# Status  : FOUNDATION (Freeze Candidate)
# Owner   : Product Architecture
#
# This document defines the ONLY accepted information architecture
# for all BaZi consultation reports.
#
# It governs:
#
# • Reading sequence
# • Information priority
# • Section hierarchy
# • Progressive disclosure
# • User cognition
#
# This document overrides screen-level implementation decisions.
#
# ============================================================================

# 1. PURPOSE

The purpose of this document is to define

HOW INFORMATION IS ORGANIZED.

NOT

how it looks.

NOT

how it is implemented.

NOT

how components are rendered.

Information Architecture exists independently
from UI components.

------------------------------------------------------------------------------

# 2. FUNDAMENTAL PRINCIPLE

Users do NOT come to BTE to browse data.

Users come to BTE to understand themselves.

Therefore the report is organized around

QUESTIONS

instead of

DATA TYPES.

Wrong

↓

Chart

↓

Rules

↓

Analysis

↓

Knowledge

Correct

↓

Who am I?

↓

Is my chart good?

↓

Why?

↓

What should I do?

↓

Can I trust this?

------------------------------------------------------------------------------

# 3. REPORT ARCHITECTURE

The report contains exactly six chapters.

They are NOT dashboards.

They are NOT modules.

They are chapters of one consultation report.

Chapter 1

Executive Summary

↓

Chapter 2

BaZi Chart

↓

Chapter 3

Executive Insight

↓

Chapter 4

Explainable Analysis

↓

Chapter 5

Consultation Report

↓

Chapter 6

Appendix

No additional primary chapters are allowed.

------------------------------------------------------------------------------

# 4. CHAPTER PURPOSES

Chapter 1

Executive Summary

Purpose

Immediate understanding.

The reader must understand the chart
within seconds.

Contains

• Identity

• Overall verdict

• Recommendation

Must NOT contain

Detailed rules.

--------------------------------------------------

Chapter 2

BaZi Chart

Purpose

Present the chart visually.

The chart is

NOT

the conclusion.

It is evidence.

Must remain compact.

--------------------------------------------------

Chapter 3

Executive Insight

Purpose

Summarize strengths.

Summarize weaknesses.

Summarize opportunities.

Summarize risks.

No detailed reasoning.

--------------------------------------------------

Chapter 4

Explainable Analysis

Purpose

Explain WHY.

Every conclusion must be supported.

Conclusion

↓

Explanation

↓

Evidence

↓

Rule

↓

Confidence

↓

Knowledge

--------------------------------------------------

Chapter 5

Consultation Report

Purpose

Professional reading.

Long-form interpretation.

Natural language.

Book-like reading.

No dashboard layout.

--------------------------------------------------

Chapter 6

Appendix

Purpose

Evidence.

Knowledge.

Classical references.

Rule traceability.

Not intended for first-time readers.

------------------------------------------------------------------------------

# 5. INFORMATION FLOW

Information always moves from

Simple

↓

Detailed

↓

Evidence

↓

Reference

Never reverse this order.

Never expose raw rules
before users understand the conclusion.

------------------------------------------------------------------------------

# 6. READING DEPTH

The report supports multiple reading depths.

Depth 1

3 seconds

Executive Summary

--------------------------------------------------

Depth 2

30 seconds

Executive Insight

--------------------------------------------------

Depth 3

2 minutes

Explainable Analysis

--------------------------------------------------

Depth 4

10 minutes

Consultation Report

--------------------------------------------------

Depth 5

Unlimited

Appendix

Users may stop reading
at any depth.

Every depth must still provide value.

------------------------------------------------------------------------------

# 7. INFORMATION PRIORITY

Priority P0

Identity

--------------------------------------------------

Priority P1

Overall Verdict

--------------------------------------------------

Priority P2

Recommendation

--------------------------------------------------

Priority P3

Strengths / Weaknesses

--------------------------------------------------

Priority P4

Analysis

--------------------------------------------------

Priority P5

Interpretation

--------------------------------------------------

Priority P6

Evidence

--------------------------------------------------

Priority P7

References

Lower priorities
must never visually dominate
higher priorities.

------------------------------------------------------------------------------

# 8. PROGRESSIVE DISCLOSURE

Never display everything immediately.

Readers should progressively discover:

Overview

↓

Insight

↓

Explanation

↓

Evidence

↓

References

Every deeper layer
must answer a new question.

Never repeat information.

------------------------------------------------------------------------------

# 9. WHAT MUST NEVER HAPPEN

The report must NEVER become

Dashboard

↓

Dashboard

↓

Dashboard

↓

Dashboard

It must NEVER feel like

multiple pages glued together.

It must ALWAYS feel like

one continuous consultation.

------------------------------------------------------------------------------

# 10. SECTION TRANSITIONS

Transitions between chapters
must feel natural.

Do NOT separate chapters
using heavy borders.

Use

Whitespace

Typography

Rhythm

to indicate transitions.

The reader should never feel

"I entered another page."

------------------------------------------------------------------------------

# 11. USER COGNITIVE LOAD

At any point

the reader should focus on

ONE primary message.

Never compete
for attention.

One chapter

↓

One message

↓

One focus.

------------------------------------------------------------------------------

# 12. IMPLEMENTATION RULES

Frontend implementation

shall NOT

change this architecture.

Responsive layouts

shall preserve

reading order.

Dark mode

shall preserve

information hierarchy.

Animations

shall reinforce

reading flow,

not distract.

------------------------------------------------------------------------------

# 13. ACCEPTANCE

Information Architecture passes
only when:

The reader can understand

without reading everything.

The report feels continuous.

No dashboard feeling exists.

No duplicated information exists.

No chapter competes
with another chapter.

The reader always knows

where they are,

why they are there,

and

what comes next.

------------------------------------------------------------------------------

# 14. FREEZE

This Information Architecture
becomes immutable after approval.

Future UI redesigns

must preserve

this architecture.

Only business strategy changes

may modify this document.

# ============================================================================
# END OF DOCUMENT
# ============================================================================