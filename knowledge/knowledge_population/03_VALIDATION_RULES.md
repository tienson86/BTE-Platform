# 03 — Validation Rules

Version: 1.0  
Status: **EPIC 3 · SPRINT A — Population Framework**  
Date: 2026-08-08  
Depends on: `01`, `02`, EPIC 2 `12`/`15`/`18`/`19`  

---

## 1. Purpose

Define **validation rules** and **quality gates** for Knowledge Population.

Validation answers: *Is this unit allowed to proceed / publish?*  
It does not author content and does not run engines in this sprint.

---

## 2. Validation layers

| Layer | When | Focus |
|-------|------|-------|
| L1 Schema | Draft + Technical | Fields, enums, ids |
| L2 Integrity | Technical + Publish | Pairs, refs, supersession |
| L3 Meaning | Knowledge | Analytical non-contradiction, ethics |
| L4 Commercial | Commercial | Value, voice, priority |
| L5 Narrative | Narrative | Evidence/component/CQ fit |
| L6 Wave / Suite | Wave exit | Catalog coverage + sample outcomes |

---

## 3. Hard fail rules (block Publish)

| ID | Rule |
|----|------|
| HF-01 | Missing `knowledge_unit_id` or id not in catalog / not Architect-approved amendment |
| HF-02 | Missing required schema fields for Published (`12` §12) |
| HF-03 | Duplicates Rule Database thresholds/weights/match logic |
| HF-04 | Contradicts Analysis meaning for stated conditions |
| HF-05 | Kind=RK without Published-or-co-batched MT pair path |
| HF-06 | Medical diagnosis / treatment claims |
| HF-07 | Guaranteed financial returns / absolute fate language |
| HF-08 | Empty or technical-only body that Narrative would filter to nothing |
| HF-09 | Missing `evidence_kind` or `supported_narrative_components` |
| HF-10 | `primary_usage` empty |
| HF-11 | Ethics-gated domain without `ethics_flags` |
| HF-12 | Attempt to Publish while any review stage is Fail/pending |

---

## 4. Soft fail rules (must fix before Approve; may Draft)

| ID | Rule |
|----|------|
| SF-01 | Weak Action specificity (“try harder”) |
| SF-02 | Opportunity without clear signal binding |
| SF-03 | Academic quote without modern advisory use |
| SF-04 | Over-broad conditions (always true) |
| SF-05 | Missing secondary_usage (recommended) |
| SF-06 | Title/summary not descriptive for search/reuse |
| SF-07 | Confidence_requirement unset |
| SF-08 | Scenario affinity empty when unit is scenario-specific |

---

## 5. Author self-check checklist

Before submit:

- [ ] Catalog row matched; intent title honored  
- [ ] Real consultation problem stated  
- [ ] Schema required fields filled  
- [ ] Conditions bound to real signals  
- [ ] No Rule DB duplication  
- [ ] Body consultant VI; explainable  
- [ ] Evidence kind + Narrative components set  
- [ ] Primary usage set  
- [ ] Ethics flags if needed  
- [ ] RK/MT paired if Risk  
- [ ] Decision posture set if Action/Strategy decision-related  
- [ ] Trace refs present (signal and/or REF-*)  
- [ ] Version + draft status set  
- [ ] HF-* self-scan clean  

---

## 6. Quality gates (QG)

| Gate | Owner | Pass condition |
|------|-------|----------------|
| QG-Author | Author | §5 complete |
| QG-Tech | Technical Reviewer | L1+L2 + no HF from tech set |
| QG-Know | Knowledge Reviewer | L3 + no HF-04/06/07 |
| QG-Comm | Commercial Reviewer | L4 |
| QG-Narr | Narrative Reviewer | L5 |
| QG-Approve | Ops | All reviews Pass |
| QG-Publish | Ops | L2 pair integrity + manifest |
| QG-Wave | Wave lead | §8 wave checklist |

A unit may not skip gates. Fast-track typo path: see `04` (still records Technical confirmation).

---

## 7. Pair integrity validation

| Check | Rule |
|-------|------|
| Bidirectional ids | RK lists MT; MT lists RK |
| Same risk family | Categories align |
| Co-publish | Prefer same Publish batch |
| Orphan MT | Soft fail unless documented generic family template |
| Orphan RK | **Hard fail** HF-05 |

---

## 8. Wave / suite validation checklist

At wave exit (before declaring wave complete):

- [ ] All wave catalog ids Published (or explicitly deferred with Architect sign-off)  
- [ ] All RK in wave have MT Published  
- [ ] Minimum Narrative pack covered if Wave 1.x (`19` §7)  
- [ ] Scenario Required profiles for targeted CS-* satisfied (`18`)  
- [ ] Sample composition traces include KU ids (when runtime exists; until then, manual composition review against `13`)  
- [ ] No HF open  
- [ ] Content Quality spot-check on Exec/Rec/Warning samples  
- [ ] Re-audit note: insufficient rate expectation documented  

Until retrieval is implemented, wave exit uses **manual composition review** against frozen models — not engine code changes in population sprints.

---

## 9. Validation evidence to retain

| Artifact | Purpose |
|----------|---------|
| Review records (pass/fail/notes) | Audit |
| Self-check snapshot | Author accountability |
| Publish manifest (unit id + version + wave) | Production allow-list |
| Pair register updates | Warning integrity |
| Wave exit report | Phase progress |

Formats TBD in ops; content of evidence is mandatory.

---

## 10. Non-validation (explicit)

Validation does **not** include:

- Redesigning Narrative components  
- Editing Foundation tokens  
- Changing Score formulas to make units “fit”  
- Snapshot/Golden Dataset edits to force pass  

---

## 11. Stop line

Validation rules defined. No units validated (none created).

---

END
