# Change Policy

**Module:** `knowledge/governance`  
**Document:** CHANGE_POLICY  
**Version:** V1.0.0  
**Status:** Official Foundation  

---

## 1. Change principles

1. Minimal change — fix only what is required
2. No silent ID remapping after Official publication
3. No invented academic content — use `TODO_REVIEW`
4. Backward compatibility preferred; wrappers / deprecation over deletion
5. Locked modules remain locked unless explicitly authorized

---

## 2. Allowed Foundation changes

- Documentation
- JSON catalogs and indexes
- Validation rules and reports
- Changelogs
- Formatting normalization
- `TODO_REVIEW` markers

---

## 3. Disallowed without separate authorization

- Schema changes under `knowledge/schema/`
- Knowledge Canon content edits
- Rule Database edits
- Engine / application logic
- Invented bibliographic or doctrinal claims

---

## 4. Change request flow

```text
Propose change → Impact check → Draft update → Review → Approve → Release → Changelog
```

Breaking changes require MAJOR version and consumer migration notes.

---

## 5. Deprecation and archive

| Action | Rule |
|--------|------|
| Deprecate | Mark status; keep ID; document replacement |
| Archive | Read-only retention; no new citations |
| Delete | Forbidden for published IDs |

---

## 6. Related detailed documents

- `policies/02_CHANGE_MANAGEMENT_POLICY.md`
- `policies/05_DEPRECATION_POLICY.md`
- `policies/06_ARCHIVE_POLICY.md`
- `procedures/09_CHANGE_REQUEST_WORKFLOW.md`
