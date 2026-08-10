# Data Retention Policy

**Template for legal review**

This document is a production-ready draft template. It is **not legal advice**. Retention periods below are **proposed operational defaults**, not legal requirements, until counsel and the data controller confirm them.

---

Version: 1.0.0-draft  
Product: BTE Product v1.0

## Principles

Keep data only as long as needed for the Service, support, security, and legal holds. Do not retain birth data “forever” by accident.

## Proposed defaults (for review)

| Record | Proposed retain | Owner |
|--------|-----------------|-------|
| Customer profile / license | Term + 24 months | commercial + ops |
| Analysis inputs & report ids | Term + 24 months or Customer delete request | ops |
| Application / access logs | 14–30 days (see logging catalog) | platform-ops |
| Audit / security logs | 90 days | security-owner |
| Backups | Rolling per backup policy (RPO 24h ops target) | platform-ops |
| Support tickets | 36 months | support |

## Deletion / export

**[Counsel to insert process, identity verification, and exceptions for legal hold.]**

## Anonymization

Where feasible, operational metrics should not require raw birth data.

---

END
