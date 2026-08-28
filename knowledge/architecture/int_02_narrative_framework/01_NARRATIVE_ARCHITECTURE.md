# 01 — Narrative Architecture

| Field | Value |
|-------|--------|
| Document | INT-02A Narrative Architecture |
| Version | 1.0.0 |
| Status | Canonical for INT-02A |

---

## 1. Purpose

INT-02 defines the **topic-level Narrative Framework**.

Every analytical topic must be able to speak in the same five blocks.

The framework is reusable. It is not a new scoring engine. It is not UI. It is not an LLM.

---

## 2. What a topic narrative is

A **Topic Narrative Unit** is the canonical customer-facing explanation of **one** analytical result, for example Strength or Useful God.

It is not the whole-chart commercial story (Pack 05 `NarrativeResult`).

It is not the Interpretation Engine execution pipeline (Pack 04).

It is the shared shape those later layers must fill.

---

## 3. Position in the platform

```
Calendar / BaZi / Strength / Pattern / Useful God /
Five Elements / Ten Gods / ShenSha / Temperature / Luck
        ↓
Engine Result (facts only, immutable)
        ↓
Narrative Framework (INT-02)     ← this epic
        ↓
Topic Narrative Unit
        ↓
Interpretation composition  /  Pack 05 Narrative  /  Identity keys  /  Report  /  Portal
```

Canonical analytical truth remains the engine result.

Canonical topic speech becomes the Topic Narrative Unit.

---

## 4. Responsibilities

The Narrative Framework owns:

- block inventory and order
- template hierarchy
- sentence ownership
- composition order
- insufficient-data policy for missing facts

The Narrative Framework does **not** own:

- calendar conversion
- chart construction
- strength / pattern / useful-god / element / ten-god / shensha / luck calculation
- identity assembly
- workspace layout
- report / PDF / DOCX rendering
- LLM rewrite

---

## 5. Dependency rules

```
Engine Result  →  Narrative Framework  →  Delivery
```

No reverse imports.

Narrative never calls an engine calculator.

Narrative never mutates an engine result.

Narrative never invents facts.

If a required fact is unpublished, the block is **insufficient**, not fabricated.

---

## 6. Analytical topics in scope

These topics must support the five-block unit:

| Topic id | Fact owner |
|----------|------------|
| `strength` | Strength engine |
| `pattern` | Pattern engine |
| `useful_god` | Useful God engine |
| `five_elements` | Five Elements result |
| `ten_gods` | Ten Gods result |
| `shensha` | ShenSha result |
| `temperature` | Temperature result |
| `luck` | Luck engine |

Calendar and BaZi remain chart identity, not topic narrative.

Score totals may appear as evidence inside a topic. Score is not a separate narrative topic in INT-02A.

Bone-weight remains optional until identity publishes it.

---

## 7. Chart-level vs topic-level

| Layer | Shape | Owner |
|-------|--------|--------|
| Topic unit | Observation → … → Conclusion | INT-02 |
| Chart narrative | Pack 05 sections / commercial summary | Pack 05 (frozen) |
| Identity keys | `observation_id`, `reasoning_id`, `recommendation_id`, `conclusion_id` | Identity (frozen) |
| Workspace Panel 9 | Quan sát / Lý do / Tác động / Khuyến nghị | Workspace (frozen) |
| Workspace Panel 10 | Kết luận | Workspace (frozen) |

INT-02A does not rewrite those consumers.

It freezes the **source shape** they should eventually read.

Workspace aliases (`observe`, `reason`, `advice`) map onto framework slots. They are not a second contract.

---

## 8. No implementation in this sprint

INT-02A publishes architecture + frozen Python contracts only.

No composer runtime.

No template authoring.

No engine wiring.

---

END
