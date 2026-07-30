# BTE Report Template Framework

**Module:** Knowledge Report Templates  
**Version:** V1.0.0  
**Status:** Official Framework  
**Governance Alignment:** Governance V1.0 (frozen — not modified)  

Frozen modules (not modified by this framework):

- Governance V1.0
- Reference Library
- Terminology Framework
- Knowledge Canon Framework
- Rule Database Framework
- Sentence Library Framework
- Golden Dataset Framework

---

## Purpose

The Report Template Framework defines the architecture, standards, templates, and domain scaffolding for BTE report layouts that assemble Knowledge, Rules, and Sentences into publishable reports.

This release is **framework only**. It does not author report contents, sample narratives, or rendered outputs.

---

## Scope

In scope:

- Framework documentation
- Domain directories and templates
- Traceability, quality, and review standards
- Registry scaffolding

Out of scope:

- Writing report body content
- Academic doctrine
- Runtime report rendering engines
- Changes to frozen Knowledge Infrastructure modules

---

## Directory Structure

```
knowledge/report_templates/
├── README.md
├── REPORT_TEMPLATE_SPEC.md
├── REPORT_TEMPLATE.md
├── TRACEABILITY_SPEC.md
├── QUALITY_STANDARD.md
├── REVIEW_GUIDE.md
├── CHANGELOG.md
├── EDGE_CASES.md
├── 01_basic/
├── 02_professional/
├── 03_business/
├── 04_marriage/
├── 05_career/
├── 06_health/
├── 07_children/
├── 08_wealth/
├── 09_luck_cycles/
├── 10_custom/
└── registry/
```

Each domain contains `README.md`, `INDEX.md`, and `REPORT_TEMPLATE.md`.

---

## Report Template ID Format

```
RPT-000001
RPT-000002
...
```

Rules:

- IDs are immutable once published.
- Numbers are zero-padded to six digits.
- Domain is metadata, not part of the ID string.

---

## Mandatory Template Support

Every report template record MUST support:

| Field / Concern | Description |
|-----------------|-------------|
| Metadata | Administrative metadata block |
| Title | Human-readable template title |
| Domain | Framework domain directory |
| Category | Classification label |
| Audience | Intended audience |
| Language | Report language |
| Structure | Section outline placeholders |
| Knowledge Links | `KNO-*` IDs |
| Rule Links | `RUL-*` IDs |
| Sentence Links | `SEN-*` IDs |
| Reference Links | `REF-*` IDs |
| Version | `V#.#.#` |
| Status | Lifecycle status |
| Traceability | Trace level / notes |

---

## Domains

| # | Directory | Domain |
|---|-----------|--------|
| 01 | `01_basic/` | Basic |
| 02 | `02_professional/` | Professional |
| 03 | `03_business/` | Business |
| 04 | `04_marriage/` | Marriage |
| 05 | `05_career/` | Career |
| 06 | `06_health/` | Health |
| 07 | `07_children/` | Children |
| 08 | `08_wealth/` | Wealth |
| 09 | `09_luck_cycles/` | Luck Cycles |
| 10 | `10_custom/` | Custom |

---

## Related Documents

| Document | Role |
|----------|------|
| [REPORT_TEMPLATE_SPEC.md](REPORT_TEMPLATE_SPEC.md) | Formal specification |
| [REPORT_TEMPLATE.md](REPORT_TEMPLATE.md) | Root template |
| [TRACEABILITY_SPEC.md](TRACEABILITY_SPEC.md) | Traceability rules |
| [QUALITY_STANDARD.md](QUALITY_STANDARD.md) | Quality rules |
| [REVIEW_GUIDE.md](REVIEW_GUIDE.md) | Review procedure |
| [EDGE_CASES.md](EDGE_CASES.md) | Edge cases |
| [CHANGELOG.md](CHANGELOG.md) | Module history |
| [registry/](registry/) | Central registry scaffolding |

---

## Architecture Position

```
Knowledge / Rules / Sentences / References
                    ↓
         Report Template (RPT-*)
                    ↓
            Rendered Report
```
