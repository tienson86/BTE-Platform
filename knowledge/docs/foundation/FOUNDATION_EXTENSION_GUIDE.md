# Foundation Extension Guide

| Field | Value |
|-------|-------|
| **Document** | FOUNDATION_EXTENSION_GUIDE |
| **Foundation version** | 1.0.0 |
| **Status** | Canonical |
| **Owner** | BTE Architecture Board |

---

## Rule

```
Foundation is extended.
Foundation is not modified.
```

All post-1.0.0 capability lands as **new packages**, **new engines**, **new pipelines**, or **new contracts** that consume frozen published outputs.

---

## 1. New packages

How:

1. Author under `knowledge/packages/<domain>/<name>/`.
2. New `package_id`. Do not reuse a sealed id.
3. Comply with KD-3, KD-4, Generator v1.0, PVP profile appropriate to maturity.
4. Consume **published contracts only**. Never import another package’s rule internals.
5. Declare optional peers; keep required deps empty unless governance approves a hard load dependency.
6. Seal checksum via two-pass SHA-256. Released bytes are immutable.

Useful God stack pattern (frozen example):

```
Foundation → Priority → Override
```

Future school / language / luck-decision packages follow the same additive stack. They do not edit `bz_06`, `bz_07`, or `bz_08`.

---

## 2. New engines

How:

1. Create a new engine directory (for example `engines/luck_engine/` when Phase IV starts).
2. Do not import internal modules of Analysis Engine or Decision Engine.
3. Consume public result objects / published package contracts.
4. Own exceptions, tests, and documentation.
5. Register new orchestration only inside the new engine until a Foundation minor/major adds it to a canonical catalog.

Foundation 1.0.0 does **not** include Luck, Interpretation, or Report as active canonical stages. Those engines are Phase IV–VI extensions.

---

## 3. New pipelines

How:

1. Prefer a new pipeline id and version over mutating AX-2 / AX-3 order.
2. Future stages already reserved (Luck Cycle, Interpretation, Report on Analysis; Luck / Annual / Monthly / Interpretation on Decision) are enabled by **new Foundation-approved catalog updates**, not by informal code edits.
3. Enabling a reserved stage that already exists in the frozen catalog is a **Foundation minor or major** per impact (additive enable vs order change).
4. Pipelines remain deterministic, append-only, and diagnostics-only at the public `run()` boundary.

---

## 4. New contracts

How:

1. Publish new output names. Do not rename frozen fields.
2. Downstream contracts consume upstream published outputs only.
3. Analysis contracts and Decision contracts stay separate.
4. New optional fields on a new package version are allowed. Changing meaning of an existing field is a breaking Foundation/package major.

Frozen contract families:

- Package published inputs / outputs (`assets/published_*.json`)
- Canonical Analysis Result (AX-2)
- Canonical Decision Result (AX-3)
- Execution / Decision traces and audits
- Diagnostics codes already issued

---

## 5. Future AI integration

AI may:

- Author draft packages through Generator v1.0 profiles
- Explain `decision_trace` / `execution_trace` / evidence bundles
- Propose override packages

AI may not:

- Bypass canonical pipelines
- Rewrite sealed packages
- Invent unpublished score fields
- Modify Foundation freeze documents without a versioned change request

AI orchestration is a **consumer** of traces and contracts, not a second execution path.

---

## 6. Future plugins

Plugin rules:

| Plugin kind | Lands as | Modifies Foundation? |
|-------------|----------|----------------------|
| School override package | New package_id | No |
| Language expansion | New language in a new package version or language pack | No |
| Extra diagnostic exporter | New engine or report adapter | No |
| New Decision layer (e.g. luck usefulness) | New package + later pipeline stage | Only when catalog is version-upgraded |
| Alternate checksum store | Out of scope for 1.0.0 | Requires major |

Plugins register through the existing stage registry / package loader extension points. They do not fork frozen engines in place.

---

## 7. Extension checklist

Before merging an extension:

- [ ] No edit to sealed package checksums
- [ ] No edit to AX-2 / AX-3 public APIs unless Foundation version bump is approved
- [ ] New ids only
- [ ] Published-contract consumption only
- [ ] Tests scoped to the new module
- [ ] Documentation additive

If any box fails, stop. That work is a Foundation change, not an extension.
