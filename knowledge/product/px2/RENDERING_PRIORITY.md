# Rendering Priority

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2

---

## 1. Bind / render order

Matches PX-1 reading order — **not** layout `CANONICAL_MODULE_ORDER`.

```
1  ResultPage chrome + skip link
2  Hero
3  ExecutiveSummary
4  Recommendation + CTA
5  ImportantWarnings          (if visible)
6  DomainCareer
7  DomainWealth
8  DomainRelationship
9  DomainHealth
10 DomainLuck
11 Charts                     (if visible)
12 TechnicalInfo              (collapsed)
13 Knowledge                  (collapsed / if visible)
14 Appendix                   (if visible)
15 Footer
```

---

## 2. Why not layout module order

RE-2 module order is cover → overview → chart → analysis → decision → luck → interpretation → appendix → summary.

That order is a **document assembly** sequence.  
V2 consultation sequence is advice-first (PX-1).

Adapter may read layout in module order internally.  
It **emits** UI in rendering priority above.

---

## 3. Progressive bind

On `loading`: render page skeleton / status only — no fake Hero name.

On `partial_ready`: render all ready P1/P2 units; skip hidden P3/P4.

On `error`: page error card; do not render a false consultation.

---

## 4. Visual vs bind priority

Visual hierarchy (PX-1 H0–H4) applies after bind.  
Rendering priority is sequence, not type size.

---

## 5. Stop line

Users read PX-1 order. Layout internals stay invisible.

END
