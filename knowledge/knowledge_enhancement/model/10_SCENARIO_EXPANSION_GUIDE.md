# 10 — Scenario Expansion Guide

Version: 1.0  
Status: **SPRINT B — Consultation Scenario Model**  
Date: 2026-08-08  
Depends on: `05_KNOWLEDGE_EXPANSION_GUIDELINES.md`, `06`–`09`  
Authority: Official rules for adding future consultation scenarios  

---

## 1. Purpose

Govern how new **scenarios** and **decisions** enter the BTE catalog without breaking:

- Commercial Knowledge SSOT  
- Frozen Narrative grammar  
- Traceability  
- Reuse across Narrative, Report, and future AI assistants  

---

## 2. What may be expanded

| Expandable | Not expandable via this guide |
|------------|-------------------------------|
| New `CS-*` scenarios | Pack 05 component list |
| New `DS-*` decisions | Rule Database schemas |
| Scenario↔domain/kind profiles | Foundation / Design System |
| Retrieval profile notes | Engine architecture |

Scenarios are **entry points**. They must not become a second knowledge corpus.

---

## 3. Mandatory principles for future scenarios

Future scenarios must:

| # | Rule |
|---|------|
| 1 | **Answer real consultation questions** — customer intent first |
| 2 | **Reuse existing knowledge** — map to CK-* domains and commercial kinds before inventing new domains |
| 3 | **Avoid duplication** — no parallel scenario that only renames an existing CS-* |
| 4 | **Remain traceable** — scenario → knowledge → evidence → Narrative component |
| 5 | **Support Narrative** — declare expected Pack 05 components |
| 6 | **Support Report** — same NarrativeResult SSOT; no report-only advice |
| 7 | **Support future AI assistants** — scenario id + profile must be machine-selectable |

Also inherit Sprint A expansion rules (`05`): no Rule DB duplication; explainable; commercially valuable; no analytical contradiction.

---

## 4. Authoring workflow

```
1. Capture customer question
        ↓
2. Check existing CS-*/DS-* (reuse or specialize)
        ↓
3. Draft scenario card (template §5)
        ↓
4. Map Required/Optional/Conditional domains & kinds
        ↓
5. Map evidence + Narrative components
        ↓
6. Identify reusable Commercial Knowledge gaps (content backlog)
        ↓
7. Submit for review
```

**Authoring rule:** Write the scenario card **before** writing new knowledge records.  
If existing knowledge can serve the scenario, prefer reuse.

---

## 5. Scenario card template (required)

```text
scenario_id: CS-____
title:
customer_intent:
typical_questions: []
expected_outcome:
primary_domains: []      # CK-*
optional_domains: []
conditional_domains: []
required_kinds: []       # commercial kinds
optional_kinds: []
conditional_kinds: []
required_evidence: []
interpretation_focus: []
narrative_components_required: []
narrative_components_conditional: []
ethics_flags: []
linked_decisions: []     # DS-* if any
reuses_scenarios: []     # parent/related CS-*
knowledge_gaps: []       # backlog only — not invented filler
version:
status: draft|review|approved|deprecated
```

Decision cards (`DS-*`) additionally require fields from `08` (risk/opportunity/mitigation/action/success indicators).

---

## 6. Review workflow

| Step | Owner | Checks |
|------|-------|--------|
| Peer review | Knowledge author peer | Customer-first; not academic folder rename |
| Model review | Knowledge architect | Fits `06`–`09`; no Narrative grammar change |
| Ethics review | Required if MA/CH/HE/PA or similar | Flags, disclaimers, tone |
| Commercial review | Product | Tier (T0–T3), priority vs P0 evidence backlog |

Review rejects if:

- Organized by Five Elements / Ten Gods as the scenario itself  
- Requires new Narrative sections  
- Duplicates an existing scenario without specialization rationale  
- Cannot name Required Commercial Knowledge kinds  
- Encourages invented claims when knowledge missing  

---

## 7. Approval workflow

| Status | Meaning |
|--------|---------|
| `draft` | Authoring |
| `review` | Submitted |
| `approved` | Catalog official; may appear in product scenario lists |
| `deprecated` | Superseded; keep id for trace |

Approval artifacts:

1. Scenario card merged into `06` catalog (or appendix register in future)  
2. Relationship rows added to `07`  
3. If decision: entry in `08`  
4. Retrieval notes updated in `09` if priority exceptions exist  
5. Content backlog tickets for missing Commercial Knowledge (separate epic)

**Approval of a scenario ≠ approval to populate database.** Content remains a gated content epic.

---

## 8. Versioning strategy

| Object | Versioning |
|--------|------------|
| Scenario id (`CS-*`) | Stable forever once approved; never reuse ids |
| Scenario card | `version` semver within doc/register; breaking profile changes bump major |
| Deprecated scenarios | Remain resolvable for old traces; hidden from new UX |
| Model docs `06`–`10` | Document version in header; Sprint amendments logged |
| Commercial Knowledge units | Independent versioning per `05` / governance |

Breaking change examples (require major + review):

- Removing a Required kind from a live T0 scenario  
- Changing ethics posture  
- Splitting/merging scenarios that affect production traces  

Additive optional domains/kinds = minor.

---

## 9. Specialization vs new scenario

| Prefer specialize | Prefer new CS-* |
|-------------------|-----------------|
| Same intent, tighter decision (Career → Career Change already exists) | Genuinely new customer job-to-be-done |
| Adds only decision overlay | Cross-domain intent not covered |
| Marketing synonym only | — reject; use alias on existing |

Aliases (e.g. “đổi nghề” → CS-CC) belong in product UX mapping, not duplicate scenarios.

---

## 10. Support matrix for multi-channel

Every approved scenario must declare support:

| Channel | Requirement |
|---------|-------------|
| Narrative / Result Page | Component profile defined |
| Report | Consumes same NarrativeResult; no extra advice store |
| Future AI assistant | Scenario id + retrieval profile selectable; answers use Commercial Knowledge SSOT |

If a scenario cannot support Narrative honestly (no feasible knowledge), keep as `draft` until content backlog exists — do not approve empty shells into production UX.

---

## 11. Expansion checklist

- [ ] Real customer question documented  
- [ ] Existing CS-*/DS-* searched for reuse  
- [ ] Scenario card complete  
- [ ] Domain/kind/evidence/narrative profiles set (req/opt/cond)  
- [ ] Ethics flags considered  
- [ ] Knowledge gaps listed as backlog (not fake units)  
- [ ] Peer + model (+ ethics if needed) review passed  
- [ ] Approval recorded; docs `06`–`09` updated as needed  
- [ ] No CSV/JSON/runtime sneaked into “scenario expansion”  

---

## 12. Stop line

Scenario Expansion Guide complete.

**Sprint B complete.**  
Do **not** create knowledge records.  
Do **not** implement retrieval logic.  
Wait for architecture review.

---

END
