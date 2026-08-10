# Expert Calibration Protocol

**Status:** DESIGN — operational process for future calibration rounds  
**Goal:** Avoid single-expert overfitting; produce adjudicated reference labels.

## Steps

### 1. Chart verification

- Confirm solar birth, timezone policy, location  
- Verify pillars against classical tiết khí SSOT (PILOT-1A lesson)  
- Record corrected chart if fixture diverges — **without silent Golden mutation**

### 2. Evidence inspection

- Produce Strength Evidence ledger + Profile snapshot  
- Mark DIRECT / DERIVED / CONTEXTUAL / INTERACTION  
- Flag NOT_EXPOSED producers

### 3. Independent expert classification

- ≥1 expert for clear cases; **≥2 for disputed/boundary**  
- Blinded to runtime taxonomy label where practical  
- Experts may see pillars + evidence summary, not forced runtime band

### 4. Rationale recording

Required fields:

```text
expert_id, case_id, label_v2, confidence, rationale,
key_strengthen_evidence[], key_weaken_evidence[],
disputed_points[]
```

### 5. Disagreement resolution

| Situation | Action |
|---|---|
| Exact or adjacent match | Accept majority / primary |
| Two-level gap | Adjudicator review |
| Model vs all experts | Mark MODEL_DISAGREEMENT; do not auto-change engine |

### 6. Confidence recording

Experts record their own certainty (HIGH/MEDIUM/LOW).  
System confidence is separate.

### 7. Final adjudication

Adjudicator (knowledge lead) sets:

```text
reference_label_v2
reference_status: accepted | provisional | rejected_for_dataset
notes
```

### 8. Dataset inclusion criteria

Include only if:

- Chart verified  
- At least one complete rationale  
- Boundary/dispute cases have dual review or adjudication  
- No fabricated birth data  

## Blinding guidance

Prefer: experts classify before seeing `strength_level` / normalized score.  
Scores may be revealed in a second pass for disagreement analysis only.

## Anti-patterns

- One expert + force engine to match  
- Case-specific rule patches  
- Using runtime label as expert label  
