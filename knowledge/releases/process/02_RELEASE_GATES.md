# 02 — Release Gates

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  

---

## 1. Purpose

Define mandatory gates that must pass before a Commercial version may move from RC to Released.

Gates are sequential for the **Commercial version** track.  
Capability track may pass Engineering/Golden earlier; Product Approval still gates announcement.

---

## 2. Official gates

```
Engineering Gate
    ↓
Golden Case Gate
    ↓
Commercial Quality Gate
    ↓
Human Consulting Gate
    ↓
Product Approval Gate
```

---

## 3. Gate definitions

### 3.1 Engineering Gate

| Item | Requirement |
|------|-------------|
| Scope | Agreed Commercial / Capability scope implemented |
| Architecture | No unauthorized Foundation / engine boundary breaks |
| Tests | Module suites for touched areas PASS |
| Runtime freeze | No drive-by refactors outside scope |
| Owner | Engineering lead |
| Evidence | CI / local module test reports; wiring reports |

**Fail if:** Red modules in scope, or architecture freeze violated.

### 3.2 Golden Case Gate

| Item | Requirement |
|------|-------------|
| Cases | Required Golden Cases for in-scope Capabilities PASS |
| Regression | Prior Released Capabilities / Wave cores do not regress |
| Owner | Engineering + Domain |
| Evidence | Domain golden reports; `tests/<module>` |

**Fail if:** Required case FAIL, or silent Golden Dataset edits to force green.

### 3.3 Commercial Quality Gate

| Item | Requirement |
|------|-------------|
| Experience | Audit / polish blockers for this version addressed or waived |
| Actionability | Primary Rec meets What/Why/How/When/Expected outcome (when in scope) |
| Framing | Capability discoverability rules for the version met |
| Owner | Product + Engineering |
| Evidence | `commercial_v1/` polish reports or successor; QA notes |

**Fail if:** Open **P0** experience blockers without written waiver.

### 3.4 Human Consulting Gate

| Item | Requirement |
|------|-------------|
| Review | Mandatory case set reviewed with Checklist + Scoring |
| Acceptance | PASS or PASS WITH MINOR FIXES (no REJECT aggregate) |
| Blockers | Zero consulting Blockers open |
| Owner | Consulting Reviewer(s) |
| Evidence | `release_candidate/` forms `02`–`04` (or successor) |

**Fail if:** REJECT, or incomplete review set, or open Blocker.

### 3.5 Product Approval Gate

| Item | Requirement |
|------|-------------|
| Decision | GO or GO WITH MINOR FIXES recorded |
| Checklist | Release Checklist complete |
| Signoff | Engineering + Knowledge + Consulting + Product as required |
| Owner | Product Owner |
| Evidence | `04_RELEASE_SIGNOFF.md` + RC decision form |

**Fail if:** NO GO, or unsigned Product decision.

---

## 4. Gate matrix (who can waive)

| Gate | Waiver allowed? | By whom |
|------|:---------------:|---------|
| Engineering | Rare | Product + Engineering (written) |
| Golden Case | No for required set | — |
| Commercial Quality | P0 only with written risk | Product Owner |
| Human Consulting | No for Blockers | — |
| Product Approval | N/A (is the decision) | Product Owner |

---

## 5. Relationship to Capability gates

Capability Acceptance Standard (`knowledge/product/04`) and Capability Release Policy remain required for **each Capability**.

Commercial version gates **aggregate** capability readiness + experience + human review + Product decision.

---

## 6. Commercial V1 RC1

| Field | Value |
|-------|-------|
| Status | Release Candidate 1 |
| Engineering | PASS |
| Golden Cases | PASS |
| Commercial QA | PASS |
| Human Consulting Review | PENDING |
| Product Decision | PENDING |
| Commercial Version | RC1 |
| Declared Released? | No |

---

## 7. Stop line

No Commercial version announcement without all five gates satisfied (or Product-documented waiver where allowed).

---

END
