# BTE Document Creation Procedure

## Document Information

| Field | Value |
|------|------|
| Document ID | BTE-SOP-001 |
| Document Name | Document Creation Procedure |
| Version | V1.0.0 |
| Status | Official |
| Category | Governance Procedure |
| Applies To | All Knowledge Assets |
| Last Updated | 2026-07-30 |

---

# 1. Purpose

This Standard Operating Procedure (SOP) defines the official process for creating new Knowledge Assets within the BTE Knowledge Platform.

Its objectives are:

- Ensure consistency.
- Ensure completeness.
- Ensure traceability.
- Ensure governance compliance.
- Support AI-ready knowledge creation.

Every official Knowledge Asset SHALL follow this procedure.

---

# 2. Scope

This procedure applies to the creation of:

- Knowledge Chapters
- Knowledge Sections
- Rules
- Rule Collections
- Sentence Libraries
- Phrase Libraries
- Case Studies
- Glossary Entries
- Reference Records
- Metadata Files
- Report Templates
- Governance Documents

---

# 3. Preconditions

Before creating a new Knowledge Asset, the following conditions SHALL be satisfied:

- The asset does not already exist.
- The purpose has been defined.
- The scope has been approved.
- Related Standards are available.
- Required templates are available.
- Terminology has been verified.

---

# 4. Inputs

Required inputs include:

| Input | Description |
|------|-------------|
| Asset Type | Type of asset to be created |
| Asset Title | Official title |
| Module | Knowledge module |
| Metadata | Required metadata |
| References | Initial reference list |
| Related Assets | Dependencies |
| Author | Responsible creator |

---

# 5. Roles and Responsibilities

| Role | Responsibility |
|------|----------------|
| Author | Create the initial draft |
| Technical Reviewer | Verify structure and formatting |
| Knowledge Reviewer | Verify technical accuracy |
| Editorial Reviewer | Verify language and style |
| Governance Reviewer | Verify compliance |
| Approver | Approve official publication |

No individual should approve their own work.

---

# 6. Procedure Steps

## Step 1 — Identify Need

Determine whether a new Knowledge Asset is required.

Deliverables:

- Business justification
- Scope definition

---

## Step 2 — Verify Existing Assets

Search existing repositories to avoid duplication.

Verify:

- Knowledge Registry
- Rule Registry
- Terminology Registry
- Reference Registry

If an equivalent asset already exists, update the existing asset instead of creating a duplicate.

---

## Step 3 — Assign Asset ID

Generate an official Asset ID according to the Knowledge ID Specification.

Example:

```
KID-BZ-FND-CH01
```

The ID SHALL remain immutable throughout the asset lifecycle.

---

## Step 4 — Select Template

Choose the official template corresponding to the asset type.

Examples:

- Chapter Template
- Rule Template
- Case Study Template
- Reference Template
- Glossary Template

---

## Step 5 — Populate Metadata

Complete all mandatory metadata fields.

Mandatory fields include:

- Asset ID
- Title
- Version
- Status
- Author
- Module
- Language
- Tags
- Dependencies

Metadata SHALL comply with the Metadata Specification.

---

## Step 6 — Draft Content

Create the initial content following:

- Chapter Standard
- Markdown Standard
- Style Guide
- Terminology Standard

The draft should focus on correctness before optimization.

---

## Step 7 — Add References

Attach authoritative references using official Reference IDs.

Every major statement should be traceable.

---

## Step 8 — Link Dependencies

Identify upstream and downstream relationships.

Examples:

- Related Rules
- Related Chapters
- Related Cases
- Related References
- Related Terminology

---

## Step 9 — Self Validation

Before submission, the author SHALL verify:

- Metadata complete
- IDs valid
- Formatting compliant
- References valid
- Terminology compliant
- No duplicated content

---

## Step 10 — Submit for Review

Submit the completed draft to the Review Workflow.

The review process SHALL follow the Review Policy.

---

# 7. Outputs

Successful completion of this procedure produces:

- Draft Knowledge Asset
- Metadata
- Traceability Links
- Reference Mapping
- Validation Checklist
- Review Package

---

# 8. Validation

A Knowledge Asset SHALL NOT proceed to review unless:

- Metadata is complete.
- Asset ID is valid.
- Required sections exist.
- References are attached.
- Templates are followed.
- Terminology is compliant.

---

# 9. Exceptions

Emergency documentation may use an accelerated workflow.

The accelerated workflow SHALL still require:

- Metadata
- Asset ID
- Review
- Traceability

after publication.

---

# 10. Related Standards

- Canon Specification
- Markdown Standard
- Chapter Standard
- Metadata Specification
- Knowledge ID Specification
- Traceability Standard
- Knowledge Quality Standard
- Knowledge Style Guide

---

# 11. Related Policies

- Versioning Policy
- Change Management Policy
- Review Policy
- Release Policy
- Access Control Policy

---

# 12. Performance Indicators (KPIs)

The effectiveness of this procedure should be monitored using the following indicators:

| KPI | Target |
|------|--------|
| Metadata Completeness | 100% |
| Duplicate Asset Rate | < 1% |
| Validation Pass Rate | ≥ 95% |
| Review Rework Rate | < 10% |
| Traceability Coverage | 100% |
| Required References Present | 100% |

---

# 13. Process Flow

```
Need Identified
        │
        ▼
Verify Existing Assets
        │
        ▼
Assign Asset ID
        │
        ▼
Select Template
        │
        ▼
Populate Metadata
        │
        ▼
Draft Content
        │
        ▼
Add References
        │
        ▼
Link Dependencies
        │
        ▼
Self Validation
        │
        ▼
Submit for Review
        │
        ▼
Review Procedure
```

---

# 14. Compliance

Failure to comply with this procedure SHALL prevent a Knowledge Asset from entering the official BTE Knowledge Canon.

---

# Version History

| Version | Date | Description |
|----------|------|-------------|
| V1.0.0 | 2026-07-30 | Initial official release |