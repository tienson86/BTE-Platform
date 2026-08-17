# BETA0 Knowledge Lock

| Field | Value |
|-------|-------|
| Document | BETA0_KNOWLEDGE_LOCK |
| Date | 2026-08-17 |
| Status | **FROZEN** |
| Owner | Knowledge Board + Product Owner |
| Rule | No ownership ambiguity. One owner per surface. |

Knowledge is data.
It is not a new runtime.
It does not calculate astrology.
It does not compose customer prose.

---

## Ownership

| Surface | Authoritative owner | Location | May not |
|---------|---------------------|----------|---------|
| Knowledge Domains / Rule Database | Knowledge Board | CSV-first rule DB under `knowledge/` and engine loaders | Be replaced by Python if/else |
| Knowledge packages | Knowledge Board | `bz_01` … `bz_09` and domain packages | Be rewritten as a new framework |
| Concept Layer | Knowledge Board | Concept packs under `knowledge/` | Become a second narrative source |
| Canon | Knowledge Board + Chief Editor | Existing knowledge / editorial canon only | Gain a new Canon in Beta |
| Editorial Standard | BTE Chief Editor | `knowledge/editorial/BTE_EDITORIAL_STANDARD_V1.md` (ES-V1) | Be replaced by a style guide in code |
| Published Narrative | Interpretation Foundation publish | `engines/interpretation_engine/foundation/narrative/publish/` (`PublishedNarrativeBuilder`) | Recalculate or rewrite knowledge |
| Professional Publisher | Same publish package | `professional.py` · `editions.py` | Become a second composer |

---

## Boundary

```
Rule / Concept / Canon
        ↓
    Knowledge selection
        ↓
    Narrative Composer
        ↓
    Published Narrative
        ↓
    Professional Publisher
```

Upstream knowledge answers: what is true and admissible.
Composer answers: what sentence exists.
Publisher answers: which already-composed evidence reaches which edition.
Editorial Standard answers: may this sentence reach a paying customer.

No layer may take another’s job.

---

## Explicit prohibition

During Beta, do **not** add:

- a new Knowledge system
- a new Canon beside ES-V1 and existing packages
- a new Matrix as a product layer
- a new Framework that owns customer meaning

Knowledge Improvement (records, coverage, references) is allowed.
A new knowledge **system** is an Architecture Change.

---

## Official status

**Knowledge ownership is frozen for Beta 0.**
No ownership ambiguity remains.
