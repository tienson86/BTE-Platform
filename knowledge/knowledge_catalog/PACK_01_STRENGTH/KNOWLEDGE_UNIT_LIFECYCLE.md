# Knowledge Unit Lifecycle — PACK-01 Strength

| Field | Value |
|-------|-------|
| Document | KNOWLEDGE_UNIT_LIFECYCLE |
| Pack | PACK_01_STRENGTH |
| Version | 1.0.0 |

---

# 1. States

```text
Draft → Validated → Frozen
                ↘ Deprecated
         Validated → Deprecated
         Frozen → Deprecated
```

There is no skip from Draft to Frozen.

PACK-01 catalog output starts in **Draft**.

---

# 2. Draft

A unit is Draft when:

- It was normalized from a source paragraph
- Schema fields are present
- `source_document` is set
- `duplicate_cluster` is set (`NONE` or a named cluster)
- Status has not passed review

Draft units **must not** be treated as production Customer Mode inventory.

A Reasoning prototype may read Draft units only as a design aid.

---

# 3. Validated

A unit becomes Validated only after the review in [VALIDATION_RULES.md](VALIDATION_RULES.md).

Validated means: eligible for Reasoning selection design and for Customer Mode trials.

Validated does not mean the pack is Frozen.

---

# 4. Frozen

A unit becomes Frozen when a catalog version is locked for production.

Frozen units:

- Keep the same `knowledge_id`
- Change meaning only by new version + review
- Are the only units a production Reasoning Engine should select for Customer Mode

This delivery does **not** freeze units.

---

# 5. Deprecated

Set `status` to `Deprecated` when:

- The claim was split into new IDs
- The claim duplicates a representative and should not remain selectable
- The claim is unsafe or out of subject

Deprecated IDs are never reused.

Customer Mode: never.

Validation Mode: may record `REJECTED_DEPRECATED` if a selector still points at them.

---

# 6. Split / merge

Split: new IDs, old ID Deprecated or narrowed. Both declare clusters and conflicts.

Merge: only inside one `duplicate_cluster`. Survivor stays. Loser Deprecated. Runtime reason: `MERGED_DUPLICATE_CLUSTER`.

This catalog does not perform production merges. It only declares clusters.

---

# 7. Version

Unit `version` starts at `1.0.0`.

Compatible wording fix after Validated: patch.

Claim meaning change: minor or major; new review required.

`knowledge_id` does not change when version changes.

---

END
