# 08 — Cross-Domain Dependencies · Career & Business

Version: 1.0  
Status: **OFFICIAL — Domain 01 Cross-Domain Dependencies**  
Date: 2026-08-08  
Depends on: Wave 1.1 freeze · Knowledge Model domains · `01`–`07`  
Scope: Documentation only  

---

## 1. Purpose

State what Domain 01 **depends on**, what it **provides to** other domains, and what it must **not** duplicate or break.

---

## 2. Hard dependencies (must exist)

| Dependency | Status | Domain 01 need |
|------------|--------|----------------|
| Wave 1.1 KU-ID/ST/WK/UG/RC | **Frozen / published** | Structural spine; mitigate-first; useful-god compass |
| Commercial Knowledge Adapter | Complete | Retrieval + bundle; scenario allow-list later |
| Narrative Pack 05 grammar | Frozen | Delivery surfaces |
| EPIC 5 Consulting Quality | Approved | Acceptance scoring |
| EPIC 6 Golden Case workflow | Approved | Validation method |

**Rule:** Domain 01 population must not modify Wave 1.1 content.

---

## 3. Soft dependencies (enrich when present)

| Domain / system | Relationship |
|-----------------|--------------|
| **CK-LU (Luck)** | Promotion / founder timing windows (P1/P2 OP units) |
| **CK-ED (Education)** | Professional development skill bets |
| **CK-FI (Finance)** | Business money posture — **hand-off**, do not absorb full FI |
| **CK-PG (Personal Growth)** | Long-horizon capability narrative |
| **CK-DM (Decision Making)** | Shared postures prepare/advance/defer |
| **CK-PE (Personality)** | Optional color for leadership style — not required for P0 |

---

## 4. Provides to other domains

| Consumer | What Domain 01 offers |
|----------|----------------------|
| Default Result (if enabled) | Light career line beyond pure structure |
| CS-MD major decisions | Work-context actions when decision is job/business |
| Future Finance domain | Employment vs enterprise context without owning FI rules |
| Portal scenarios | CS-CA / CS-BU / … routing targets |

---

## 5. Conflict & priority rules

| Conflict | Resolution |
|----------|------------|
| Domain Advance vs Wave 1.1 WK | **WK / mitigate-first wins** |
| Career CN vs Finance CN on same money-work ask | Prefer explicit scenario; else Career for role, Finance for money mechanics |
| Leadership vs Management units both fire | Management answers IC vs manager; Leadership answers authority strain — both allowed if non-duplicative |
| Domain Rec vs KU-RC-001 | Domain specializes; do not emit contradictory Dụng thần direction |

---

## 6. Scenario activation dependency

| Policy option | Effect |
|---------------|--------|
| **A — CS-CA/CS-BU only** | Domain units only when scenario set |
| **B — default + light** | P0 career units also on default Result |

Product must choose before population. Architecture supports both; Wave 1.1 `default` affinity remains for core units.

---

## 7. What Domain 01 must not do

| Forbidden | Reason |
|-----------|--------|
| Edit Wave 1.1 rows | Frozen |
| Create FI/MA/HE units under Domain 01 ids | Wrong domain ownership |
| Bypass Adapter / expose raw Rule DB | Architecture |
| Require Narrative redesign | Frozen |
| Depend on unpublished Wave 1.2 structural units | Not needed |

---

## 8. Dependency diagram

```
CK-ID / Wave 1.1 cores (frozen)
        ↓
DOMAIN-01 Career & Business (CK-CA + CK-BU + CK-LE)
        ↕ soft
CK-LU · CK-ED · CK-DM · (CK-FI hand-off)
        ↓
NarrativeResult → Portal
```

---

## 9. Stop line

Cross-domain dependencies defined.  

**Domain 01 Sprint A complete. Wait for Product review before authoring any Career/Business Knowledge Units.**

---

END
