# ============================================================================
# BTE PLATFORM
# COMMERCIAL UI V3
# PACK 03 — SCREEN SPECIFICATION
# 07_APPENDIX.md
# ============================================================================

Version : 1.0.0

Status : Freeze Candidate

Owner : Product Architecture

Related Documents

- Pack 01 Product Vision
- Pack 02 Design System
- 00_SCREEN_SPEC_STANDARD.md
- 06_CONSULTATION_REPORT.md

==============================================================================
1. BUSINESS GOAL
==============================================================================

The Appendix is the supporting knowledge layer
of the Consultation Report.

Its purpose is

not

to introduce new conclusions.

Its purpose is

to strengthen trust

through

references,

evidence,

classical sources,

definitions,

and

related knowledge.

It serves readers
who wish to verify
or study the report in greater depth.

==============================================================================

2. USER GOAL
==============================================================================

Users want to know

• Where does this conclusion come from?

• Which rule supports it?

• Which classical text is referenced?

• Where can I learn more?

• What related topics should I explore?

==============================================================================

3. READING GOAL
==============================================================================

After reading the Appendix

users should

understand the origin

of every important conclusion

and

feel confident

that the report
is evidence-based.

==============================================================================

4. SUCCESS CRITERIA
==============================================================================

The Appendix succeeds only when

users can trace

a report conclusion

↓

its evidence

↓

its governing rule

↓

its knowledge source.

==============================================================================

5. USER QUESTIONS ANSWERED
==============================================================================

Q1

What evidence supports this?

↓

Evidence

--------------------------------------------------

Q2

Which rule?

↓

Rule Reference

--------------------------------------------------

Q3

Which classical source?

↓

Citation

--------------------------------------------------

Q4

What terminology is used?

↓

Glossary

--------------------------------------------------

Q5

Where should I continue learning?

↓

Related Knowledge

==============================================================================

6. INFORMATION PRIORITY
==============================================================================

Priority 0

Evidence

--------------------------------------------------

Priority 1

Rule Reference

--------------------------------------------------

Priority 2

Classical Citation

--------------------------------------------------

Priority 3

Glossary

--------------------------------------------------

Priority 4

Related Topics

==============================================================================

7. EXPECTED READING TIME
==============================================================================

2–10 minutes

Appendix supports

verification

rather than

primary reading.

==============================================================================

8. ASCII LAYOUT
==============================================================================

+------------------------------------------------------------------+

APPENDIX

--------------------------------------------------------------------

Evidence

--------------------------------------------------------------------

Rule References

--------------------------------------------------------------------

Classical Sources

--------------------------------------------------------------------

Glossary

--------------------------------------------------------------------

Related Knowledge

--------------------------------------------------------------------

Further Reading

+------------------------------------------------------------------+

==============================================================================

9. COMPONENT TREE
==============================================================================

Appendix

├── EvidenceSection

├── RuleReferenceSection

├── ClassicalSourceSection

├── GlossarySection

├── RelatedKnowledgeSection

└── FurtherReadingSection

==============================================================================

10. SECTION CONTRACT
==============================================================================

Every Appendix section
must contain

Heading

↓

Purpose

↓

Content

↓

Reference

↓

Related Links (optional)

Sections are independent

but follow
the same structure.

==============================================================================

11. GRID MAPPING
==============================================================================

Desktop

Single Reading Column

Tablet

Single Reading Column

Mobile

Single Reading Column

Appendix

must remain

document-oriented.

==============================================================================

12. SPACING MAPPING
==============================================================================

Uses only

Spacing Tokens

space.chapter

↓

space.section

↓

space.block

==============================================================================

13. TYPOGRAPHY ROLES
==============================================================================

Heading

↓

Reference Title

↓

Evidence

↓

Body

↓

Citation

↓

Metadata

==============================================================================

14. COLOR INTENT
==============================================================================

Neutral reading palette.

Semantic emphasis only

for

Evidence

Warning

Important Notes

==============================================================================

15. SURFACE ROLE
==============================================================================

One continuous document surface.

Appendix

must never appear

as a dashboard

or

a collection of unrelated cards.

==============================================================================

16. MOTION INTENT
==============================================================================

Guide

↓

Reveal

↓

Focus

Expand/Collapse

may be used

for optional details.

==============================================================================

17. INTERACTION RULES
==============================================================================

Click

↓

Open related reference

--------------------------------------------------

Copy

↓

Citation

--------------------------------------------------

Expand

↓

Evidence details

--------------------------------------------------

Keyboard

↓

Fully supported

==============================================================================

18. BINDING CONTRACT
==============================================================================

Consumes only

knowledge.*

references.*

citations.*

glossary.*

appendix.*

No calculations.

No inference.

No rewriting.

==============================================================================

19. DATA DEPENDENCIES
==============================================================================

Required

Evidence

Rule References

Optional

Classical Sources

Glossary

Related Knowledge

Further Reading

==============================================================================

20. LOADING STATE
==============================================================================

Display

Appendix Skeleton

Maintain

document layout.

==============================================================================

21. EMPTY STATE
==============================================================================

Display

"No supporting references available."

Offer

Return to Report.

==============================================================================

22. UNAVAILABLE STATE
==============================================================================

Unavailable items

display

Unavailable

Never fabricate

references

or

citations.

==============================================================================

23. ERROR STATE
==============================================================================

Display

Friendly explanation.

Retry.

Diagnostic identifier.

==============================================================================

24. RESPONSIVE BEHAVIOUR
==============================================================================

Desktop

Continuous reading.

Tablet

Continuous reading.

Mobile

Single-column reading.

Information order

never changes.

==============================================================================

25. ACCESSIBILITY
==============================================================================

Semantic headings.

Keyboard navigation.

Screen readers.

Visible focus.

Reduced Motion.

WCAG AA.

==============================================================================

26. PERFORMANCE BUDGET
==============================================================================

Initial render

under 100 ms.

Long evidence lists

may lazy render.

==============================================================================

27. COGNITIVE OUTCOME
==============================================================================

After reading

users should

trust

the report

because

every conclusion

can be traced

to

evidence

and

knowledge.

==============================================================================

28. ANTI-PATTERNS
==============================================================================

Commercial UI V3 must never

✗ Introduce new conclusions.

✗ Hide references.

✗ Display raw database records.

✗ Mix unrelated knowledge.

✗ Overwhelm users

with unnecessary detail.

✗ Replace references

with AI-generated content.

==============================================================================

29. ACCEPTANCE CRITERIA
==============================================================================

PASS

✓ Evidence supports conclusions.

✓ Rule references are traceable.

✓ Classical sources are identifiable.

✓ Related knowledge extends understanding.

✓ Appendix feels like part of the report.

FAIL

✗ References missing.

✗ Evidence disconnected.

✗ Raw technical data shown.

✗ Appendix appears as an independent module.

==============================================================================

30. FUTURE EXTENSIONS
==============================================================================

May support

Interactive Classical Explorer

Knowledge Graph

Citation Export

Reference Comparison

Academic Sources

without changing

Appendix Structure

or

Binding Contract.

==============================================================================

31. IMPLEMENTATION NOTES
==============================================================================

This specification defines

Supporting Reading Experience

Knowledge Structure

Binding

State Behaviour

Acceptance Rules

It does NOT define

HTML

CSS

React

Vue

Knowledge retrieval logic.

==============================================================================

32. FREEZE
==============================================================================

After approval

Appendix becomes

the canonical

knowledge support layer

of Commercial UI V3.

Every implementation

must preserve

Business Goal

Reading Goal

Evidence hierarchy

Knowledge hierarchy

and

Binding Contract.

# ============================================================================
# END OF DOCUMENT
# ============================================================================