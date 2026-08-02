# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 06 — CURSOR WORK PACKAGE
# WP-0008 — EXPLAINABLE ANALYSIS
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Priority : CRITICAL

Work Package ID

WP-0008

Estimated Scope

Explainable Analysis Screen

Owner

Product Architecture

Executor

Cursor

==============================================================================
1. OBJECTIVE
==============================================================================

Implement

the Explainable Analysis Screen

according to

Commercial UI V3.

This screen

explains

why

the Analysis Engine

reached

its conclusions.

Every conclusion

must be

traceable,

understandable,

and

supported

by evidence.

==============================================================================

2. BUSINESS GOAL
==============================================================================

Increase

user trust

by presenting

transparent,

structured,

and

evidence-based

analysis.

Users

must understand

how

every major conclusion

was derived.

==============================================================================

3. REQUIRED SPECIFICATIONS
==============================================================================

Cursor MUST read

Pack 01

01_PRODUCT_VISION.md

02_INFORMATION_ARCHITECTURE.md

03_READING_JOURNEY.md

04_PAGE_LAYOUT.md

05_VISUAL_HIERARCHY.md

Pack 02

All Design System

Pack 03

05_EXPLAINABLE_ANALYSIS.md

09_RESPONSIVE_LAYOUTS.md

Pack 03.5

01_DESKTOP_WIREFRAMES.md

02_TABLET_WIREFRAMES.md

03_MOBILE_WIREFRAMES.md

05_READING_FLOW_VALIDATION.md

Pack 04

All Implementation Specifications

WP-0001

WP-0002

WP-0003

WP-0004

WP-0005

WP-0006

WP-0007

==============================================================================

4. SCOPE
==============================================================================

IN SCOPE

Explainable Analysis Header

↓

Executive Conclusion

↓

Explanation Blocks

↓

Evidence Blocks

↓

Rule References

↓

Confidence Indicators

↓

Knowledge References

↓

Recommendation

↓

Section Transition

OUT OF SCOPE

Consultation Report

Appendix

Navigation

==============================================================================

5. COMPONENTS TO IMPLEMENT
==============================================================================

Business Components

ExplainableAnalysis

AnalysisSection

ConclusionPanel

ExplanationPanel

EvidencePanel

RuleReferencePanel

ConfidencePanel

KnowledgeReferencePanel

RecommendationPanel

AnalysisSummary

Shared Components

SectionHeader

Callout

EvidenceRow

EvidenceList

ReferenceBlock

CitationRow

PropertyGrid

LabelValueRow

ConfidenceBadge

InformationBox

StatusBadge

ReadingProgress

Base Components

Consume only

WP-0002 components.

==============================================================================

6. LAYOUT REQUIREMENTS
==============================================================================

The screen

must follow

Commercial Report Layout V3.

Reading order

Section Title

↓

Conclusion

↓

Explanation

↓

Evidence

↓

Rule Reference

↓

Confidence

↓

Recommendation

↓

Transition

Never

present

Evidence

before

Conclusion.

==============================================================================

7. EXPLAINABILITY CONTRACT
==============================================================================

Every Analysis Block

must follow

exactly

the same structure.

Conclusion

↓

Explanation

↓

Evidence

↓

Rule Reference

↓

Confidence

↓

Recommendation

No block

may

change

this sequence.

==============================================================================

8. DATA BINDING
==============================================================================

Components

must consume

Explainable Analysis

View Models only.

Forbidden

Raw Payload

Rule Evaluation

Knowledge Query

Engine Invocation

Business Calculation

==============================================================================

9. STATE SUPPORT
==============================================================================

Every Business Component

must support

Loading

↓

Ready

↓

Empty

↓

Unavailable

↓

Error

according to

Presentation State Contract.

==============================================================================

10. ACCESSIBILITY
==============================================================================

Verify

Semantic Headings

↓

Logical Reading Order

↓

Keyboard Navigation

↓

Screen Reader Labels

↓

Focus Order

↓

Contrast

↓

Reduced Motion

Evidence

must remain

accessible

without

visual cues.

==============================================================================

11. RESPONSIVE
==============================================================================

Desktop

Report layout

↓

Tablet

Stacked sections

↓

Mobile

Single-column reading

Reading order

must remain

identical

across

all devices.

==============================================================================

12. PERFORMANCE
==============================================================================

Render

Conclusion

before

Evidence.

Render

Evidence

before

References.

Lazy-load

secondary

Knowledge References

when appropriate.

==============================================================================

13. STYLING
==============================================================================

Consume only

Design Tokens.

Forbidden

Hardcoded colors

Hardcoded spacing

Hardcoded typography

Hardcoded borders

Hardcoded shadows

==============================================================================

14. VISUAL VALIDATION
==============================================================================

Verify

Narrative hierarchy

↓

Evidence hierarchy

↓

Typography hierarchy

↓

Whitespace rhythm

↓

Section transitions

↓

Dark Theme

↓

Light Theme

==============================================================================

15. TESTING
==============================================================================

Execute

Build

↓

Lint

↓

Component Tests

↓

Binding Tests

↓

Accessibility Tests

↓

Responsive Tests

↓

Performance Tests

↓

Visual Regression

==============================================================================

16. DELIVERABLES
==============================================================================

Explainable Analysis Screen

↓

Business Components

↓

Styles

↓

Tests

↓

Documentation

↓

Visual Comparison

==============================================================================

17. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Reading Journey matches Pack 03.

✓ Every Conclusion has Explanation.

✓ Every Explanation has Evidence.

✓ Every Evidence links to Rule Reference.

✓ Confidence displayed consistently.

✓ Recommendation concludes each section.

✓ Design Tokens only.

✓ Binding unchanged.

✓ Accessibility PASS.

✓ Responsive PASS.

✓ Performance PASS.

✓ Tests PASS.

FAIL

✗ Evidence shown without Conclusion.

✗ Missing Rule References.

✗ Payload parsing.

✗ Hardcoded styling.

✗ Business logic inside Components.

✗ Dashboard appearance.

==============================================================================

18. ROLLBACK
==============================================================================

Rollback

must restore

the previous

Explainable Analysis Screen

without

affecting

Metrics

or

Consultation Report.

==============================================================================

19. REQUIRED OUTPUT
==============================================================================

Cursor must provide

Implementation Summary

↓

Files Changed

↓

Business Components Created

↓

Visual Comparison

↓

Binding Validation

↓

Accessibility Report

↓

Performance Report

↓

Acceptance Checklist

==============================================================================

20. REVIEW CHECKLIST
==============================================================================

Architecture

□ PASS

Explainability

□ PASS

Evidence Flow

□ PASS

Design Tokens

□ PASS

Binding

□ PASS

Accessibility

□ PASS

Responsive

□ PASS

Performance

□ PASS

Testing

□ PASS

==============================================================================

21. EXECUTION PROMPT
==============================================================================

Implement

WP-0008 only.

Implement

Explainable Analysis Screen only.

Consume

Shared Components

from WP-0003.

Do not implement

Consultation Report

Appendix

Navigation

Do not modify

Backend

Bindings

Business Logic

Database

Analysis Engine

Knowledge Base

Return

1.

Files Changed

2.

Business Components Created

3.

Visual Comparison

4.

Binding Validation

5.

Accessibility Validation

6.

Performance Validation

7.

Acceptance Checklist

==============================================================================

22. EXPLAINABLE ANALYSIS CONTRACT (EAC)
==============================================================================

Every analysis

must be

fully traceable.

The user

must be able

to navigate

from

Conclusion

↓

Explanation

↓

Evidence

↓

Rule Reference

↓

Knowledge Source

without

ambiguity.

Business Components

must never

hide

supporting evidence.

==============================================================================

23. REFERENCE SCREENSHOT CONTRACT (RSC)
==============================================================================

The implementation

must be validated

against

Approved Desktop Wireframe

↓

Approved Tablet Wireframe

↓

Approved Mobile Wireframe

↓

Pack 03 Screen Specification

↓

Commercial UI V3 Visual Hierarchy

No layout deviation

is permitted

without

Product Architecture approval.

==============================================================================

24. FREEZE
==============================================================================

After approval,

WP-0008

becomes

Frozen.

The Explainable Analysis Screen

becomes

the canonical

explainability interface

for Commercial UI V3.

No redesign

is permitted

after Freeze.

# ============================================================================
# END OF DOCUMENT
# ============================================================================