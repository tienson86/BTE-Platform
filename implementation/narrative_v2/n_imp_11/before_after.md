# Before / after

## Before (production)

Portal `/result`, customer PDF, and customer DOCX still render Pack05 / Report Engine.
Those production paths were not switched in N-IMP-11.

## After (shadow)

Presentation Export Layer renders NarrativeV2Presentation v2.1 only:

- status: partial
- version: bte.presentation.v2.1
- Portal shadow JSON = Presentation
- PDF shadow / DOCX shadow / JSON shadow share the same blocks
- No new Meaning, no consumer compose
