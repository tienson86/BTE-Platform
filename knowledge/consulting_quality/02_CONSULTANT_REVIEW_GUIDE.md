# 02 — Consultant Review Guide

Version: 1.0  
Status: **OFFICIAL — Consultant Review Guide**  
Date: 2026-08-08  
Depends on: `01_CONSULTING_QUALITY_FRAMEWORK.md`  
Scope: Documentation only — human review procedure  

---

## 1. Purpose

Tell a human reviewer **how** to evaluate Executive Summary, Recommendation, Warning, and Narrative for consulting quality.

Use with Scorecard (`04`) and Case Review Workflow (`03`).

---

## 2. Review posture

1. Read as a **paying customer**, then as a **senior consultant**.  
2. Do not re-run engines or redesign Narrative.  
3. Judge the **merged** output (Analysis + Interpretation + Wave 1.1 Commercial Knowledge).  
4. Prefer evidence-backed defects over taste preferences.  
5. Separate: *analytical bug* (escalate to engineering) vs *consulting quality defect* (revision / knowledge / merge guidance).

---

## 3. Executive Summary

### 3.1 What to look for

| Check | Pass signal |
|-------|-------------|
| Identity | Customer knows “who I am in this chart” in consultant language |
| Strength / weakness honesty | Favorable cases name real supports; weak/enemy cases name limits calmly |
| Useful-god frame | Priority direction is understandable without jargon dump |
| Hierarchy | Identity → supports/cautions → priority, not a flat list of fields |
| Enrichment | When Wave 1.1 applies, prose is advisory — not a calculator echo |

### 3.2 Common defects

| Defect | Example symptom |
|--------|-----------------|
| Label dump | “Nhật chủ: X. Cách cục: Y.” as the entire identity |
| Invented strength | Strength language when signals are weak / absent |
| Missing weakness when due | Enemy/weak signals present but Exec silent or soft-washed incorrectly |
| Technical leak | “kích hoạt”, “matched rules”, mock/placeholder residue |
| Overclaim | Guarantees, medical/legal destiny language |
| Incoherent with Rec | Exec priority contradicts Recommendation action |

### 3.3 Improvement guidance

- Prefer Wave 1.1 Identity / Strength / Weakness / Useful God cores when conditions match.  
- Keep analytical tokens only as bind inputs — not as customer-facing labels.  
- If data insufficient, say so calmly; do not invent Wave 1.2 depth.  
- Align Exec priority wording with Recommendation action.

---

## 4. Recommendation

### 4.1 What to look for

| Check | Pass signal |
|-------|-------------|
| One primary action | Clear priority for the near term |
| Reason | Tied to Dụng thần / structure (e.g. KU-UG / KU-RC path) |
| Next step | Concrete enough for “this week / next 2–4 weeks” |
| Scope honesty | No guaranteed returns; prepare posture when appropriate |
| Trace | Knowledge / interpretation refs present when commercial enrichment used |

### 4.2 Common defects

| Defect | Example symptom |
|--------|-----------------|
| Token-only action | Action is just “Thủy” or a single god token |
| Empty reason | Action without why |
| Multi-priority noise | Three equal “must do now” items |
| Contradicts useful god | Advises against stated Dụng thần without explanation |
| Overwrite of Analysis | Changes scores/grades/meaning (must never happen) |
| Duplicate advice | Same sentence repeated in Exec and Rec without lift |

### 4.3 Improvement guidance

- Require Action / Reason / Next-step shape for commercial cases.  
- Keep analytical codes in provenance side-channels; customer text should be prose.  
- Soften or defer when weakness signals require reduce-load-first posture.  
- Do not demand units outside Wave 1.1 allow-list.

---

## 5. Warning

### 5.1 What to look for

| Check | Pass signal |
|-------|-------------|
| Trigger honesty | Warning appears when risk/weakness evidence exists |
| Tone | Careful, specific, non-shaming |
| Link to action | Points toward safer posture or deferral, not panic |
| Consistency | Matches Exec weakness / Recommendation load-reduction when relevant |

### 5.2 Common defects

| Defect | Example symptom |
|--------|-----------------|
| Fear marketing | Catastrophic language without evidence |
| Silent risk | Clear enemy/clash/weak signals, no caution |
| Generic filler | “Cần cẩn thận” with no chart binding |
| Blame | Personality insult or moral failure framing |

### 5.3 Improvement guidance

- Prefer calm constraint language (“giữ mực / giảm tải”) over doom.  
- If Wave 1.1 Weakness Core applies, use it; otherwise mark insufficient rather than invent.  
- Never invent medical, legal, or financial guarantees.

---

## 6. Narrative (full arc)

### 6.1 What to look for

| Check | Pass signal |
|-------|-------------|
| Arc coherence | Observation → reasoning → impact → recommendation → caution → conclusion feel like one consultation |
| No contradiction | Same identity and useful-god story throughout |
| Commercial lift | Where Wave 1.1 enriches, customer text improves vs analysis echo |
| Insufficient honesty | Thin slots flagged rather than padded with fiction |

### 6.2 Common defects

| Defect | Example symptom |
|--------|-----------------|
| Fragmented voice | Calculator observation next to consultant prose with no bridge |
| Orphan enrichment | Commercial sections appended but Exec/Rec ignore them |
| Empty commercial slots with false certainty | Status complete language while critical slots empty |
| Provenance loss | No way for reviewer to see which KU supported a claim |

### 6.3 Improvement guidance

- Review Exec and Rec first; then scan Narrative for contradictions.  
- Use Commercial Knowledge Bundle / knowledge_refs to verify claims.  
- Escalate engine bugs separately from consulting copy issues.

---

## 7. Defect severity (for revision tickets)

| Severity | Meaning | Typical exit |
|----------|---------|--------------|
| **Blocker** | Accuracy failure, ethics breach, inventing facts, guarantee claims | Must fix before any approval |
| **Major** | Unusable Rec, naturalness failure (label dump), consistency break Exec↔Rec | Must fix for commercial case set |
| **Minor** | Style polish, slight verbosity, band-token romanization | May accept with noted follow-up |
| **Observation** | Future Wave 1.2 gap, UI surfacing, non-blocking | Record only |

---

## 8. Reviewer checklist (quick)

- [ ] Accurate to Analysis for this case  
- [ ] Consultant voice (not calculator)  
- [ ] Exec readable and hierarchical  
- [ ] Rec actionable with reason  
- [ ] Warning honest and calm when due  
- [ ] Consistent across surfaces  
- [ ] No technical leak / no invented knowledge beyond Wave 1.1  
- [ ] Scorecard completed (`04`)  

---

## 9. Stop line

Review guide complete. Workflow and exit criteria: `03`. Scoring: `04`. Release bar: `05`.

---

END
