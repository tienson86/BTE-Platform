# Runtime Gaps Audit — Decision / Transformation / Luck

**Sprint:** PILOT-1A  
**Mode:** Audit only — **no implementation**  
**Architecture Freeze:** AF-1 unchanged  

Pilot Replay matrix showed:

| Layer | Replay status |
|---|---|
| Decision | BLOCKED |
| Transformation | NOT_PRODUCED |
| Luck | INTERNAL_ONLY |

This document separates **engine capability**, **runtime exposure**, and **public contract availability**.

---

## 1. Decision

### Engine capability

| Item | Status |
|---|---|
| Code exists | **Yes** — `engines/decision_engine/` |
| Public type | `CanonicalDecisionPipeline`, `CanonicalDecisionResult` |
| Purpose | AX-3 decision orchestration over Decision Packages (useful-god foundation / priority / override stages) |
| Standalone runnable | Yes, as a library pipeline |

### Runtime exposure (OrchestratorService)

| Item | Status |
|---|---|
| Imported by `applications/api` | **No** |
| Stage in `PIPELINE_ORDER` | **No** `decision` stage |
| Called during `analyze` | **No** |

### Public contract availability

| Item | Status |
|---|---|
| On `data.pipeline` public list | **No** |
| On analyze JSON payload | **No** |
| QC2 decision snapshots | Exist under `knowledge/quality/qc2/snapshots/decision/` as **quality artifacts**, not live orchestrator output |

### Gap type

**Implementation / wiring gap + publication gap**

- Capability: present as a separate engine  
- Exposure: not wired into production orchestrator  
- Contract: not part of public analyze pipeline  

**Not** merely an adapter bug — Decision never enters the live path.

### Intentional?

Likely **intentional V1 scope freeze** (AF-1 public pipeline remains calendar→…→narrative). Treat as design limitation until product explicitly adds Decision to the public orchestration contract.

---

## 2. Transformation

### Engine capability

| Item | Status |
|---|---|
| Knowledge package | **Yes** — `knowledge/packages/transformation/core` (`bz_11_transformation_core`) |
| Declared outputs | Package publishes transformation contracts (e.g. `transformation_detected`, scores, diagnostics) |
| Dedicated TransformationEngine on live path | **No** producer found under `engines/` that emits `transformation_*` into Orchestrator payload |
| PatternEngine | Does **not** publish transformation detection as production fields |
| Combination package | Explicitly states combination **does not determine** transformation |

### Runtime exposure

| Item | Status |
|---|---|
| Orchestrator computes transformation | **No** |
| Fields on analyze payload | **Absent** (`transformation_detected` etc. not present) |

### Public contract availability

| Item | Status |
|---|---|
| Knowledge contract (package) | Released / documented |
| Runtime public API contract | **Not available** on `OrchestratorService.analyze` |
| Pilot CASE-0009 | Also blocked on missing reference chart data |

### Gap type

**Implementation gap (runtime producer) + publication gap**

- Knowledge capability: package exists  
- Engine capability on live path: missing / not wired  
- Contract availability to API clients: none  

Combination detection ≠ transformation detection (by package design). Do not treat combination absence as “transformation false”.

### Intentional?

Partially intentional separation of domains; **not** intentional to claim Pilot Transform PASS. Current state is an incomplete runtime realization of a released knowledge package.

---

## 3. Luck

### Engine capability

| Item | Status |
|---|---|
| Code exists | **Yes** — `engines/luck_engine.LuckEngine` |
| Instantiated in orchestrator | **Yes** — `self.luck_engine = LuckEngine()` |
| Built during analyze | **Yes** — Stage 7 `luck_engine.build(...)` |
| Consumed downstream | **Yes** — passed into Interpretation as `luck_context` |

### Runtime exposure

| Item | Status |
|---|---|
| Written to internal payload | **Yes** — `payload["luck"] = luck_context.to_dict()` |
| Stripped before return | **Yes** — `_INTERNAL_PAYLOAD_KEYS` includes `"luck"` |
| Public pipeline stage name | **No** — not in `PUBLIC_PIPELINE_ORDER` |

Evidence:

```146:157:applications/api/services/orchestrator.py
_INTERNAL_PAYLOAD_KEYS: frozenset[str] = frozenset(
    {
        ...
        "luck",
        ...
    }
)
```

### Public contract availability

| Item | Status |
|---|---|
| Clients of `/analyze` | **Cannot read** `data.luck` |
| Interpretation may use luck internally | Possible, but luck object itself is not published |
| QC2 luck snapshots | Quality artifacts only |

### Gap type

**Publication / adapter gap** (not missing engine)

- Capability: present and executed  
- Exposure: computed then intentionally stripped  
- Contract: internal-only by current public orchestration policy  

### Intentional?

**Yes — intentional public-contract limitation** under current AF-1 public pipeline. Changing this is a product/API contract decision, not a silent bugfix.

---

## 4. Comparison matrix

| Concern | Decision | Transformation | Luck |
|---|---|---|---|
| Engine capability | Present (separate) | Package yes / live producer no | Present |
| Runtime execution in analyze | No | No | Yes |
| Runtime exposure to payload (pre-finalize) | No | No | Yes then stripped |
| Public contract availability | No | No | No |
| Pilot Replay label | BLOCKED | NOT_PRODUCED | INTERNAL_ONLY |
| Gap class | Wiring + publication | Implementation + publication | Publication |
| Implement in PILOT-1A? | **No** | **No** | **No** |

---

## 5. Distilled definitions

| Term | Meaning |
|---|---|
| Engine capability | Code/package can compute the concern somewhere in the repo |
| Runtime exposure | Live `OrchestratorService.analyze` path computes and retains the concern |
| Public contract availability | Stable client-visible field/stage on the published analyze response |

---

## 6. Recommendations (future; not this sprint)

1. **Decision:** Product decision whether CanonicalDecisionPipeline becomes an orchestrator stage or stays offline/QC-only.  
2. **Transformation:** Design a single producer (not combination) that emits `transformation_*`, then wire publish rules; keep combination≠transformation invariant.  
3. **Luck:** If Pilot needs Luck PASS, either:  
   - publish `luck` under a versioned public contract, or  
   - add an explicit internal snapshot channel for Pilot (without claiming public PASS).  

Do not invent CASE-0008/0009 inputs to fake coverage.

---

## 7. Freeze statement

No engines, packages, pipelines, API contracts, UI, or AF-1 documents were modified for this audit.
