# Catalog Governance — FROZEN V1.0

| Field | Value |
|-------|-------|
| Document | CATALOG_GOVERNANCE |
| Status | FROZEN |

---

# 1. Principle

Catalog rows are governed assets.

Prose knowledge chapters remain the consulting text.

The catalog is the machine contract.

No silent runtime invention of units, clusters, or purposes.

---

# 2. Add

1. Allocate next `knowledge_id` in the topic range (never reuse).
2. Fill every frozen schema field.
3. Declare `duplicate_cluster` (`none` or an existing cluster id).
4. Status = `draft`.
5. Review: evidence keys, class gate, advice safety (`absolute` advice forbidden).
6. Approve → `official`.
7. Bump **catalog version** (patch if additive and compatible).

A unit without `duplicate_cluster` is invalid.

---

# 3. Update

- Official units: new **unit version**; old version remains for trace.
- Do not change `knowledge_id`.
- Do not change `purpose` (that is a split + deprecate).
- Compatible field adds: catalog minor.
- Meaning change of a claim: catalog minor or major per [VERSIONING.md](VERSIONING.md).

---

# 4. Deprecate

- Set `authoring_status = deprecated`.
- Record successor id if any.
- Deprecated units never enter Customer Mode.
- Validation may list them as `REJECTED_DEPRECATED` if a selector still points at them.

---

# 5. Merge

- Allowed only inside one `duplicate_cluster`.
- Surviving id = declared **representative** (see Duplicate Policy).
- Loser deprecated with pointer to representative.
- Reason code: `MERGED_DUPLICATE_CLUSTER`.

Runtime merge of undeclared units is **forbidden**.

---

# 6. Split

- New ids for new purposes.
- Old unit deprecated or narrowed.
- Both must declare clusters and conflicts.
- Catalog minor or major if Customer Mode meaning changes.

---

# 7. Review / approve

Roles: Author, Knowledge Reviewer, Governance Reviewer.

Official requires: schema complete, no free-text domain/purpose, duplicate cluster set, evidence keys from the frozen fact-key list.

---

# 8. Version

See [VERSIONING.md](VERSIONING.md).

Governance changes to process require freeze V1.1 — not silent.

---

END
