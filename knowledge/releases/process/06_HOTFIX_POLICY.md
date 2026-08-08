# 06 — Hotfix Policy

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  

---

## 1. Purpose

Define when and how emergency fixes ship outside the normal RC cycle.

---

## 2. Severity levels

| Severity | Definition | Examples |
|----------|------------|----------|
| **Critical** | Customer harm, ethics breach, data loss, total Result failure | Wrong person data; medical/financial overclaim live; Result crash for all |
| **High** | Major consulting meaning wrong for many customers | Primary Rec systematically wrong Capability; technical leak in Exec for all cases |
| **Medium** | Meaningful defect, workaround exists | Secondary milestone missing label; density regression on one profile |
| **Low** | Cosmetic / minor copy | Typos; non-blocking polish |

---

## 3. Hotfix eligibility

| Severity | Hotfix eligible? | Notes |
|----------|:------------------:|-------|
| Critical | **Yes** | Immediate |
| High | **Yes** | Fast-track |
| Medium | Rare | Prefer normal patch train |
| Low | **No** | Next planned patch |

Hotfix must **not** introduce new Capabilities or Foundation redesign.

---

## 4. Hotfix release criteria

1. Severity Critical or High (or Product-approved Medium).  
2. Minimal diff; root-cause fix preferred over symptom hide.  
3. Targeted regression PASS (affected modules + prior Released Capabilities smoke).  
4. Engineering Approval recorded.  
5. Product Approval for customer-facing meaning changes.  
6. Consulting spot-check if Exec / Rec / Capability framing changes.  
7. Changelog entry with severity + rollback note.  
8. Version bump per Versioning Policy (usually Patch).

---

## 5. Rollback criteria

Rollback (or disable feature/allow-list gate) when:

- Hotfix introduces new Critical/High regression  
- Consulting Blocker reappears  
- Traceability / ethics regression  
- Fix cannot be verified within agreed time box  

Rollback preference order:

1. Capability-scoped disable / allow-list gate  
2. Revert hotfix commit/train  
3. Full Commercial version rollback (last resort; Product only)

---

## 6. Communication

| Audience | When |
|----------|------|
| Product | Before ship for High+; immediately for Critical |
| Consulting | If customer-facing advice changes |
| Customers | Per Product incident policy (out of scope here) |

---

## 7. Stop line

Hotfix is for safety and severe correctness — not a shortcut for roadmap features.

---

END
