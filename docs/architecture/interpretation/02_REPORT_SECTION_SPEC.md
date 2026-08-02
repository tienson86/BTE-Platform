# 02 — Report Section Specification

| Field | Value |
|-------|--------|
| **Title** | BTE Interpretation System — Report Section Specification |
| **Document ID** | `ARCH-INT-02` |
| **Version** | `1.0.0` |
| **Status** | **Frozen / Normative** |
| **Owner** | Architecture (Interpretation System) |
| **Effective** | 2026-08-02 |

---

## Purpose

This document is the **authoritative catalogue of report sections** for BTE Interpretation System V1.0.

For every section it defines:

- Why the section exists
- What information it owns and cannot own
- Required and optional inputs
- Dependencies, priority, visibility
- Display recommendations (presentation-agnostic)
- Validation rules
- Output examples (illustrative, not golden snapshots)

Implementers MUST treat section IDs as stable public contracts.

---

## Scope

### In scope

- Normative section definitions listed below
- Shared section metadata schema
- Validation and visibility rules

### Out of scope

- CSS / UI component implementation
- Exact JSON field names of a particular API build (map during implementation; do not invent facts)
- Sentence ranking internals ([05](05_SENTENCE_PRIORITY.md))
- Full narrative style ([03](03_NARRATIVE_GUIDE.md))

---

## Audience

Engineers implementing Interpretation / Report pipelines; product managers defining SKUs contents; domain reviewers; AI implementers.

---

## Definitions

| Term | Meaning |
|------|---------|
| **Section** | Stable interpretive unit with `section_id` |
| **Required input** | Without it, section cannot produce substantive content |
| **Optional input** | Enriches depth; absence does not force Unavailable if required inputs exist |
| **Priority** | Ordering weight for assembly and conflict resolution (lower number = earlier / higher precedence in V1.0) |
| **Visibility** | `always` \| `when_data` \| `sku_gated` \| `expert_only` |
| **Unavailable** | Explicit empty outcome with reason — still a valid section result |

Shared vocabulary: [GLOSSARY.md](GLOSSARY.md). Completeness: [01_INTERPRETATION_STANDARD.md](01_INTERPRETATION_STANDARD.md).

---

## Architecture Notes

### Shared section metadata schema (conceptual)

Every section result SHOULD expose:

| Field | Description |
|-------|-------------|
| `section_id` | Stable id |
| `title` | Localized display title |
| `status` | `ok` \| `partial` \| `unavailable` \| `error` |
| `priority` | Integer per this spec |
| `confidence` | Optional 0–1 or enum from upstream |
| `inputs_used` | Trace of which inputs were bound |
| `body` | Structured blocks and/or narrative paragraphs |
| `warnings` | Non-fatal policy notes |
| `reason_codes` | Machine-readable gaps |

### Global validation rules

1. Unknown `section_id` MUST NOT be silently treated as mandatory.
2. Section MUST NOT emit medical/legal/guaranteed-finance claims ([03](03_NARRATIVE_GUIDE.md)).
3. Section MUST use terminology from [06](06_TERMINOLOGY_STYLE_GUIDE.md).
4. Section MUST NOT contradict higher-priority resolved sections without conflict resolution ([05](05_SENTENCE_PRIORITY.md)).

### Priority band (V1.0)

| Band | Priority range | Sections |
|------|----------------|----------|
| Framing | 10–19 | Overview |
| Structural core | 20–49 | Body Strength, Five Elements, Ten Gods, Pattern |
| Gods | 50–69 | Useful, Helpful, Unfavorable |
| Dynamics | 70–79 | Luck |
| Closure | 80–89 | Recommendations, Summary |
| Annex | 90–99 | Appendix |

---

## Section catalogue

---

### 1. Overview

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `overview` |
| **Purpose** | Establish reading identity, scope, and orientation. |
| **Description** | Opens the report: who/what is being read (within privacy rules), chart framing, and what the reader will learn. Does not deep-dive gods or luck. |
| **Why it exists** | Without orientation, later sections feel disconnected. |
| **Owns** | Scope statement, high-level chart identity cues, reading disclaimers alignment |
| **Must not own** | Strength verdict detail, pattern name as sole content, decade luck lists |
| **Required Inputs** | Minimal chart identity (e.g., day master or pillars summary available upstream) |
| **Optional Inputs** | Customer display name, gender presentation, timezone label, overall confidence |
| **Dependencies** | None (root framing) |
| **Priority** | `10` |
| **Visibility** | `always` |
| **Display Recommendation** | Short hero block; 1–3 paragraphs; no dense tables |
| **Future Extension** | Multi-profile comparison intro |
| **Validation Rules** | Must not assert Complete if mandatory downstream sections are globally skipped without Partial flag; must not use forbidden tone |
| **Output Example** | “This reading explains the Four Pillars structure and how elemental balance, pattern, and useful-god guidance interact. Conclusions are interpretive, not absolute predictions.” |

---

### 2. Body Strength

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `body_strength` |
| **Purpose** | Explain Day Master relative strength (thân vượng / thân nhuợc / balanced bands as provided). |
| **Description** | Translates strength analysis into educational narrative. |
| **Why it exists** | Strength is a primary BaZi hinge for pattern and useful-god logic. |
| **Owns** | Strength level explanation and implications *for reading method* |
| **Must not own** | Pattern renaming; Useful God selection; health diagnosis |
| **Required Inputs** | Strength label/level (or equivalent enum) from analysis |
| **Optional Inputs** | Supporting scores, season context, brief rationale codes |
| **Dependencies** | Conceptually after `overview`; feeds `pattern`, god sections |
| **Priority** | `20` |
| **Visibility** | `always` (Unavailable if input missing) |
| **Display Recommendation** | Status badge + 1 explanatory card; avoid alarmist colors implying doom |
| **Future Extension** | Multi-method strength comparison (explicitly labeled) |
| **Validation Rules** | If strength missing → `unavailable`; prose must match input label; no “disaster” wording |
| **Output Example** | “Day Master strength is assessed as relatively strong in this chart. Supportive resources appear available; useful-god guidance should be read in that context.” |

---

### 3. Five Elements

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `five_elements` |
| **Purpose** | Explain ngũ hành distribution and balance narrative. |
| **Description** | Describes elemental presence/emphasis and educational implications. |
| **Why it exists** | Element balance is a core explanatory layer between pillars and gods. |
| **Owns** | Element distribution explanation |
| **Must not own** | Final career guarantee; redefining strength without strength section |
| **Required Inputs** | Element counts/weights or equivalent distribution structure |
| **Optional Inputs** | Score-linked element metrics, season tags |
| **Dependencies** | Benefits from `body_strength`; supports `ten_gods`, `pattern` |
| **Priority** | `30` |
| **Visibility** | `always` / Unavailable if no distribution |
| **Display Recommendation** | Bars or compact distribution + short prose; not a rainbow dashboard of unrelated KPIs |
| **Future Extension** | Interactive element drill-down in Expert Mode |
| **Validation Rules** | Must not invent missing element; percentages if shown must sum/consistently derive from inputs |
| **Output Example** | “Metal and Water appear more prominent, while Fire is comparatively limited. Guidance later in this report should be read against that imbalance.” |

---

### 4. Ten Gods

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `ten_gods` |
| **Purpose** | Explain Thập thần configuration relevant to the chart. |
| **Description** | Maps present ten gods to educational meanings without moral condemnation. |
| **Why it exists** | Ten gods connect structure to life-domain tendencies. |
| **Owns** | Ten-god presence/emphasis narrative |
| **Must not own** | Absolute personality labels; medical claims |
| **Required Inputs** | Ten-god assignments or catalogue of present gods |
| **Optional Inputs** | Strength per god, pillar-linked gods |
| **Dependencies** | After pillars/elements context; before or alongside `pattern` as data allows |
| **Priority** | `40` |
| **Visibility** | `always` / Unavailable if absent |
| **Display Recommendation** | Checklist or chips of present gods + prose; collapse long catalogues |
| **Future Extension** | Per-domain ten-god deep dives (career/wealth) as optional child sections |
| **Validation Rules** | Only gods present in input may be asserted as present; unknown → do not mark present |
| **Output Example** | “Direct Resource and Peer influences are visible in the structure. Their interaction should be interpreted with pattern and useful-god sections.” |

---

### 5. Pattern

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `pattern` |
| **Purpose** | Explain Cách cục / chart structure classification. |
| **Description** | States pattern result and educational meaning. |
| **Why it exists** | Pattern organizes how useful/helpful/unfavorable gods are applied. |
| **Owns** | Pattern identity and structural narrative |
| **Must not own** | Inventing pattern when engine returns none; overriding strength silently |
| **Required Inputs** | Pattern label/id or structured pattern result |
| **Optional Inputs** | Pattern confidence, alternate candidates (if engine exposes) |
| **Dependencies** | `body_strength`, preferably `five_elements` / `ten_gods` |
| **Priority** | `45` |
| **Visibility** | `always` / Unavailable if missing |
| **Display Recommendation** | Named pattern card + short method note; alternatives only if in payload |
| **Future Extension** | Pattern family taxonomy pages |
| **Validation Rules** | No silent fallback to a popular pattern name; conflict with strength requires priority resolution note |
| **Output Example** | “The chart is read under a Resource-oriented structure. Useful-god recommendations follow from this classification.” |

---

### 6. Useful God

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `useful_god` |
| **Purpose** | Explain Dụng thần (primary useful god/element direction). |
| **Description** | Core guidance axis of classical reading. |
| **Why it exists** | Customers and experts expect explicit useful-god clarity. |
| **Owns** | Primary useful-god explanation |
| **Must not own** | Guaranteed outcomes; redefining pattern |
| **Required Inputs** | Useful god / element / structured useful-god result |
| **Optional Inputs** | Rationale codes, confidence, linked evidence ids |
| **Dependencies** | `pattern`, `body_strength` |
| **Priority** | `50` |
| **Visibility** | `always` / Unavailable if missing |
| **Display Recommendation** | Prominent but calm callout; pair with Helpful/Unfavorable |
| **Future Extension** | Multi-useful-god debate mode (Expert) |
| **Validation Rules** | Must match upstream useful-god field; narrative depth per [04](04_EXPLANATION_POLICY.md) |
| **Output Example** | “Useful God guidance emphasizes Water. Environments and timing that reinforce this direction are generally more supportive in classical reading.” |

---

### 7. Helpful God

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `helpful_god` |
| **Purpose** | Explain Hỷ thần / supportive gods or elements. |
| **Description** | Secondary supportive direction that cooperates with Useful God. |
| **Why it exists** | Prevents oversimplification to a single element slogan. |
| **Owns** | Helpful/supportive direction narrative |
| **Must not own** | Contradicting Useful God without conflict note |
| **Required Inputs** | Helpful god/element field(s) when product claims this section |
| **Optional Inputs** | Relative weight vs Useful God |
| **Dependencies** | `useful_god`, `pattern` |
| **Priority** | `55` |
| **Visibility** | `when_data` (if SKU includes section but data missing → Unavailable) |
| **Display Recommendation** | Secondary card beside Useful God |
| **Future Extension** | Seasonal helpful modulation |
| **Validation Rules** | If absent, do not invent; if conflicts with Useful God, apply [05](05_SENTENCE_PRIORITY.md) |
| **Output Example** | “Wood is treated as supportive alongside the primary useful direction, reinforcing growth-oriented contexts.” |

---

### 8. Unfavorable God

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `unfavorable_god` |
| **Purpose** | Explain Kỵ / unfavorable directions with responsible caution. |
| **Description** | Names caution zones without fear or curse framing. |
| **Why it exists** | Balanced reading requires risk communication, not only positives. |
| **Owns** | Caution-oriented guidance |
| **Must not own** | Fear, fatalism, “disaster,” moral blame |
| **Required Inputs** | Unfavorable god/element when section is claimed |
| **Optional Inputs** | Mitigation notes from rules |
| **Dependencies** | `useful_god`, `pattern` |
| **Priority** | `60` |
| **Visibility** | `when_data` |
| **Display Recommendation** | Neutral warning badge (info/warn), never alarm-red doom UI copy |
| **Future Extension** | Mitigation playbooks per domain |
| **Validation Rules** | Must pass [03](03_NARRATIVE_GUIDE.md) risk-communication rules; terminology from [06](06_TERMINOLOGY_STYLE_GUIDE.md) |
| **Output Example** | “Fire-heavy contexts may require additional caution in this chart’s framework. This is a tendency note, not a prediction of harm.” |

---

### 9. Luck

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `luck` |
| **Purpose** | Explain available luck-cycle framing (Đại vận / related) without fabrication. |
| **Description** | Dynamic layer over static chart structure. |
| **Why it exists** | Timing is expected in commercial BaZi; honesty about missing data is mandatory. |
| **Owns** | Luck narrative grounded in payload |
| **Must not own** | Invented decade stems/branches; guaranteed windfalls |
| **Required Inputs** | At least one luck structure field OR explicit empty → Unavailable |
| **Optional Inputs** | Current luck pointer, annual overlays |
| **Dependencies** | Structural sections SHOULD be resolved first |
| **Priority** | `70` |
| **Visibility** | `when_data` |
| **Display Recommendation** | Timeline if data exists; otherwise professional Unavailable card |
| **Future Extension** | Lưu niên / nguyệt / nhật / thời sub-sections |
| **Validation Rules** | No fabricated years; Partial allowed if only coarse luck text exists |
| **Output Example** | “Luck-cycle data in this result highlights a supportive phase relative to the useful-god direction. Exact decade tables appear only when provided by analysis.” |

---

### 10. Recommendations

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `recommendations` |
| **Purpose** | Provide practical, non-absolute guidance synthesized from prior sections. |
| **Description** | Actionable orientation: environments, focus areas, caution areas. |
| **Why it exists** | Converts analysis into usable customer value without becoming fortune-telling guarantees. |
| **Owns** | Recommendation list/paragraphs |
| **Must not own** | New facts; medical/legal/financial guarantees |
| **Required Inputs** | At least one resolved upstream section (prefer useful_god + body_strength) |
| **Optional Inputs** | Score strengths/weaknesses lists if present |
| **Dependencies** | All prior mandatory sections ideally; MUST NOT contradict them |
| **Priority** | `80` |
| **Visibility** | `always` (may be thin if many Unavailables) |
| **Display Recommendation** | Bulleted guidance cards; max density per [04](04_EXPLANATION_POLICY.md) |
| **Future Extension** | SKU-specific recommendation packs |
| **Validation Rules** | Every recommendation MUST map to an earlier section or explicit input; forbidden expressions banned |
| **Output Example** | “Favor environments aligned with the useful-god direction; treat unfavorable-element overload as a caution signal, not a fixed outcome.” |

---

### 11. Summary

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `summary` |
| **Purpose** | Close the reading with a coherent synthesis. |
| **Description** | Short executive closing; no new facts. |
| **Why it exists** | Readers need a landing conclusion after long reports. |
| **Owns** | Synthesis only |
| **Must not own** | New gods, new strength, new luck years |
| **Required Inputs** | Outputs of previously resolved sections |
| **Optional Inputs** | Overall confidence |
| **Dependencies** | All included sections |
| **Priority** | `85` |
| **Visibility** | `always` |
| **Display Recommendation** | 1 short section at end; optionally mirrored as executive blurb at top *only if identical facts* |
| **Future Extension** | Multi-language summary packs |
| **Validation Rules** | Fact-check against section statuses; if most Unavailable → Summary must say Partial |
| **Output Example** | “Overall, the chart’s structural reading emphasizes a strong Day Master with Water as useful direction. Recommendations stay within that framework; timing details depend on available luck data.” |

---

### 12. Appendix

| Attribute | Specification |
|-----------|---------------|
| **section_id** | `appendix` |
| **Purpose** | Hold references, method notes, and advanced annex material. |
| **Description** | Non-essential for casual readers; valuable for experts. |
| **Why it exists** | Keeps core narrative clean while preserving auditability. |
| **Owns** | Citations, method notes, term clarifications |
| **Must not own** | Primary conclusions that belong in Summary |
| **Required Inputs** | None for Complete gate (optional section) |
| **Optional Inputs** | Classical citations, rule ids (prefer internal), request metadata |
| **Dependencies** | None hard |
| **Priority** | `90` |
| **Visibility** | `expert_only` or `sku_gated` |
| **Display Recommendation** | Collapsed by default in consumer UI |
| **Future Extension** | Visible bibliography toggle (Knowledge Expert alignment) |
| **Validation Rules** | Must not leak internal-only rule ids to consumer tiers unless product allows |
| **Output Example** | “Method note: Useful-god narrative is bound to analysis outputs; classical references are listed when citation mode is enabled.” |

---

## Cross-section matrix (quick)

| Section | Priority | Mandatory V1.0 | Visibility |
|---------|----------|----------------|------------|
| overview | 10 | Yes | always |
| body_strength | 20 | Yes | always |
| five_elements | 30 | Yes | always |
| ten_gods | 40 | Yes | always |
| pattern | 45 | Yes | always |
| useful_god | 50 | Yes | always |
| helpful_god | 55 | Yes | when_data |
| unfavorable_god | 60 | Yes | when_data |
| luck | 70 | Yes | when_data |
| recommendations | 80 | Yes | always |
| summary | 85 | Yes | always |
| appendix | 90 | No | expert/sku |

Note: `helpful_god`, `unfavorable_god`, and `luck` are **mandatory section slots** in the product standard, but may legitimately resolve as `unavailable` when inputs are absent. That is different from omitting the section silently.

---

## Examples

### Valid Partial report

`useful_god` = ok, `luck` = unavailable (reason: `LUCK_PAYLOAD_ABSENT`), `summary` acknowledges missing luck.

### Invalid report

`recommendations` asserts a luck decade not present in `luck` inputs.

---

## Best Practices

1. Emit structured `status` + `reason_codes` for every section.
2. Keep display titles localized; keep `section_id` stable.
3. Prefer linking recommendations to `inputs_used` traces.
4. Review new section proposals against [01](01_INTERPRETATION_STANDARD.md) before coding.

---

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Hiding Unavailable sections | Show honest empty state |
| Putting Useful God prose inside Overview only | Use proper section ownership |
| Using Appendix for core conclusions | Move to Summary/Recommendations |
| Fear copy in Unfavorable God | Apply [03](03_NARRATIVE_GUIDE.md) + [06](06_TERMINOLOGY_STYLE_GUIDE.md) |

---

## Future Expansion

- Sub-sections for Annual / Monthly luck
- Domain packs: relationship, career, finance, health (optional family)
- A/B section visibility by commercial SKU without changing this catalogue’s IDs

---

## Cross References

- [01_INTERPRETATION_STANDARD.md](01_INTERPRETATION_STANDARD.md) — completeness & lifecycle  
- [03_NARRATIVE_GUIDE.md](03_NARRATIVE_GUIDE.md) — wording  
- [04_EXPLANATION_POLICY.md](04_EXPLANATION_POLICY.md) — depth  
- [05_SENTENCE_PRIORITY.md](05_SENTENCE_PRIORITY.md) — conflicts  
- [06_TERMINOLOGY_STYLE_GUIDE.md](06_TERMINOLOGY_STYLE_GUIDE.md) — lexicon  
- [INDEX.md](INDEX.md) — navigation  

---

## Version

`1.0.0`

## Status

**Frozen — Section Contract Catalogue**

## Review Checklist

- [ ] All listed sections have Purpose through Output Example
- [ ] Priorities unique enough for deterministic ordering
- [ ] Mandatory vs optional aligned with Standard
- [ ] No ownership conflicts across sections
- [ ] Examples comply with Narrative Guide
- [ ] CHANGELOG updated on any section_id change
