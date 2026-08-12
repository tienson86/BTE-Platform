# Knowledge Architecture — PACK-01 Strength

| Field | Value |
|-------|-------|
| Document | KNOWLEDGE_ARCHITECTURE |
| Pack | PACK-01 Strength Interpretation Knowledge |
| Version | 1.0.0 |
| Status | KNOWLEDGE ONLY |

---

# 1. Purpose

This document defines how Strength interpretation knowledge is organized so a future Interpretation Engine can select **what to say** without owning the knowledge.

The Interpretation Standard remains the contract for **how to say it**.

---

# 2. Position in the Platform

```text
Product Manifesto
        ↓
Interpretation Standard          ← HOW (Mode A / Mode B, sentence, value)
        ↓
Interpretation Knowledge         ← WHAT (this pack)
        ↓
Future Interpretation Engine     ← SELECT + COMPOSE
        ↓
Customer Mode / Validation Mode
        ↓
Report / Portal
```

Upstream facts come from Strength Engine.

This pack does not read Rule Database files.

This pack does not compute.

---

# 3. Knowledge Unit

The atomic record is a **knowledge unit**.

A unit is one reusable consulting claim.

Logical fields (not a runtime schema):

| Field | Role |
|-------|------|
| `unit_id` | Stable identity, e.g. `IK-STR-MEAN-STRONG-01` |
| `class` | `very_strong` / `strong` / `balanced` / `weak` / `very_weak` / `all` / `edge` |
| `topic` | meaning / cause / advantage / challenge / personality / career / wealth / marriage / health / luck / recommendation / edge / example |
| `facet` | e.g. leadership, saving, conflict_style, supportive_luck |
| `so_what` | The lived claim |
| `use_when` | Which published facts make this unit eligible |
| `do_not_use_when` | When this unit would invent or contradict |
| `pairs_with` | Related units in other topics (not copies) |
| `leak_safe` | Always true for this pack — no Rule IDs, scores, or enums |

A unit is eligible only when the published Strength class matches, and when any named cause (season, root, drain, luck support, …) is actually present in the case.

If the cause is absent, the unit stays unused.

Absence is not filled with a generic paragraph.

---

# 4. Class Set

| ID | English | Vietnamese |
|----|---------|------------|
| `very_strong` | Very Strong | Thân Cực Vượng |
| `strong` | Strong | Thân Vượng |
| `balanced` | Balanced | Trung Hòa |
| `weak` | Weak | Thân Nhược |
| `very_weak` | Very Weak | Thân Cực Nhược |

These IDs are knowledge keys.

They are not customer-facing dumps.

Customer wording follows the Interpretation Standard.

---

# 5. Topic Ownership

Each file owns one information type.

| Topic | File | Must add | Must not repeat |
|-------|------|----------|-----------------|
| Meaning | 01 | Identity-level “what this standing is like to live” | Career lists, advice lists |
| Cause | 02 | Why the standing arises in chart structure | Personality portraits |
| Advantage | 03 | What it helps the person do well | Meaning restated as praise |
| Challenge | 04 | Operating cost, blind spot, typical mistake | Negated copy of 03 |
| Personality | 05 | How they speak, think, work, fight | Job titles |
| Career | 06 | Work environment and role fit | Personality adjectives only |
| Wealth | 07 | How force holds or releases money | Career paragraph |
| Marriage | 08 | How force takes space in a bond | Personality paragraph |
| Health | 09 | Energy, stress, body pacing | Metaphorical “health of spirit” only |
| Luck | 10 | Time interaction with natal standing | Natal meaning again |
| Recommendation | 11 | Do / avoid | Recap of 03–10 |
| Edge | 12 | Borderline and conflict knowledge | New scoring method |
| Example | 13 | Full consultant vignettes | New doctrine |

If two files can swap a paragraph without loss, one file has failed.

---

# 6. Selection Logic (Knowledge-Level, Not Engine Code)

A future engine should think in this order:

```text
Published Strength class
        ↓
Select meaning units for that class
        ↓
Select cause units only for causes present in the case
        ↓
Select advantage / challenge / domain units for that class
        ↓
If luck published: select luck-interaction units
        ↓
Select recommendations that follow from the selected meaning + challenges
        ↓
Compose using Interpretation Standard (Mode B)
```

This pack describes the units.

It does not implement the selector.

---

# 7. Cause Dimensions as Knowledge, Not Algorithms

Causes in this pack are consulting explanations:

- Season (Đắc Lệnh) — climate feeds or starves the Day Master
- Root (Đắc Địa / Thông Căn) — the person has ground, or does not
- Support (Đắc Thế) — allies and same-nature backup
- Drain — output without refill
- Control — pressure sitting on the Day Master
- Combination / clash / void — support merged, cancelled, or emptied
- Special structure — ordinary reading is not enough

Knowledge says what each cause **means in life**.

Knowledge does not say how to calculate it.

---

# 8. Honesty Rules

1. Do not write a unit that requires a cause the case may not have.
2. Mark such units `use_when` that cause is present.
3. Do not upgrade Strong to Very Strong inside knowledge.
4. Do not treat supportive luck as Useful God.
5. Do not treat Weak as a moral defect.
6. Do not invent careers, marriages, or illnesses as fate.

---

# 9. Relationship to Frozen Strength Knowledge

`knowledge/02_strength_knowledge/` owns analytical terminology and evaluation knowledge for the Strength Engine.

This pack owns **interpretation consulting knowledge**.

It may use the same class names.

It must not redefine scoring, weights, or rule assets.

It must not duplicate engine architecture documents.

---

# 10. Extensibility

Later packs (Pattern, Useful God, Ten Gods, ShenSha, Luck, Career, Marriage) SHOULD reuse:

- knowledge unit shape
- class-or-domain key
- topic ownership
- `use_when` / `do_not_use_when`
- So What requirement

They MUST NOT copy Strength paragraphs into another domain and relabel them.

---

# 11. Non-Goals

- Runtime code
- Sentence IDs (`SEN-…`)
- Rule IDs (`STR-…`)
- Confidence percentages
- Report layout

---

END
