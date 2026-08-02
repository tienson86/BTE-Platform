# Business Components (WP-0004 … WP-0010)

Presentation components for Commercial UI V3 business screens.
Compose Shared Components only. Consume presentation ViewModels only.

## Consultation Report (WP-0009)

- ConsultationReport, ReportContainer, ReportHeader, ReportSection,
  ReportFooter, ReportProgress, SectionTransition, TableOfContents,
  PrintHeader, PrintFooter

## Appendix (WP-0010)

- AppendixContainer
- AppendixSummary
- GlossarySection
- TerminologySection
- KnowledgeReferenceSection
- RuleReferenceSection
- CitationSection
- CreditsSection
- VersionInformation

## Rules

- No Base Component imports (Shared only).
- No analysis, scoring, calculation, API, Knowledge lookup, or Rule Engine access.
- Support Loading / Ready / Empty / Unavailable / Error via presentation status.
- Public imports via barrel only.
