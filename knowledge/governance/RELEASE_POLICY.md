# Release Policy

**Module:** `knowledge/governance`  
**Document:** RELEASE_POLICY  
**Version:** V1.0.0  
**Status:** Official Foundation  

---

## 1. Purpose

Control when Knowledge Foundation assets become Official for platform consumers.

---

## 2. Release gates

A Foundation release MAY proceed only if:

1. Validation scripts pass (no ERROR severity)
2. Required CHANGELOG entries exist
3. Review workflow completed for touched Official candidates
4. Locked modules (`schema`, `knowledge_canon`, `rule_database`, engines, applications) were not modified unless separately authorized
5. Uncertain scholarly metadata remains marked `TODO_REVIEW` (not invented)

---

## 3. Release package (Foundation)

Typical Foundation V# package includes:

- Updated JSON catalogs and indexes
- Updated module CHANGELOGs
- Validation / Coverage / TODO_REVIEW reports
- Summary of consumer impact (ID remaps, new terms)

---

## 4. Post-release

1. Status fields updated to `official` only for approved records
2. Consumers notified of ID or catalog changes
3. Deprecated records retained per CHANGE_POLICY

---

## 5. Related detailed documents

- `policies/04_RELEASE_POLICY.md`
- `procedures/08_RELEASE_WORKFLOW.md`
