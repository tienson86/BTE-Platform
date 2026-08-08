# 15 — Knowledge Authoring Standard

Version: 1.0  
Status: **SPRINT C — Knowledge Unit Model**  
Date: 2026-08-08  
Depends on: `05`, `11`–`14`, Sprint B `10`  
Authority: Official standard for creating Knowledge Units (future content epics)  

---

## 1. Purpose

Define how authors create Knowledge Units so every unit is:

- commercially useful  
- reusable  
- traceable  
- explainable  
- non-duplicative of Rule Database  
- supportive of Narrative  
- independent of rendering technology  

**This sprint does not authorize writing production units.**

---

## 2. Mandatory unit principles

Every Knowledge Unit must:

| # | Rule |
|---|------|
| 1 | Answer a **real consultation problem** (`primary_intent`) |
| 2 | Be **commercially useful** (improves Exec / Rec / Warning / Impact / decision posture) |
| 3 | Avoid **academic repetition** without advisory value |
| 4 | **Never duplicate Rule Database** (no thresholds/weights/match tables) |
| 5 | **Never contradict** Analysis / Interpretation meaning |
| 6 | **Support Narrative** (declare components + evidence_kind) |
| 7 | Remain **reusable** (not one-off UI copy) |
| 8 | Remain **traceable** (signals / REF / ids) |
| 9 | Remain **explainable** (consultant language) |

Also inherit `05_KNOWLEDGE_EXPANSION_GUIDELINES.md` and scenario rules in `10`.

---

## 3. Writing principles

| Principle | Guidance |
|-----------|----------|
| Customer first | Write to the question, not the CSV folder |
| One intent | One primary_intent per unit |
| Specific actions | Chart-bound; avoid “try harder” |
| Calm risks | No doom, curse, or absolute fate |
| Pair mitigations | Material Risk KUs need Mitigation path |
| Honest emptiness | Prefer no unit over filler |
| Consultant voice | Brand: consultant, not calculator |
| Locale | Commercial VI for customer-facing `body` |
| Ethics | Sensitive domains use flags + approved patterns |
| Non-medical | Health units are lifestyle-only |
| No guarantees | Finance/investment: no promised returns |
| Render-agnostic | No CSS, card names, or Report layout in body |

---

## 4. Naming convention

### 4.1 Knowledge Unit ID

```
KU-{KIND}-{DOMAIN}-{SEQ}
```

Examples (illustrative):

- `KU-AN-ID-000001` — Analytical / Identity  
- `KU-AC-CA-000014` — Action / Career  
- `KU-RK-FI-000003` — Risk / Finance  
- `KU-MT-FI-000003` — Mitigation paired family for finance risk  

| Segment | Meaning |
|---------|---------|
| `KU` | Knowledge Unit |
| `KIND` | Short code: AN, CN, PG, AC, RK, MT, ST, OP (Analytical, Consultation, Practical Guidance, Action, Risk, Mitigation, Strategy, Opportunity) |
| `DOMAIN` | CK short: ID, PE, CA, BU, … or `XX` for multi/structural |
| `SEQ` | Zero-padded sequence; never reuse |

IDs are immutable after first Draft reservation.

### 4.2 Title

- Internal, concise, English or VI consistently per team convention  
- Not a marketing headline  
- Include posture/category when helpful: `Career Change — Wait under suppressed useful god`

---

## 5. Authoring workflow

```
1. Identify consultation problem / scenario
        ↓
2. Search existing Published/Approved KUs (reuse)
        ↓
3. Choose kind + domain + evidence_kind
        ↓
4. Draft fields per schema `12`
        ↓
5. Self-check against §6 checklist
        ↓
6. Submit lifecycle: Technical → Knowledge → Commercial
        ↓
7. Approved → Published (release)
```

**Do not** invent signals. Bind `applicable_conditions` to Analysis meanings that already exist or are scheduled.

---

## 6. Review checklist (author + reviewers)

- [ ] Real consultation problem stated  
- [ ] Commercially useful for declared primary_usage  
- [ ] Not academic filler  
- [ ] No Rule Database duplication  
- [ ] No contradiction with analytical meaning  
- [ ] `evidence_kind` + Narrative components declared  
- [ ] `applicable_conditions` present and testable  
- [ ] Trace refs (signal and/or REF-*) present  
- [ ] Primary usage set; secondary usage considered  
- [ ] Ethics flags set if needed  
- [ ] Risk has Mitigation pairing path if material  
- [ ] Action specific; posture set if decision-related  
- [ ] Granularity atomic; reusable  
- [ ] Render-independent  
- [ ] Naming/id valid  
- [ ] Version + author_notes adequate  

---

## 7. Approval workflow

Follows `14_KNOWLEDGE_LIFECYCLE.md`:

| Gate | Must pass |
|------|-----------|
| Technical Review | Structure, schema, no rule duplication |
| Knowledge Review | BaZi meaning & ethics correctness |
| Commercial Review | Customer value & Narrative fit |
| Approved | Release candidate |
| Published | Production eligibility |

Scenario approval (`10`) ≠ KU approval.  
KU approval ≠ automatic database file creation without a content epic.

---

## 8. Versioning

| Change type | Version bump | Review path |
|-------------|--------------|-------------|
| Typo / formatting only | Patch | Fast-track if Technical confirms no semantic change |
| Wording clarity, same meaning | Patch/Minor | Commercial at minimum |
| Condition / advice / ethics change | Minor/Major | Full review path |
| Kind / evidence_kind / primary intent change | Major | Full review; consider new id if reuse breaks traces |
| Deprecation | — | Architect approval; `superseded_by` if any |

Published traces should record `knowledge_unit_id` + `version`.

---

## 9. Maintenance rules

| Rule | Detail |
|------|--------|
| M1 | Prefer revise + supersede over silent edit of Published meaning |
| M2 | Never delete Published history needed for audit |
| M3 | On Analysis signal rename, update conditions via Revised units — do not patch Rule DB from KU work |
| M4 | Periodic reuse audit: merge duplicates |
| M5 | When Scenario profile changes, re-validate dependent KUs |
| M6 | Orphan KUs (no scenario/domain use) → revise affinity or deprecate |
| M7 | Content quality regressions (G6/CQ) drive P0 authoring, not engine hacks |

---

## 10. Relationship to physical population (future)

When a later epic populates stores:

1. Map every row → logical schema `12`  
2. Only Published units enter production retrieval  
3. Prefer additive rows; stable ids  
4. Do not rename Rule Database columns to fit KU text  

Sprint C establishes the **foundation**; it does not populate `database/20_knowledge`.

---

## 11. Anti-patterns

| Anti-pattern | Why forbidden |
|--------------|---------------|
| KU = full NarrativeResult | Not atomic |
| KU = score threshold table | Rule duplication |
| KU only in Portal i18n | Breaks SSOT |
| KU without conditions | Untestable / untraceable |
| KU invents medical/legal claims | Ethics |
| KU adds Pack 05 sections | Architecture freeze |

---

## 12. Stop line

Authoring standard complete.

**Sprint C complete.**  
Do **not** populate `database/20_knowledge`.  
Do **not** create Knowledge Records / Units.  
Wait for architecture review.

---

END
