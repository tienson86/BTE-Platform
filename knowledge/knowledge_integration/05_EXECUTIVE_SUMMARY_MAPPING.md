# 05 — Executive Summary Mapping

Version: 1.0  
Status: **EPIC 4 · SPRINT A**  
Date: 2026-08-08  
Wave 1.1 units: KU-ID-001 · KU-ST-001 · KU-WK-001 · KU-UG-001 (+ RC for priority/next)  

---

## 1. Purpose

Map Golden Baseline units into **Executive Summary** slots without redesigning Exec grammar.

Commercial reading targets (Content Quality):

1. Who is this person? → identity  
2. Core strengths → strength  
3. Core weaknesses → weakness  
4. Opportunities (derived) → strength + UG when present  
5. Risks (derived) → weakness when present  
6. Immediate priority → action (RC)  
7. Next action → action (RC)  

---

## 2. Unit → Exec section map

| KU | Exec role | evidence_kind | Composition priority |
|----|-----------|---------------|---------------------:|
| KU-ID-001 Identity Core | Who / identity line | identity | **1 (required for Exec commercial spine)** |
| KU-ST-001 Strength Core | Strengths | strength | **2 (conditional)** |
| KU-WK-001 Weakness Core | Weaknesses / risk reading | weakness | **3 (conditional)** |
| KU-UG-001 Useful God Core | Priority framing / opportunity reading support | explanation | **4 (conditional)** |
| KU-RC-001 Core Recommendation | Priority + next action lines | action | **5 (conditional on useful_god)** |

---

## 3. Composition order (Adapter → Exec fill)

```
1. Bind & attach KU-ID-001 (if condition pass)
2. Attach KU-ST-001 if favorable strength
3. Attach KU-WK-001 if weakness/caution signals
4. Attach KU-UG-001 if useful_god present
5. Attach KU-RC-001 if useful_god present (shared with Rec)
```

Composer uses existing Exec assembly; Adapter only supplies ordered evidence units tagged `executive_summary`.

---

## 4. Priority rules

| Rule | Detail |
|------|--------|
| Identity first | Without identity, Exec commercial quality fails → prefer insufficient identity over skipping silently |
| ST XOR typical WK bands | Conditions usually exclusive; both allowed if signals support |
| UG before RC in Exec prose | Explanation frames why priority exists; RC states what to do |
| Cap | Max one unit per evidence_kind for Exec in Wave 1.1 |

---

## 5. Fallback

| Missing | Exec behavior |
|---------|---------------|
| No ID | Insufficient identity slot / partial |
| No ST | Omit strengths commercial line (do not invent) |
| No WK | Omit weaknesses line |
| No UG | Omit useful-god framing; RC also absent |
| No RC | Omit priority/next commercial lines |
| Empty CK | Baseline Exec (pre-integration honesty) |

---

## 6. Example composition (logical, not runtime)

When day master, pattern, strength band, useful god present and strength favorable:

| Slot | Source unit |
|------|-------------|
| Identity | KU-ID-001 bound |
| Strengths | KU-ST-001 bound |
| Weaknesses | (none if not triggered) |
| Priority / next | KU-RC-001 bound; reason echoed from KU-UG-001 |

---

## 7. Traceability

Each Exec paragraph from CK must cite `knowledge_unit_id` + version in Narrative trace refs.

---

## 8. Stop line

Executive Summary mapping complete. No runtime.

---

END
