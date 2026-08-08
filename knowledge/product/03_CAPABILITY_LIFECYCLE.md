# 03 — Capability Lifecycle

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  
Depends on: `01_CAPABILITY_REGISTRY.md`, `02_CAPABILITY_RELEASE_POLICY.md`  

---

## 1. Purpose

Document the full lifecycle of a BTE commercial capability — from idea to retirement.

Release Policy stages are the **governance gates**.  
Lifecycle phases are the **work sequence** Product and Domain teams follow.

---

## 2. Lifecycle diagram

```
Idea
  ↓
Architecture
  ↓
Knowledge
  ↓
Golden Cases
  ↓
Integration
  ↓
Release
  ↓
Freeze
  ↓
Maintenance
  ↓
Revision
  ↓
Retirement
```

---

## 3. Phase definitions

### 3.1 Idea

- Customer problem and commercial value articulated  
- Candidate Registry ID proposed  
- Mapped tentatively to a Domain (or “new Domain required”)  
- Outcome: Registry row Status = **Proposed**

### 3.2 Architecture

- Domain architecture / decision model / consultation questions ready or scheduled  
- Capability boundaries and non-goals written  
- Dependencies on Wave 1.1 and other capabilities listed  
- Outcome: Stage may move to **Planned**

### 3.3 Knowledge

- Required Knowledge Unit slots defined  
- Units authored, reviewed, approved  
- Commercial wording only (no technical engine leakage)  
- Outcome: Stage = **Authoring** → ready for Golden Review

### 3.4 Golden Cases

- Official Golden Case set for the capability  
- Pass/fail against consulting quality + acceptance checklist  
- Gaps logged; P0 blockers cleared  
- Outcome: Stage = **Golden Review** complete

### 3.5 Integration

- Allow-list / Bundle / Narrative merge / Portal delivery wiring  
- Traceability: Knowledge Unit → Bundle → Narrative → Portal  
- Module tests + regression  
- Outcome: Stage = **Integration** complete

### 3.6 Release

- Production enablement  
- Release Notes + Changelog entry  
- Registry: Status **Released**, Stage **Production**, Production **Yes**  
- Outcome: Customer-visible capability live

### 3.7 Freeze

- Behavior and content locked  
- Changes require explicit Revision  
- Outcome: Stage **Frozen**

### 3.8 Maintenance

- Monitor defects, consulting quality, ethics flags  
- Patch releases (`1.x.y`) for non-breaking fixes only  
- No silent expansion of scope

### 3.9 Revision

- Planned minor/major improvement under Release Policy  
- Re-run Acceptance Standard for changed surfaces  
- Update Registry Version + Changelog

### 3.10 Retirement

- Capability Deprecated or replaced  
- Sales/Portal stop promoting  
- Historical runs may remain for audit; new customers directed to successor

---

## 4. Mapping lifecycle ↔ release stages

| Lifecycle phase | Typical release stage |
|-----------------|----------------------|
| Idea | Proposed |
| Architecture | Planned |
| Knowledge | Authoring |
| Golden Cases | Golden Review |
| Integration | Integration |
| Release | Production |
| Freeze | Frozen |
| Maintenance | Production or Frozen |
| Revision | Authoring → … → Production (cycle) |
| Retirement | Deprecated |

---

## 5. Reference path (Career Selection Assessment)

| Phase | Evidence |
|-------|----------|
| Idea / Architecture | Domain 01 packs `01`–`13` |
| Knowledge | `22_domain01_career_business.csv` SEL units |
| Golden Cases | Domain `15`, `18`; production `22_PRODUCTION_VALIDATION` |
| Integration / Release | Domain `20`–`23`; Registry CAP-CAREER-SEL-001 v1.0.0 |
| Freeze | Pending Product freeze notice after review window |
| Next | Maintenance only — **not** Promotion Readiness |

---

## 6. Stop line

Lifecycle is normative for all future capabilities.  

**Do not start Promotion Readiness lifecycle without Product approval.**

---

END
