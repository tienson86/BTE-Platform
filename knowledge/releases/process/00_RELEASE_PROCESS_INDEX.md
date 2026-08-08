# 00 — Release Process Index · BTE Release Management

Version: 1.1.0  
Status: **OFFICIAL — Permanent Release Process**  
Date: 2026-08-08  
Owner: BTE Product  
Scope: **Documentation only** — governs every future Commercial version  

---

## 1. Purpose

This pack is the **permanent BTE Release Management** process.

It applies to:

- Commercial V1 (currently **RC1** — Human Consulting + Product sign-off open)  
- Commercial V1.1 / V2 / later  
- Hotfixes and post-release maintenance  

It complements (does not replace):

| Pack | Role |
|------|------|
| `knowledge/product/` Capability Registry & policies | Capability as release unit |
| `knowledge/product/release_candidate/` | Human consulting validation for a given RC |
| `knowledge/releases/v1/` | V1 Architecture Freeze & Commercial V1 RC1 package (`09`–`13`) |
| `knowledge/consulting_quality/` | Consulting scorecard & acceptance minima |

---

## 2. Reading order

| Order | File | Content |
|------:|------|---------|
| 0 | `00_RELEASE_PROCESS_INDEX.md` | This index |
| 1 | `01_RELEASE_WORKFLOW.md` | Dev → RC → Review → Release → Maintenance → Next |
| 2 | `02_RELEASE_GATES.md` | Engineering → … → Product Approval |
| 3 | `03_RELEASE_CHECKLIST.md` | Pre-release checklist |
| 4 | `04_RELEASE_SIGNOFF.md` | Approval roles & decision |
| 5 | `05_POST_RELEASE_POLICY.md` | Bugfix / quality / knowledge / expansion |
| 6 | `06_HOTFIX_POLICY.md` | Severity, release, rollback |
| 7 | `07_VERSIONING_POLICY.md` | Commercial / Capability / Knowledge versions |
| 8 | `08_NEXT_RELEASE_PLANNING.md` | V1 → V1.1 → V2 planning rules |

---

## 3. Current Commercial V1 status (do not invent)

| Field | Value |
|-------|-------|
| **Status** | **Release Candidate 1** |
| **Engineering** | **PASS** |
| **Golden Cases** | **PASS** |
| **Commercial QA** | **PASS** |
| **Human Consulting Review** | **PENDING** |
| **Product Decision** | **PENDING** |
| **Commercial Version** | **RC1** |
| Career Selection Assessment | Capability Released · Frozen |
| Promotion Readiness Assessment | Capability Released · Production |
| Declared Commercial V1 Released? | **No** |
| Release package | `knowledge/releases/v1/09`–`13` |
| Archive folder | **INACTIVE** (`release_candidate/archive/`) |

**Commercial V1 is NOT Released.**

---

## 4. Core principle

```
Capability release  ≠  Commercial version release
```

A Capability may be Released on the production path while the **Commercial version** (e.g. Commercial V1) remains RC until Product Approval Gate passes.

---

## 5. Stop line

Release Management V1 published.  

| Field | Value |
|-------|-------|
| Status | Release Candidate 1 |
| Commercial Version | RC1 |
| Human Consulting Review | PENDING |
| Product Decision | PENDING |
| Commercial V1 Released? | No |

**Commercial V1 is NOT Released.**  
**Wait for Product Review.**

---

END
