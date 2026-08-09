# Foundation Compatibility Policy

| Field | Value |
|-------|-------|
| **Document** | FOUNDATION_COMPATIBILITY |
| **Foundation version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## 1. Backward compatibility

Foundation 1.0.0 consumers MUST continue to work:

- AX-1 `AnalysisPipeline` 1.0.0 remains a compatibility surface (Calendar → Temperature).
- AX-2 `CanonicalPipeline` 2.0.0 remains the only supported full Analysis Knowledge flow.
- AX-3 `CanonicalDecisionPipeline` 1.0.0 remains the only supported Decision Package flow.
- Sealed package checksums remain valid indefinitely for that `package_id` + `package_version`.
- Public type names used by tests and engines at freeze time are stable.

Removing or renaming those surfaces requires a Foundation **major**.

---

## 2. Forward compatibility

Foundation 1.0.0 does not promise to understand future schema generations.

Rules:

- Unknown `schema_version` → reject at load.
- Unknown stage ids → dependency violation (do not ignore).
- Unknown optional JSON fields on packages MAY be ignored by 1.0.0 loaders if `additionalProperties` is allowed by KD-3.
- Unknown diagnostic codes MAY be logged; they MUST NOT crash `run()`.

Forward features ship as new packages/engines or a new Foundation version.

---

## 3. Package compatibility

| Check | 1.0.0 rule |
|-------|------------|
| `status` | Must be `released` to execute |
| `schema_version` | Must equal `2.0.0` |
| `package_version` | Must satisfy stage SemVer constraint (default `^1.0.0`) |
| `package_type` | Analysis cores: `analytical`. Useful God stack: `decision`. |
| Checksum | SHA-256 two-pass; non-null on release |
| Optional deps | Validated only when the peer is co-loaded |
| Required deps | Empty on Foundation-era cores; pipeline order is orchestration |

A newer compatible package (`1.2.0` under `^1.0.0`) MAY replace `1.0.0` at load time. It MUST be a **new sealed artifact**, not an edit of `1.0.0`.

---

## 4. Schema compatibility

- Knowledge envelope: **2.0.0 only**.
- Package spec generation: **1.0.0**.
- Rule object required fields remain those enforced by package tests at freeze (id, category, priority, conditions, result, explanation, references, tags, enabled).
- Schema enum extensions (for example adding a new `package_type`) are Foundation **minor** only if existing values remain valid; removal is **major**.

---

## 5. Engine compatibility

| Engine | Foundation 1.0.0 stance |
|--------|-------------------------|
| Rule Engine | Frozen public behavior relative to Foundation; not modified by F-1 |
| Analysis Engine | AX-1 + AX-2 orchestration frozen; V1 runtime `CANONICAL_STAGES` untouched |
| Decision Engine | AX-3 frozen |
| Interpretation Engine | Exists as product code; **not** an active canonical Decision/Analysis stage |
| Report Engine | Exists as product code; **not** an active canonical stage |
| Luck Engine | Phase IV extension; not Foundation 1.0.0 |

Engines MUST NOT import each other’s internal modules. Communication is via published results and contracts.

---

## 6. Decision compatibility

Decision stack order is frozen:

```
Useful God Foundation → Priority → Override → Canonical Decision Result
```

Compatibility rules:

- Override may only replace a **published** resolved decision.
- Upstream Decision outputs are immutable for the run.
- `decision_role = override` packages do not identify or rank Useful God.
- `final_useful_god` is the downstream Decision contract. Luck / Interpretation (future) consume it; they do not reread Foundation internals.

---

## 7. Analysis compatibility

Analysis Knowledge order is frozen (AX-2):

```
Calendar → Four Pillars → Seasonal → Strength → Temperature
  → Pattern → Pattern Evaluation → Useful God → Analysis Result
```

Compatibility rules:

- Stages consume published upstream outputs only.
- AX-1 five-stage result remains valid for callers that still use `AnalysisPipeline`.
- Pattern Evaluation publishes quality / confidence / integrity / stability / score for Decision.
- Analysis Engine MUST NOT evaluate SKC / SEC / TEC / PAT / PEV / UGD rule bodies in the orchestration layer.

---

## 8. Dual-read with V1

Where packages declare `compatible_with_v1: true`, V1 Rule Database paths remain a dual-read reference. Foundation 1.0.0 does not delete V1 databases. It also does not allow V1 identifiers to collide with V2 prefixes (SKC / SEC / TEC / PAT / PEV / UGD / UGP / UGO).
