# 14 — Domain 01 Implementation Report (P0)

Version: 1.0  
Status: **DOMAIN 01 · SPRINT B — P0 Knowledge Authoring COMPLETE**  
Date: 2026-08-08  
Depends on: Sprint A / A.5 frozen · Wave 1.1 frozen · Golden Knowledge Standard  
Scope: Author P0 units only — **no P1/P2 · no Wave 1.1 edits · no runtime**  

---

## 1. Summary

Domain 01 Career & Business P0 Knowledge Units are authored in:

`database/20_knowledge/22_domain01_career_business.csv`

| Metric | Value |
|--------|------:|
| New units | **4** |
| P1 / P2 units | **0** |
| Wave 1.1 rows modified | **0** |
| Runtime / Narrative / Portal changes | **0** |

Offline Golden Case validation (merged corpus, eval-only) shows career Rec specializes beyond Wave 1.1 generic action when Domain 01 P0 is allow-listed.

**Production note:** Default Adapter still loads Wave 1.1 allow-list + `21_*.csv` only. Wiring `22_*.csv` + Domain allow-list is a **Product/engineering follow-up** (explicitly out of this sprint’s strict rules). Content is ready.

---

## 2. P0 units authored (approved matrix)

| Id | Title | Capability | Kind | evidence_kind |
|----|-------|------------|------|---------------|
| KU-CN-CA-000001 | Career Work Direction | CAP-D1-CA-SEL | CN | career_direction |
| KU-AC-CA-000001 | Career Role-Fit Next Step | CAP-D1-CA-SEL · CAP-D1-CA-DEV | AC | action (priority 105) |
| KU-CN-LE-000001 | Leadership Style Light | CAP-D1-CA-LED | CN | leadership_style |
| KU-AC-BU-000001 | Employment vs Independent Posture | CAP-D1-BU-ENP | AC | business_posture |

Wave id: `W-D01-P0-CAREER` · Version `1.0.0` · Status `approved` (Publish/activation Product-owned).

---

## 3. Required fields coverage

Each row includes base Wave 1.1-compatible columns **plus** additive Domain fields:

| Required concept | Column / encoding |
|------------------|-------------------|
| ID | `knowledge_unit_id` |
| Version | `version` |
| Status | `review_status` |
| Capability | `capability_id` |
| Domain | `domain` |
| Scenario | `scenarios` |
| Conditions | `condition` |
| Evidence | `evidence_kind` · `required_evidence` · `signal_refs` |
| Interpretation | `required_interpretation` |
| Narrative Targets | `narrative_targets` |
| Executive Summary Support | `executive_summary_support` |
| Recommendation Support | `recommendation_support` |
| Decision Support | `decision_support` · `decision_ids` |
| Commercial Value | `commercial_value` |
| Traceability | `traceability` |

---

## 4. Quality controls applied

| Standard | Applied |
|----------|---------|
| Golden Knowledge Standard | Correct / commercial / actionable / professional / natural |
| Wave 1.1 writing style | Consultant Vietnamese; placeholder bind; mitigate-first awareness |
| No technical leakage | No `vuong`/`nhuoc`/engine crumbs in authored prose |
| Ethics | `no_guaranteed_returns` on action units; no job-title prophecy |
| Pairing | CN-CA ↔ AC-CA; LE/BU reference UG |

---

## 5. Explicit non-work

| Not done | Why |
|----------|-----|
| P1 change/promote/founder deep packs | Out of sprint |
| Modify `21_knowledge_units.csv` | Wave 1.1 frozen |
| Adapter / allow-list / multi-CSV loader | No runtime |
| Capability HTTP API | Design only (Sprint A.5) |

---

## 6. Files touched

```
database/20_knowledge/22_domain01_career_business.csv   (new)
database/20_knowledge/README.md
database/20_knowledge/CHANGELOG.md
knowledge/domains/domain_01_career_business/14–16
knowledge/domains/domain_01_career_business/00_DOMAIN_INDEX.md
```

---

## 7. Stop line

P0 authoring complete. Results → `15`. Gaps → `16`.  
**Wait for Product Review before P1 authoring or production wiring.**

---

END
