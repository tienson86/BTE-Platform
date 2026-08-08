# 02 — Capability Release Policy

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  
Depends on: `01_CAPABILITY_REGISTRY.md`  

---

## 1. Purpose

Define how a commercial capability moves from idea to production — and how it is frozen, revised, or rolled back.

**Release unit = Capability** (not Knowledge Unit, Engine, or Narrative pack).

---

## 2. Official stages

```
Proposed
  → Planned
  → Authoring
  → Golden Review
  → Integration
  → Production
  → Frozen
  → Deprecated
```

| Stage | Meaning |
|-------|---------|
| **Proposed** | Named in Registry; not funded for build |
| **Planned** | Scoped, prioritized, dependencies agreed |
| **Authoring** | Knowledge / decision content being written |
| **Golden Review** | Golden Cases + consulting quality review |
| **Integration** | Bundle / Narrative / Portal wiring in progress |
| **Production** | Live on customer Result / delivery path |
| **Frozen** | No content or behavior change without revision ticket |
| **Deprecated** | Removed from new sales; may remain for legacy runs |

---

## 3. Entry and exit criteria

### 3.1 Proposed → Planned

| Entry | Exit |
|-------|------|
| Registry row exists | Commercial value & priority set |
| Customer outcome stated | Dependencies listed |
| Product sponsor assigned | Target release slot on Roadmap |
| | Acceptance Standard checklist opened |

### 3.2 Planned → Authoring

| Entry | Exit |
|-------|------|
| Domain architecture available or scheduled | Required KU slots / decision ids listed |
| No Foundation / Wave 1.1 content changes required (or change RFC approved) | Authoring owners named |
| Ethics / commercial claims reviewed at outline level | Authoring kickoff recorded in Changelog (Planned note) |

### 3.3 Authoring → Golden Review

| Entry | Exit |
|-------|------|
| Required Knowledge Units authored & approved status | Golden Case set defined |
| No raw technical wording in commercial text | Cases executable offline or in harness |
| Capability allow-list candidates identified (doc) | Consulting quality scorecard started |

### 3.4 Golden Review → Integration

| Entry | Exit |
|-------|------|
| Golden Cases meet Acceptance Standard for content | Product signs Golden Review |
| Narrative targets mapped (Exec / Rec / Decision) | Integration ticket opened |
| Gaps logged (P0 blockers cleared) | Domain completion / acceptance docs linked |

### 3.5 Integration → Production

| Entry | Exit |
|-------|------|
| Production allow-list / adapter wiring complete | Module tests PASS |
| Narrative merge enrich-only (no Interpretation replace) | Portal verification on existing Result surfaces |
| Traceability KU → Bundle → Narrative → Portal | Release Notes written |
| Regression on Wave 1.1 / prior capabilities PASS | Registry Status → **Released**; Stage → **Production** |
| | Changelog entry with production date |

### 3.6 Production → Frozen

| Entry | Exit |
|-------|------|
| Capability stable in production | Freeze notice in Changelog |
| No open P0 customer defects for the capability | Stage → **Frozen**; further change requires Revision |

### 3.7 Any stage → Deprecated

| Entry | Exit |
|-------|------|
| Product decision to retire or replace | Customer migration note |
| Replacement capability identified (or explicit none) | Registry Status → **Deprecated** |
| Rollback / dual-run plan if needed | Sales / Portal no longer promote capability |

---

## 4. Rollback policy

### 4.1 When to rollback

- P0 customer harm (misleading commercial claim, ethics breach, technical wording leak)  
- Golden Case regression on a released capability  
- Production wiring breaks Wave 1.1 or prior Released capabilities  
- Traceability broken (statements without KU provenance)

### 4.2 Rollback actions (product + engineering)

1. **Disable** capability on production allow-list / feature gate (prefer capability-scoped disable).  
2. **Do not** delete Knowledge Units or Golden Cases to “fix” history.  
3. Revert Registry Status to **Integration** or **Golden Review** as appropriate.  
4. Log rollback in `06_PRODUCT_CHANGELOG.md` with date, reason, operator.  
5. Re-enter Acceptance Standard before returning to Production.

### 4.3 What rollback must not do

- Rewrite Golden Dataset expected outputs to force green  
- Modify Foundation or Wave 1.1 frozen content as a shortcut  
- Ship a partial capability as Production without Acceptance Pass  

---

## 5. Versioning

| Change type | Version bump |
|-------------|--------------|
| New capability first production | `1.0.0` |
| Customer-visible enrichment within same capability | `1.x.0` (minor) |
| Copy / binding fix without meaning change | `1.x.y` (patch) |
| Breaking change to customer outcome model | New major (`2.0.0`) + Product approval |

Registry Version field always reflects the **capability** semver, not the platform monorepo tag.

---

## 6. Governance

| Role | Responsibility |
|------|----------------|
| Product Owner | Stage transitions; Roadmap; customer outcome |
| Domain / Knowledge | Authoring quality; KU approval |
| Engineering | Integration; tests; rollback switches |
| Review | Golden Review + Acceptance Standard sign-off |

No capability enters **Production** without Product Owner sign-off recorded in Changelog.

---

## 7. Stop line

Release Policy is in force. Next capability (Promotion Readiness) remains **Proposed** until Product approval.

---

END
