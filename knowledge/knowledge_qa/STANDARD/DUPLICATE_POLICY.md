# Duplicate Policy — V1.0

| Field | Value |
|-------|-------|
| Document | DUPLICATE_POLICY |
| Standard | Knowledge QA V1.0 |

---

# 1. Purpose

Prevent the same customer insight from printing twice under narrative budget.

Duplicates waste budget, confuse emphasis, and break consultant trust.

---

# 2. Frozen taxonomy

| Term | Definition |
|------|------------|
| **Duplicate** | Same So what, same effective conditions, interchangeable in Customer Mode |
| **Semantic duplicate** | Different wording; customer cannot distinguish insight |
| **Near duplicate** | Overlapping insight; one unit subsumes or partially repeats another |
| **Cross-pack duplicate** | Same insight in two packs without declared cross-pack dependency |
| **Representative** | Single unit selected per cluster under budget |
| **Cluster** | Governance-owned `duplicate_cluster` id; members share selection budget |

---

# 3. Evaluation rules

| Rule | Action |
|------|--------|
| Declared cluster | Score Duplicate Risk per membership; representative must be identified |
| Undeclared overlap | REVIEW minimum; governance assigns cluster |
| MEANING vs ADVANTAGE overlap | Near duplicate — prefer MEANING for identity, ADV for use |
| CAUSE taxonomy + atomic | Taxonomy intro often LOW EXPLAINABILITY; atomic units carry value |
| Cross-topic same class | Check all topics for same class cluster |

---

# 4. QA scoring (Duplicate Risk criterion)

| Situation | Score |
|-----------|-------|
| NONE, no overlap | 10 |
| Declared cluster, clear representative | 7 |
| Declared cluster, representative unclear | 5 |
| Undeclared semantic duplicate | 3 |
| Two representatives same cluster | 0 |

---

# 5. Resolution actions

| Finding | Owner | Action |
|---------|-------|--------|
| Semantic duplicate | Governance | Merge or deprecate one id |
| Near duplicate | Author | Differentiate claim or assign cluster |
| Cross-pack | Governance | Declare dependency or deprecate one pack’s unit |
| Representative conflict | Reasoning + Governance | Pin representative in catalog metadata |

---

# 6. Runtime rule

Reasoning selects **at most one representative per cluster** per narrative unless governance explicitly allows multi-print.

QA does not implement runtime — QA ensures clusters are **declared before Validated**.

---

# 7. PACK-01 reference clusters (examples only)

| Cluster | Example ids |
|---------|-------------|
| DUP-STR-FULL_TANK | MEAN-0006, ADV-0014 |
| DUP-STR-ENDURANCE_AS_PROOF | ADV-0009, ADV-0013 |
| DUP-STR-CARRY_LOAD | ADV-0006, ADV-0013 |
| DUP-STR-BATTERY | MEAN-0008, ADV-0015 |
| DUP-STR-C1_QUALIFIER | CAUS-0020–0024 vs atomics |

Detail: [QA_EXAMPLES.md](QA_EXAMPLES.md).

---

END
