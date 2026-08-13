# ARCHITECTURE

| Field | Value |
|-------|-------|
| Package | Commercial Theme Library V1.0 |
| Status | **FROZEN (catalog)** |

---

## 1. Position

```
Engines
  → Domain composers
    → Cross-Domain Reasoning   ← owns theme IDs and claim plans
      → Commercial Theme Library  ← YOU ARE HERE (content)
        → Commercial Language Layer  ← owns paragraph craft
          → Product Context (audience)
            → Customer Mode
```

Higher layers win on **truth**.  
This library wins on **which consulting class and which blocks to fill**.  
CLL wins on **sentence craft**.

---

## 2. What this is

A **content system**: reusable stances, memory lines, and action lines keyed by commercial theme.

Writers look up:

1. Theme (Layer 1)  
2. Block (Layer 2)  
3. Variant (Layer 3)  
4. Then apply CLL rules to the claim-plan slots.

---

## 3. What this is not

| Not | Owner instead |
|-----|----------------|
| Engine | Calendar / Bazi / Score / Pattern |
| Knowledge rule | Rule Database / Knowledge packs |
| Reasoning / theme derivation | CDR `theme_engine` |
| Paragraph grammar | CLL V1.2 |
| Audience / child-parent | Product Context |
| Recruitment persona | RC3 `CUSTOMER_PERSONAS` |

Personas remain review lenses. They do not select this library at runtime.

---

## 4. Binding (read-only)

A library theme is **selected from published CDR signals**. It is never invented.

| Library theme | Typical published signals (examples, not rules) |
|---------------|--------------------------------------------------|
| OPERATING_SELF_CARRY | `primary_theme = OPERATING_SELF_CARRY` |
| OPERATING_OUTPUT | `primary_theme = OPERATING_OUTPUT` |
| OPERATING_STANDARDS | `primary_theme = OPERATING_STANDARDS` |
| BALANCE_DIRECTION | `primary_theme = BALANCE_DIRECTION` |
| FOLLOW_FRAME | `FOLLOW_STRUCTURE` active |
| CONSERVING | `CAPACITY_WEAK` or thin-leaning capacity + cooling |
| TENSION_HOLDER | Two published layers both true (capacity vs structure, or two operating themes) |
| STABILIZER | Standards or balance as *hold-the-frame*, not as grind |

If signals do not support a theme, **do not apply it**.

---

## 5. Overlay, not replacement

Operating theme (how they work) and overlay (how to speak when a second truth is live) may combine:

```
OPERATING_OUTPUT + FOLLOW_FRAME     → non-ordinary output (P02/P05 class)
OPERATING_SELF_CARRY + CONSERVING   → do not use empowerment close
BALANCE_DIRECTION + CONSERVING      → rest is the product
OPERATING_* + TENSION_HOLDER        → keep both stories in Memory
```

Overlays never delete the operating theme. They gate Memory and Action.

---

## 6. Data flow (conceptual)

```
Claim plan.primary_theme
Claim plan.identity_core (capacity / structure fragments)
        ↓  select 1 operating + 0–2 overlays
Library theme id(s)
        ↓  fill
9 blocks × 1 writing variant
        ↓  CLL
Customer paragraphs
```

This package does not implement the selector. V1.0 is the catalog only.

---

END
