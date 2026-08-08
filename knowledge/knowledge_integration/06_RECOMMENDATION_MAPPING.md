# 06 — Recommendation Mapping

Version: 1.0  
Status: **EPIC 4 · SPRINT A**  
Date: 2026-08-08  
Primary unit: KU-RC-001 · Support: KU-UG-001 · Future: Risk / Opportunity  

---

## 1. Purpose

Map Commercial Knowledge into the **Recommendation** block using Content Quality shape:

| Part | Role |
|------|------|
| **Action** | What to do |
| **Reason** | Why (from analysis-backed CK) |
| **Benefit / next** | What improves / what to do this week |

Wave 1.1 wires **Core Recommendation + Useful God**.  
Risk / Opportunity columns are reserved for future units (not authored in Wave 1.1).

---

## 2. Unit → Recommendation map

| Source | Rec role | evidence_kind | Wave 1.1 |
|--------|----------|---------------|----------|
| KU-RC-001 Core Recommendation | **Action** + **Next step** (+ embedded reason text) | action | **Yes** |
| KU-UG-001 Useful God Core | **Reason** / priority framing | explanation | **Yes** |
| Risk units (future RK) | Caution that may force Protect/Wait posture | risk | No |
| Opportunity units (future OP) | Unlock Advance posture | strength/action | No |
| KU-WK-001 | Soft constraint (“reduce load first”) when present | weakness | Optional influence on tone via RC body already |

---

## 3. Composition priority

```
1. If useful_god absent → no CK Recommendation (fallback insufficient/baseline)
2. Select KU-UG-001 (reason)
3. Select KU-RC-001 (action) — must not emit without useful_god condition
4. Future: if Risk high → prefer Wait/Protect actions over Advance
5. Future: Opportunity required for Advance posture
```

Wave 1.1 RC `decision_posture=prepare` — safe default; do not upgrade to Advance in Adapter.

---

## 4. Recommendation block fields

| Field | Source mapping |
|-------|----------------|
| **priority** | KU-RC-001 priority (100) over others; single action unit in Wave 1.1 |
| **reason** | Prefer KU-UG-001 bound text; else reason clause inside KU-RC-001 |
| **action** | KU-RC-001 “Hành động: …” segment |
| **benefit / next** | KU-RC-001 “Bước tiếp theo: …” segment |

Adapter may pass RC as one `action` evidence unit; Composer already shapes Recommendation from action evidence.  
Optional: split RC into structured subfields in Phase B **without** changing Pack 05 section list (additive evidence metadata only).

---

## 5. Fallback

| Case | Behavior |
|------|----------|
| No useful_god | Empty Rec CK; Narrative insufficient/baseline |
| UG passes, RC bind fails | Drop both or drop RC only (prefer drop RC; keep UG for Reasoning) |
| Conflict with future Risk | Risk gate wins over Advance (N/A Wave 1.1) |
| Duplicate action texts | Dedupe keep RC |

---

## 6. Risk & Opportunity (reserved)

| Future input | Effect on Rec |
|--------------|---------------|
| Risk CK | May select Protect/Wait sibling actions; Warning pairing |
| Opportunity CK | May allow Advance posture actions |

Do not invent Risk/Opportunity text from Wave 1.1 units.

---

## 7. Traceability

Recommendation paragraphs must trace to `KU-RC-001` and, when used, `KU-UG-001`.

---

## 8. Stop line

Recommendation mapping complete. No runtime.

---

END
