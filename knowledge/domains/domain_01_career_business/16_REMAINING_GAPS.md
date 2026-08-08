# 16 — Remaining Gaps · Domain 01 P0

Version: 1.0  
Status: **DOMAIN 01 · SPRINT B — post-authoring gaps**  
Date: 2026-08-08  
Depends on: `14`, `15`, Capability Roadmap `13`  

---

## 1. Purpose

Record what remains after P0 Knowledge authoring — before Product authorizes wiring or P1.

---

## 2. Closed by Sprint B

| Item | Status |
|------|--------|
| P0 matrix units authored (4) | **Done** |
| Domain CSV `22_*.csv` created | **Done** |
| Wave 1.1 left frozen | **Done** |
| Offline Golden Case lift demonstrated | **Done** |

---

## 3. Remaining gaps

### 3.1 Production wiring (blocked by Sprint B rules)

| Gap | Impact | Owner |
|-----|--------|-------|
| Adapter loads only `21_knowledge_units.csv` | Domain 01 invisible in default pipeline | Engineering (allow multi-CSV) |
| Allow-list is Wave 1.1-only | Domain ids never selected | Engineering + Product policy |
| Bundle buckets ignore `career_direction` / `leadership_style` / `business_posture` | Typed fields incomplete; sections still carry text | Optional Adapter enhancement |
| One `action` evidence_kind dedupe | Career AC displaces KU-RC when both eligible (intended for career) | Document; revisit multi-action later |

### 3.2 Knowledge coverage (intentional — not P0)

| Gap | Phase |
|-----|-------|
| Career change Go/stage + RK/MT | P1 |
| Promotion readiness OP pack | P1 |
| Manager vs IC deep | P1 |
| Partnership RK/MT deep | P1 |
| Startup launch/pilot/defer deep | P1 |
| Team management | P2 |
| Industry theme packs | P1 |

### 3.3 Narrative / composition (pre-existing)

| Gap | Notes |
|-----|-------|
| Summary identity↔strength merge / weakness double-print | EPIC 7 remaining — not Domain content |
| Pack 05 empty section bodies | P1 Narrative polish |

### 3.4 Capability / API

| Gap | Notes |
|-----|-------|
| Capability HTTP API | Design only (`12`) |
| Maturity still L1 in production until wiring + cases signed | Target L2–L3 after activation |

---

## 4. Recommended Product next steps

1. Review P0 unit prose (`22_domain01_career_business.csv`)  
2. Authorize **production wiring sprint** (loader + allow-list) — still no P1 units required  
3. Re-run D1 Golden Cases on live pipeline  
4. Only then open P1 authoring  

---

## 5. Success statement (content)

Domain 01 is the **first authored commercial domain corpus** beyond Wave 1.1.  
It becomes a **production commercial domain** after Product approves wiring + live validation.

---

## 6. Stop line

**No P1/P2 authoring. No runtime in this sprint. Wait for Product Review.**

---

END
