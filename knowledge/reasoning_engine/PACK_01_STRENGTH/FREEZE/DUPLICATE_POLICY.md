# Duplicate Policy — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | DUPLICATE_POLICY |
| Status | FROZEN |

---

# 1. Principle

Runtime **must not discover** duplicates by embedding similarity or LLM.

Every overlap is a **declared** `duplicate_cluster` on the catalog row.

If two official units overlap and share no cluster, that is an **authoring defect**, not a runtime guess.

---

# 2. Cluster ownership

| Field | Rule |
|-------|------|
| `cluster_id` | `DUP-STR-<NAME>` e.g. `DUP-STR-FULL_TANK` |
| Owner | Catalog / Knowledge governance, not the engine |
| Members | Official units listing that `duplicate_cluster` |
| Representative | One member flagged `cluster_role = representative` |
| Others | `cluster_role = member` |

Exactly one representative per cluster.

---

# 3. Frozen PACK-01 clusters (declared)

| Cluster | Representative (intended) | Members include |
|---------|---------------------------|-----------------|
| `DUP-STR-FULL_TANK` | MEAN-ST-01 | ADV stress_tolerance; generic persist |
| `DUP-STR-ENDURANCE_AS_PROOF` | CHAL-ST-endurance-as-proof | MEAN-ST-03 |
| `DUP-STR-CARRY_LOAD` | ADV-ST-responsibility | CAR “persist”; extra carry ADV |
| `DUP-STR-BATTERY` | MAR-ST-bond | CHAL-ST-battery |
| `DUP-STR-C1_QUALIFIER` | WHY polarities + conclusion qualified | extra EDGE paragraph |

Authoring must attach these ids when catalog rows are filled. This freeze **names** the clusters so runtime cannot invent others for V1.0.

---

# 4. Representative selection (if two claim representative)

Deterministic: `specificity` cause_specific > class_level > generic, then `customer_value` critical > high > medium > low, then `knowledge_id` ascending.

Governance should prevent two representatives. This rule is the fail-safe.

---

# 5. Merge policy

At runtime:

1. Group PASS units by `duplicate_cluster` (ignore `none`).
2. Keep representative if it PASSed.
3. If representative failed the gate, keep the next member by §4.
4. Drop others: `REJECTED_DUPLICATE`.
5. Do not merge across clusters.
6. Do not merge `none` with anything.

Catalog merge (deprecate loser) is governance, not runtime.

---

END
