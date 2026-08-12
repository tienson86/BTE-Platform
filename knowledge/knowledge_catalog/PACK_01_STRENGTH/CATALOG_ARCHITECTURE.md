# Catalog Architecture — PACK-01 Strength

| Field | Value |
|-------|-------|
| Document | CATALOG_ARCHITECTURE |
| Pack | PACK_01_STRENGTH |
| Version | 1.0.0 |
| Status | Draft |

---

# 1. Position

```text
Strength Engine (published facts)
        ↓
Interpretation Knowledge (prose source — unchanged)
        ↓
Knowledge Catalog (this pack — Knowledge Units)
        ↓
Reasoning Engine (select / rank / conflict — not implemented here)
        ↓
NarrativePlan
        ↓
Sentence Composer + Interpretation Standard
        ↓
Customer Mode / Validation Mode
```

The catalog does not compute Strength.

The catalog does not write sentences.

The catalog does not resolve conflicts.

---

# 2. One paragraph → one or more units

Every consulting paragraph in the source pack becomes one or more Knowledge Units.

Split when one paragraph contains **independent claims**.

Do not split when bullets are supporting points of the same claim.

Do not keep consulting knowledge only in prose. After this pack, the catalog is the selectable layer.

Composition rules, bans, and “how to use this file” notes are **governance**. They live in:

- this architecture
- [VALIDATION_RULES.md](VALIDATION_RULES.md)
- `limitations` on units

They are not Customer Mode claims.

---

# 3. Folder map

| Folder | Source | Purpose values |
|--------|--------|----------------|
| `catalog/meaning/` | `01_MEANINGS.md` | MEANING |
| `catalog/causes/` | `02_CAUSES.md` | WHY |
| `catalog/advantages/` | `03_ADVANTAGES.md` | ADVANTAGE, DECISION_MAKING, LEADERSHIP, LEARNING |
| `catalog/challenges/` | `04_CHALLENGES.md` | CHALLENGE, WARNING |
| `catalog/personality/` | `05_PERSONALITY.md` | PERSONALITY |
| `catalog/career/` | `06_CAREER.md` | CAREER |
| `catalog/wealth/` | `07_WEALTH.md` | WEALTH |
| `catalog/marriage/` | `08_MARRIAGE.md` | MARRIAGE |
| `catalog/health/` | `09_HEALTH.md` | HEALTH |
| `catalog/luck/` | `10_LUCK.md` | LUCK |
| `catalog/recommendation/` | `11_RECOMMENDATIONS.md` | RECOMMENDATION |
| `catalog/edge_cases/` | `12_EDGE_CASES.md` | EDGE_QUALIFIER |
| `catalog/examples/` | `13_EXAMPLES.md` | not used in Customer Mode |

One file per class (or per cause family). Several units per file. Units are separated by a heading that is the `knowledge_id`.

---

# 4. Knowledge ID policy (frozen)

```text
IK-STR-<TOPIC>-<NNNN>
```

| Part | Rule |
|------|------|
| `IK` | Interpretation Knowledge |
| `STR` | PACK-01 Strength |
| `TOPIC` | See §5 |
| `NNNN` | Four-digit sequence inside that topic, starting at `0001` |

IDs are never reused after deprecation.

New units **append**. Do not insert a new meaning between `0001` and `0002` by shifting numbers.

Gaps are allowed only if a draft ID is withdrawn before first publication. After any external reference, the ID is retired via Deprecated, not recycled.

---

# 5. Topic codes

| Code | Folder | Future expansion |
|------|--------|------------------|
| `MEAN` | meaning | Later packs: `IK-PAT-MEAN-0001` |
| `CAUS` | causes | Cause families stay under CAUS, not MEAN |
| `ADV` | advantages | Facet is not part of the ID |
| `CHAL` | challenges | |
| `PERS` | personality | |
| `CAR` | career | |
| `WEA` | wealth | |
| `MAR` | marriage | |
| `HEA` | health | |
| `LUCK` | luck | |
| `REC` | recommendation | |
| `EDGE` | edge_cases | Shared / borderline; class may be `edge` or `all` |
| `EX` | examples | Teaching only |

Class is **not** encoded in the ID. Class is a field. This lets one ID stay stable if a unit’s class gate is corrected during review.

Future packs use a new pack token, not a new numbering scheme:

```text
IK-STR-MEAN-0001
IK-PAT-MEAN-0001
IK-TGD-MEAN-0001
IK-UG-MEAN-0001
```

Do not reuse `STR` for Pattern.

---

# 6. Traceability

Every unit sets `source_document` to the exact source filename under:

`knowledge/interpretation_knowledge/PACK_01_STRENGTH/`

Example: `01_MEANINGS.md`

The catalog points at prose. It does not replace prose.

---

# 7. Selection order (knowledge-level, not code)

```text
Published classification
        ↓
MEANING units for that class
        ↓
WHY units only for causes in an allowed evidence state
        ↓
ADVANTAGE / CHALLENGE / domain units for that class
        ↓
LUCK units only if luck is published
        ↓
RECOMMENDATION units that chain from kept meaning + challenges
        ↓
EDGE_QUALIFIER only when the edge condition is published
        ↓
EX units → always reject for Customer Mode
```

Absence of a published fact is not filled with a generic paragraph.

`INACTIVE` is not `MISSING`. A drain-off fact rejects drain-leak units (`REJECTED_FACT_INACTIVE`). An unpublished drain rejects them (`REJECTED_MISSING_EVIDENCE`).

---

# 8. Duplicate clusters

A unit belongs to **exactly one** cluster or `NONE`.

PACK-01 reuses the clusters already named for this pack:

| Cluster | Intended representative in this catalog |
|---------|-----------------------------------------|
| `DUP-STR-FULL_TANK` | `IK-STR-MEAN-0006` |
| `DUP-STR-ENDURANCE_AS_PROOF` | `IK-STR-CHAL-0010` |
| `DUP-STR-CARRY_LOAD` | `IK-STR-ADV-0013` |
| `DUP-STR-BATTERY` | `IK-STR-MAR-0007` |
| `DUP-STR-C1_QUALIFIER` | `IK-STR-EDGE-0001` |

Runtime must not invent clusters.

Further overlaps noticed during authoring that do **not** fit these five are left as `NONE` and listed as a remaining gap. They are not silently clustered.

---

# 9. Conflicts

Units may list other `knowledge_id` values in `conflicts_with`.

This catalog **declares**. It does not resolve.

Reasoning Engine actions remain: qualify, defer, expose, or drop.

---

# 10. Reason codes

Units may only name codes from the frozen Reason Codes list.

This catalog does not invent codes.

---

# 11. Relationship to Reasoning FREEZE schema

The Reasoning Engine FREEZE documents a related schema with different enumerations (integer priority, `class_level` specificity, `authoring_status`, ID shape `IK-STR-<TOPIC>-<CLASS>-<NN>`).

This work package freezes **this** catalog’s schema and ID policy.

Those two contracts are **not identical**. Alignment is a remaining gap. This catalog does not edit FREEZE files.

A mapping from catalog IDs to CASE-0001 golden placeholders lives in [CATALOG_INDEX.md](CATALOG_INDEX.md).

---

# 12. Non-goals

- JSON, YAML, database, runtime code
- New interpretations
- Rule IDs, scores, thresholds
- Useful God, Pattern, Ten God lectures
- Medical diagnoses
- Guaranteed timelines

---

END
