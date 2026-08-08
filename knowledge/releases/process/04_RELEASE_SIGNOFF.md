# 04 — Release Signoff

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Use: One signoff record per Commercial version release decision  

---

## 1. Purpose

Capture required approvals before a Commercial version is declared Released.

---

## 2. Approval set

### 2.1 Engineering Approval

| Field | Value |
|-------|-------|
| Approver | |
| Date | |
| Engineering Gate | Pass ☐ · Fail ☐ |
| Golden Case Gate | Pass ☐ · Fail ☐ |
| Notes | |

Signature: ______________________

### 2.2 Knowledge Approval

| Field | Value |
|-------|-------|
| Approver | |
| Date | |
| In-scope Knowledge approved | Pass ☐ · Fail ☐ |
| Freeze / allow-list integrity | Pass ☐ · Fail ☐ |
| Notes | |

Signature: ______________________

### 2.3 Consulting Approval

| Field | Value |
|-------|-------|
| Approver | |
| Date | |
| Human Consulting Gate | Pass ☐ · Pass with minor fixes ☐ · Fail ☐ |
| Evidence (RC forms) | |
| Notes | |

Signature: ______________________

### 2.4 Product Approval

| Field | Value |
|-------|-------|
| Approver (Product Owner) | |
| Date | |
| Product Approval Gate | Pass ☐ · Fail ☐ |
| Release Checklist complete | Yes ☐ · No ☐ |
| Notes | |

Signature: ______________________

---

## 3. Release Decision

Select **one**:

| Decision | Meaning |
|----------|---------|
| ☐ **GO** | Declare Commercial version Released |
| ☐ **GO WITH MINOR FIXES** | Declare Released with owned minor list |
| ☐ **NO GO** | Remain RC / return to Development — **not Released** |

| Field | Value |
|-------|-------|
| Commercial version | |
| RC label | |
| Decision date | _pending until signed_ |
| Minor fix list (if any) | |
| Rollback plan acknowledged | Yes ☐ · No ☐ |

**Commercial version Released?** ☐ Yes · ☐ **No (default)**

---

## 4. Linkage

| Artifact | Link / path |
|----------|-------------|
| RC decision form | e.g. `knowledge/product/release_candidate/05_RC1_RELEASE_DECISION.md` |
| Product Changelog entry | `knowledge/product/06_PRODUCT_CHANGELOG.md` |
| Version release notes | |

---

## 5. Stop line

Unsigned = **not Released**.  

Commercial V1 must not be marked Released until this signoff (or equivalent RC decision) is **GO** / **GO WITH MINOR FIXES**.

---

END
