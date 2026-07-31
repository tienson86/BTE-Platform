# Compilation Report Template

**Document:** COMPILATION_REPORT_TEMPLATE  
**Module:** `knowledge/tools/record_builder`  
**Version:** V1.0.0  

Copy per compilation attempt.

---

## 1. Header

| Field | Value |
|-------|-------|
| Report ID | |
| Planning ID | |
| Knowledge ID | |
| Pack | |
| Owner module | |
| Operator | |
| Started at | |
| Finished at | |
| Overall result | PASS / FAIL / BLOCKED |

---

## 2. Inputs

| Input | Path / ID | Verified |
|-------|-----------|----------|
| Design artifact | | |
| Mapping sheet | | |
| Base schema | `knowledge/schema/knowledge_record.schema.json` | |
| Module overlay | | |
| Foundation references | `knowledge/references/references.json` | |

---

## 3. Gate results

| Gate | Result | Errors | Warnings |
|------|--------|--------|----------|
| Input verification | | | |
| Field mapping | | | |
| Schema validation | | | |
| Reference validation | | | |
| Relationship validation | | | |
| Integrity validation | | | |
| Output validation | | | |

---

## 4. Validation object written

| Flag | Value |
|------|-------|
| `schema_valid` | |
| `reference_valid` | |
| `relationship_valid` | |
| `integrity_valid` | |

---

## 5. Output

| Field | Value |
|-------|-------|
| Draft JSON path | |
| Official JSON path | |
| Written to disk | Yes / No |
| Authorization ticket | |

---

## 6. Issues

| Severity | Code | Message |
|----------|------|---------|
| | | |

---

## 7. Decision

- [ ] Blocked — fix and retry  
- [ ] Draft only  
- [ ] Approved for Official write  
- [ ] Requires Academic re-review  

---

## 8. Sign-off

| Role | Signature | Date |
|------|-----------|------|
| Operator | | |
| Technical Review | | |
| Academic Review | | |
