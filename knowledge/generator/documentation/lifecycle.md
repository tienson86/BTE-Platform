# Generation Lifecycle

| Field | Value |
|-------|-------|
| **Generator version** | 1.0.0 |
| **Aligns with** | KD-3 package status + KD-4 workflow |

---

## 1. End-to-end

```
idea (profile)
  → draft (skeleton … tests)
  → review (validation + documentation + human reviews)
  → validated (release candidate)
  → released (immutable)
  → deprecated
  → archived
```

Generator owns idea → released emission. Deprecate/archive remain KD-4.

---

## 2. Stage ↔ status

See `generation_workflow.md`. Summary:

| Pipeline | Editable | AI allowed |
|----------|----------|------------|
| profile → tests | yes (`draft`) | yes, ceiling draft |
| validation → documentation | limited | no sole-approval |
| release_candidate | frozen | no |
| released | **never** | no |

---

## 3. Quality along the lifecycle

| Moment | Minimum gate |
|--------|----------------|
| Enter review | Bronze trajectory; PVP-MINIMAL passed in draft |
| Release candidate | Bronze measured; official default Silver |
| Analytical official release | Gold recommended |
| Platinum | optional excellence + PVP-RELEASE hygiene |

---

## 4. Version lifecycle

- Generator `1.0.0` is this Foundation freeze.
- Packages version independently (`0.1.0` drafts → SemVer releases).
- Regenerating a new version of a package uses the same `package_id` and a new `package_version`.
- Changing meaning of `package_id` is forbidden; create a new id.

---

## 5. Failure handling

Reject → return to `draft`. Fix-forward. Never patch `released` bytes.

Missing taxonomy/ontology/rule/evidence references fail closed (GV-*).

---

## 6. Parallelism

Many instance profiles may run in parallel after id/prefix reservation. Publication order is deterministic via package index sort (`package_id`, `package_version`, locale `C`) when an index sprint exists.
