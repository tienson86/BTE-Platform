# Report Template Traceability Specification

**Document:** TRACEABILITY_SPEC  
**Module:** knowledge/report_templates  
**Version:** V1.0.0  
**Status:** Official  

---

## Purpose

Ensure every Official report template can be traced to Knowledge, Rules, Sentences, and References.

---

## Traceability Model

```
Reference (REF-*)
      ↓
Knowledge (KNO-*) / Rules (RUL-*) / Sentences (SEN-*)
      ↓
Report Template (RPT-*)
      ↓
Rendered Report
```

Governance expects reports to reference Sentences. This framework records Sentence Links explicitly without modifying Governance files.

---

## Required Trace Concerns

| Concern | Requirement |
|---------|-------------|
| Report Template ID | Stable `RPT-NNNNNN` |
| Structure | Ordered section outline |
| Sentence Links | Wording sources |
| Knowledge / Rule Links | Doctrinal / decision grounding |
| Reference Links | Source authority when needed |
| Audience / Language | Communicative contract |
| Version / Status | Lifecycle evidence |

---

## Traceability Levels

| Level | Meaning |
|-------|---------|
| L0 | Framework stub only |
| L1 | Metadata + structure draft |
| L2 | L1 + ≥1 Sentence or Knowledge link |
| L3 | L2 + Rule and/or Reference links |
| L4 | Fully reviewed Official network |

Framework V1.0.0 remains at L0 globally.

---

## Official Gate

An Official template SHOULD reach at least **L2**.

Client-facing thematic templates SHOULD target **L3+**.

---

## Audit Checklist

- [ ] Template ID listed in domain INDEX when content exists
- [ ] Domain path matches Domain metadata
- [ ] Structure sections ordered and non-empty for Official
- [ ] Links resolve when listed
- [ ] Status / Version present

---

## Boundaries

- Does not modify frozen Knowledge Infrastructure modules
- Does not implement report renderers in this phase
