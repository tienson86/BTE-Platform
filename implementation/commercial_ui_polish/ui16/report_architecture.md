# UI-16 Report Architecture

Status: IMPLEMENTATION  
Surface: `/report-preview` HTML preview  
Production PDF path: unchanged (`/reports`)

## Product model

The BTE report is an executive consulting document, not a printed dashboard.

Two reading depths share one layout:

- **Level A — Executive:** Cover, Executive Summary, Key Findings, Interpretation lead (`consulting_flow`), Top Priority.
- **Level B — Detailed:** Structured interpretation zones, full Action Plan, Luck timeline, Supporting Analysis, Appendix.

Prose is not duplicated between levels. Top Priority may appear as a compact finding highlight and as the dominant Action block.

## Information architecture

| # | Section | Source | Visual level |
|---|---------|--------|--------------|
| 01 | Cover | Product chrome + published identity | 1 Executive |
| 02 | Client profile | Canonical identity adapter | 2 Primary |
| 03 | Executive Summary | `NarrativeV2Presentation.overview` | 1 Executive |
| 04 | Core Chart Snapshot | Canonical BaZi / Five Elements / Pattern / current Luck | 2 Primary |
| 05 | Key Findings | Published headline, pattern, strength, top priority, current luck | 2 Primary |
| 06 | Interpretation | `interpretation.consulting_flow` then structured zones | 2 / 3 |
| 07 | Action Plan | `NarrativeV2Presentation.action_plan` | 1 / 2 |
| 08 | Timing / Luck | Canonical Luck adapter | 3 Analytical |
| 09 | Supporting Analysis | Canonical chart adapters, UI-15 viz kinds | 3 Analytical |
| 10 | Appendix | Product methodology + published versions | 4 Reference |

## Data ownership

- Narrative: `adaptNarrativeV2Presentation` only. No Pack05 fallback. No report-side composition.
- Structure: existing canonical adapters (`adaptBaziCard`, `adaptFiveElementsCard`, `adaptTenGodsCard`, `adaptPatternCard`, `adaptShenShaCard`, `adaptLuckCard`, `adaptIdentityHeader`).
- Missing optional fields are omitted. No diagnostic placeholders.

## Component system

`applications/customer_portal/src/screens/executive_report/`

ReportCover, ReportIdentity, ExecutiveSummarySection, ChartSnapshotSection, KeyFindingsSection, InterpretationSection, ActionPlanSection, LuckSection, SupportingAnalysisSection, ReportAppendix, ReportSectionHeader, ReportCallout, ReportMetric, ReportDivider.

## Preview route

`GET /report-preview` mounts `ExecutiveReportPage` on the ResultStore host.  
`GET /reports` continues to serve `reports.html`.
