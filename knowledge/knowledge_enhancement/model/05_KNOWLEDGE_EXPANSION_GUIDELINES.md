# 05 — Knowledge Expansion Guidelines

Version: 1.0  
Status: **SPRINT A — Commercial Knowledge Architecture**  
Date: 2026-08-08  
Depends on: `00`–`04`  
Authority: Official principles for all future commercial knowledge population  

---

## 1. Purpose

Define the **official rules** for expanding BTE commercial knowledge after architecture review.

These guidelines apply to:

- `database/20_knowledge` population (future)  
- Commercial evidence / sentence units  
- BaZi consultation domain content  
- Any corpus that feeds Interpretation → Narrative advisory text  

They do **not** authorize implementation in this sprint.

---

## 2. Core principles (mandatory)

### 2.1 Knowledge must answer real consultation questions

| Rule | Detail |
|------|--------|
| Requirement | Every unit maps to ≥1 question in a Consultation Domain (`01`) |
| Test | “Which client question does this answer?” must be non-empty |
| Reject | Encyclopedic trivia with no advisory use |

### 2.2 Knowledge must not duplicate Rule Database

| Rule | Detail |
|------|--------|
| Requirement | No re-stating weights, thresholds, or match tables as “knowledge” |
| Allowed | Explain *meaning* of a signal the rules already fire |
| Reject | Copying CSV score rows into commercial corpus |
| SSOT | Rules calculate; Knowledge advises |

### 2.3 Knowledge must be explainable

| Rule | Detail |
|------|--------|
| Requirement | Consultant-facing language; classical optional + modern interpretation |
| Reject | Engine jargon (“kích hoạt khi”, matched_rule dumps) |
| Voice | Consultant, not calculator (Brand / Content Quality) |

### 2.4 Knowledge must be traceable

| Rule | Detail |
|------|--------|
| Requirement | `knowledge_id` → evidence → Interpretation → Narrative component |
| Require | `signal_condition` + `trace_refs` (analytical signal and/or REF-*) |
| Reject | Orphan advice with no binding condition |

### 2.5 Knowledge must be reusable

| Rule | Detail |
|------|--------|
| Requirement | Usable by Narrative, Portal (via NarrativeResult), future Report, future Expert |
| Reject | UI-only hard-coded strings as the only copy of advice |
| Prefer | One unit → many consumers |

### 2.6 Knowledge must be commercially valuable

| Rule | Detail |
|------|--------|
| Requirement | Improves Exec / Rec / Warning / Impact quality or domain depth |
| Align | Epic 1 P0/P1 before P2 encyclopedic expansion |
| Reject | Low-frequency esoterica before core Action/Risk/Mitigation coverage |

### 2.7 Knowledge must never contradict analytical meaning

| Rule | Detail |
|------|--------|
| Requirement | Advisory text must be consistent with AnalysisResult signals |
| Forbid | Claiming “thân vượng” guidance when strength signal is weak (unless special pattern rules apply and are cited) |
| Conflict | If classical quote conflicts with engine signal → do not emit; escalate Academic / Architecture review |

---

## 3. Additional operating rules

| ID | Rule |
|----|------|
| XR-1 | Author **Risk** and **Mitigation** as pairs for material cautions (CQ-5) |
| XR-2 | **Action** units must be specific and chart-bound (CQ-4) |
| XR-3 | Sensitive domains (Marriage, Children, Health) require `ethics_flags` and approved templates |
| XR-4 | Health knowledge is lifestyle-only — never diagnosis or treatment |
| XR-5 | Prefer additive rows; never rename/delete Rule DB columns to “make knowledge fit” |
| XR-6 | Do not mutate Golden Dataset / snapshots to force narrative richness |
| XR-7 | Draft → Review → Official per existing governance; no silent Official promotion |
| XR-8 | Every Official unit declares `kind` + `consultation_domain` + `evidence_kind` |
| XR-9 | Empty is better than filler — respect approved insufficient Narrative behavior |
| XR-10 | Expansion follows Sprint A model; new kinds/domains require model amendment |

---

## 4. Authoring checklist (per unit)

Before accepting a commercial knowledge unit:

- [ ] Answers a real consultation question (`01`)  
- [ ] Declares commercial `kind` (`02`)  
- [ ] Declares `consultation_domain`  
- [ ] Declares Pack 05 `evidence_kind`  
- [ ] Has `signal_condition` tied to analytical meaning  
- [ ] Does not duplicate Rule Database  
- [ ] Explainable / non-technical  
- [ ] Trace refs present (signal and/or REF-*)  
- [ ] Commercially valuable for Narrative or domain depth  
- [ ] No contradiction with analytical meaning  
- [ ] Ethics flags set when needed  
- [ ] Reusable (not UI-only)  

---

## 5. Expansion order (model-aligned)

Follow Epic 1 priorities unless review amends:

| Phase | Expand first |
|-------|----------------|
| P0 | Analytical explanations; Action; Risk+Mitigation; core Identity; `20_knowledge` seeds (FE, Ten Gods, Useful God, Strength, Patterns) |
| P1 | Luck guidance; Career/Finance consultation; Canon integrity; curated Shensha cautions |
| P2 | Sensitive domains; Parents/Education; Transformations; academic depth |

**Do not** expand all consultation domains equally before P0 evidence kinds are healthy.

---

## 6. Format & storage (blueprint only)

Sprint A does not choose a single physical store exclusively, but future epics must:

1. Map physical rows → logical Commercial Knowledge Unit (`02` §5).  
2. Declare which store is SSOT for each kind.  
3. Avoid parallel advice corpora in Portal i18n / Report templates.  

Candidate stores (unchanged physically in this sprint):

| Candidate | Likely role |
|-----------|-------------|
| `database/20_knowledge` | Explainable classical + modern corpus |
| Pack 04 / evidence libraries | Runtime-selectable commercial sentences |
| BaZi module records | Academic depth aligned to domains |

---

## 7. Contradiction & conflict handling

| Case | Resolution |
|------|------------|
| Two knowledge units, same signal, conflicting advice | Higher priority Official wins; document related ids |
| Knowledge vs Analysis signal | Analysis fact wins; knowledge must not emit |
| Knowledge vs Brand/Ethics | Ethics wins; revise or withhold |
| Knowledge vs Foundation layout | Foundation wins for presentation; knowledge stays content-only |

---

## 8. Definition of done (future content epic)

A knowledge expansion epic is done when:

1. Units pass the checklist (§4).  
2. Traceability to Narrative components is documented for samples.  
3. No Rule Database duplication introduced.  
4. Governance review recorded.  
5. Coverage metrics updated (re-audit subset).  
6. **Still no unauthorized engine/architecture changes.**  

---

## 9. Stop line

Expansion guidelines complete.  

**Sprint A complete.**  
Do **not** create knowledge records until architecture review approves this model package.

---

END
