# 06 — Golden Knowledge Standard

Version: 1.0  
Status: **OFFICIAL — Golden Knowledge Standard**  
Date: 2026-08-08  
Epic: EPIC 3 — Knowledge Population · Golden Review  
Scope: Documentation only — no unit/content/runtime changes  

---

## 1. Purpose

Define the official quality bar that **every future Knowledge Unit** must satisfy before it can be considered Golden and eligible for Publish.

This standard extends (does not replace):

- EPIC 2 Authoring Standard (`15`)  
- EPIC 3 Validation Rules (`03`)  
- Content Quality Release B (Exec / Recommendation / Warning)  

---

## 2. Golden criteria (mandatory set)

Every Knowledge Unit must be:

1. Correct  
2. Evidence-based  
3. Commercially valuable  
4. Actionable  
5. Professional  
6. Natural  
7. Reusable  
8. Traceable  
9. Narrative-friendly  
10. Explainable  
11. Future-proof  

---

## 3. Criterion definitions

### 3.1 Correct

| Aspect | Definition |
|--------|------------|
| **Purpose** | Advisory meaning must align with BaZi analytical truth for stated conditions |
| **Acceptance criteria** | No contradiction with Analysis signals; conditions falsifiable; drop-if-conflict policy honored; no invented chart facts |
| **Common failure modes** | Advising thân vượng language under thân nhược conditions; absolute fate claims; mismatched useful-god guidance |

### 3.2 Evidence-based

| Aspect | Definition |
|--------|------------|
| **Purpose** | Unit fires only when required evidence / interpretation focus can exist |
| **Acceptance criteria** | `evidence_kind` set; `condition` bound to Analysis; `required_evidence` / `required_interpretation` coherent; placeholders only for bindable signals |
| **Common failure modes** | Always-true conditions; placeholders without signal source; requiring evidence the unit itself is supposed to create |

### 3.3 Commercially valuable

| Aspect | Definition |
|--------|------------|
| **Purpose** | Improves real consultation outcomes (Exec, Rec, Warning, Impact, decision posture) |
| **Acceptance criteria** | Clear `primary_intent`; `commercial_value` justified; improves at least one Narrative commercial slot |
| **Common failure modes** | Academic trivia; synonym spam; content that never appears in customer-facing consultation |

### 3.4 Actionable

| Aspect | Definition |
|--------|------------|
| **Purpose** | Customer can do something (or understand a clear posture) |
| **Acceptance criteria** | For Action kind: specific next step + reason; for Analytical: clear naming/framing customer can reuse; decision posture when relevant |
| **Common failure modes** | “Cố gắng hơn”; vague inspiration; Action without chart binding |

### 3.5 Professional

| Aspect | Definition |
|--------|------------|
| **Purpose** | Consultant voice — calm, respectful, ethical |
| **Acceptance criteria** | Brand consultant-not-calculator; ethics flags when needed; no shame, doom, medical overclaim, return guarantees |
| **Common failure modes** | Calculator jargon; fear language; diagnostic health claims |

### 3.6 Natural

| Aspect | Definition |
|--------|------------|
| **Purpose** | Reads as spoken commercial Vietnamese counsel |
| **Acceptance criteria** | Fluent VI body; no rule-engine residue (“kích hoạt khi”, matched_rules); minimal system flavor |
| **Common failure modes** | Translated stiffness; template brackets left unbindable; technical dumps |

### 3.7 Reusable

| Aspect | Definition |
|--------|------------|
| **Purpose** | One unit serves many scenarios/channels without clone text |
| **Acceptance criteria** | Atomic granularity; scenario/domain affinity declared; not UI-only; secondary_usage considered |
| **Common failure modes** | Whole-report blobs; Portal-hardcoded twins; one-off marketing lines |

### 3.8 Traceable

| Aspect | Definition |
|--------|------------|
| **Purpose** | End-to-end audit from unit → evidence → Narrative |
| **Acceptance criteria** | Stable id; signal_refs and/or REF-*; version; review_status; wave_id; pairing ids when needed |
| **Common failure modes** | Missing id/version; no signal binding; silent edits to Published meaning |

### 3.9 Narrative-friendly

| Aspect | Definition |
|--------|------------|
| **Purpose** | Fits Pack 05 components without composer invention |
| **Acceptance criteria** | `narrative_targets` realistic for kind; evidence_kind maps to slots; Exec/Rec/Warning CQ shape when claimed |
| **Common failure modes** | Wrong evidence kind; Warning without mitigation path for Risk kind; forcing new Narrative sections |

### 3.10 Explainable

| Aspect | Definition |
|--------|------------|
| **Purpose** | Customer understands *why*, not only *what* |
| **Acceptance criteria** | Modern interpretation states meaning clearly; classical support (if any) does not contradict; reasoning-capable when targeted |
| **Common failure modes** | Opaque labels; classical quote without modern bridge; contradiction between classical and body |

### 3.11 Future-proof

| Aspect | Definition |
|--------|------------|
| **Purpose** | Survives store format, channel, and minor Analysis field evolution |
| **Acceptance criteria** | Render-agnostic; logical schema fields complete; conditions use stable signal concepts; additive versioning ready |
| **Common failure modes** | CSS/layout coupling; brittle one-off field names with no contract note; irreversible in-place edits |

---

## 4. Golden vs Publish vs Draft

| Class | Meaning |
|-------|---------|
| **Draft** | Authoring; may fail multiple criteria |
| **Publish-eligible** | Meets hard fails (`03`) + all Golden criteria at Acceptable or better |
| **Golden Reference** | Meets Golden criteria at Strong/Golden score tier (`08`); may be cited as exemplar |

A unit can be Publish-eligible without being Golden Reference.  
Golden Reference units become teaching exemplars for future waves.

---

## 5. Relationship to scoring

Detailed 0–10 scoring: `08_KNOWLEDGE_QUALITY_SCORE.md`.  
Review workflow: `07_KNOWLEDGE_REVIEW_GUIDE.md`.

---

## 6. Stop line

Golden Knowledge Standard established.  
No units modified.

---

END
