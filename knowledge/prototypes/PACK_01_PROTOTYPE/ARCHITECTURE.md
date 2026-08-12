# Architecture — PACK-01 Prototype

| Field | Value |
|-------|-------|
| Document | ARCHITECTURE |
| Pack | PACK-01 Prototype |
| Version | 1.0.0 |

---

# 1. Purpose

Define the prototype layers so later packs copy the skeleton, not the Strength sentences.

---

# 2. Pipeline

```text
Strength Facts (published, immutable)
        ↓
Evidence Layer          normalize, group, polarity, missing, conflict
        ↓
Interpretation Standard apply Mode A / Mode B contracts, leak ban, honesty
        ↓
Knowledge Selection     pick IK-STR-* units by class + present causes
        ↓
Priority / Conflict     keep primary class; keep both polarities; drop illegal units
        ↓
Duplicate Removal       one information type per section
        ↓
Sentence Composer       one unit → one sentence job
        ↓
Transition Engine       structural bridges only
        ↓
DualModeInterpretation
        ├── Mode A Validation
        └── Mode B Customer
```

No LLM.

No rescoring.

No Rule Database write.

---

# 3. Layer ownership

| Layer | Owns | Must not |
|-------|------|----------|
| Strength Facts | Published class, scores, matched rules | Be edited here |
| Evidence Layer | Grouping, polarity, missing, leak_class | Recalculate strength |
| Interpretation Standard | Section shells, So What, leak ban | New BaZi doctrine |
| Interpretation Knowledge | What to say (`IK-STR-*`) | Decide the class |
| Knowledge Selection | Eligibility predicates | Hard-code CASE-0001 prose |
| Sentence Composer | Assembly, order, jobs | Invent facts |
| Mode A | Audit projection | Appear in customer report |
| Mode B | Customer projection | Leak internals |
| Report Engine | (out of scope) | — |

---

# 4. Relationship to existing packs

| Pack | Role in this prototype |
|------|------------------------|
| Rule Database / Strength Engine | Upstream facts only. Unchanged. |
| `knowledge/interpretation_standard/PACK_01_STRENGTH/` | HOW |
| `knowledge/interpretation_knowledge/PACK_01_STRENGTH/` | WHAT |
| This folder | SELECT + COMPOSE demonstration |
| Production Interpretation Engine | Not modified |
| Report Engine | Not modified |

Where this prototype and a later production engine conflict, the Interpretation Standard still wins on content architecture.

---

# 5. Prototype vs production

| | Prototype | Production (later) |
|--|-----------|-------------------|
| Location | `knowledge/prototypes/` | `engines/` (not now) |
| Runtime | Documented stages + CASE-0001 trace | Stateless engine |
| Knowledge | References existing markdown units | Same units, machine catalog |
| Example | CASE-0001 only | Many cases |
| LLM | Forbidden | Forbidden |

---

# 6. Reuse contract for later packs

Replace only:

- Fact source (PatternResult, UsefulGodResult, …)
- Knowledge prefix (`IK-PAT-*`, `IK-UG-*`, …)
- Domain cause catalog

Keep:

- Evidence Layer item contract
- Dual Mode A / B
- Selection predicates (`use_when` / `do_not_use_when`)
- Composer jobs
- Duplicate / conflict / transition / priority modules

A pack that outputs only a label has failed this architecture.

---

# 7. Invariants

1. Mode B claims ⊆ Mode A traces.
2. Primary class = published Strength class (mapped, never upgraded).
3. Missing data stays missing.
4. No Pattern / Useful God / Temperature theft into Strength input.
5. Deterministic: same facts → same DualModeInterpretation.

---

END
