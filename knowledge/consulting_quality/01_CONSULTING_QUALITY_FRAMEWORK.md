# 01 — Consulting Quality Framework

Version: 1.0  
Status: **OFFICIAL — Consulting Quality Framework (design)**  
Date: 2026-08-08  
Epic: EPIC 5 — Consulting Quality · Sprint A  
Depends on: Product Manifesto · Experience Principles · Brand Language · Wave 1.1 · EPIC 4 Sprint B  
Scope: Documentation only — no runtime  

---

## 1. Purpose

Define the **dimensions** of consultant-quality output for BTE.

A case may pass analytical and Narrative technical checks and still fail consulting quality.  
Commercial release requires both **truth** (Analysis) and **consultation quality** (this framework).

---

## 2. Evaluation object

Primary object: **NarrativeResult** (and its customer-visible slots), especially:

| Surface | Why it matters |
|---------|----------------|
| Executive Summary | First trust and framing |
| Recommendation | Decision support and next step |
| Warning | Risk honesty without harm |
| Full Narrative | Coherent consultation arc |

Secondary (trace only): Commercial Knowledge Bundle provenance, Interpretation sections — reviewers may inspect them to explain defects, not to re-score engines.

---

## 3. Quality dimensions (official set)

Each dimension is scored independently on the Scorecard (`04`). Definitions below are normative.

### 3.1 Accuracy

| Aspect | Definition |
|--------|------------|
| **Meaning** | Advisory statements align with Analysis facts for this case; no invented chart claims |
| **Good looks like** | Identity, strength/weakness, useful-god guidance match signals; placeholders correctly bound |
| **Fails when** | Contradicts thân band / Dụng thần / pattern; absolute fate claims; advice for signals not present |

### 3.2 Professionalism

| Aspect | Definition |
|--------|------------|
| **Meaning** | Calm consultant voice; ethical; respectful of the customer |
| **Good looks like** | Expert framing without arrogance; no shame, doom, medical/legal overclaim, return guarantees |
| **Fails when** | Calculator dumps; moral judgment; sensational language; brand-breaking tone |

### 3.3 Naturalness

| Aspect | Definition |
|--------|------------|
| **Meaning** | Reads as spoken professional consultation, not template glue or engine residue |
| **Good looks like** | Smooth Vietnamese commercial prose; coherent transitions |
| **Fails when** | Field-label echo (“Nhật chủ: … Cách cục: …” as the whole answer); technical markers; stub phrases |

### 3.4 Readability

| Aspect | Definition |
|--------|------------|
| **Meaning** | Customer can scan and understand hierarchy without BaZi training |
| **Good looks like** | Clear identity → strengths/cautions → priority; short enough to act on |
| **Fails when** | Dense jargon stack; walls of synonyms; missing hierarchy |

### 3.5 Actionability

| Aspect | Definition |
|--------|------------|
| **Meaning** | Customer knows what to prioritize and what to do next |
| **Good looks like** | One primary priority + concrete next step + reason tied to Dụng thần / structure |
| **Fails when** | Vague inspiration (“cố gắng hơn”); action without reason; many competing priorities |

### 3.6 Commercial Value

| Aspect | Definition |
|--------|------------|
| **Meaning** | Output justifies a paid consultation: insight + posture + usable next step |
| **Good looks like** | Customer would leave clearer than they arrived; Wave 1.1 enrichment improves Exec/Rec when applicable |
| **Fails when** | Restates Analysis labels only; no advisory lift; feels like a free calculator screenshot |

### 3.7 Consistency

| Aspect | Definition |
|--------|------------|
| **Meaning** | Exec, Recommendation, Warning, and Narrative do not contradict each other |
| **Good looks like** | Same identity frame; recommendation aligns with useful-god story; warning tone matches weakness |
| **Fails when** | Exec says strong / Rec implies collapse; mixed Dụng thần; duplicated conflicting advice |

### 3.8 Empathy

| Aspect | Definition |
|--------|------------|
| **Meaning** | Limits and risks are named without humiliating or alarming the customer |
| **Good looks like** | Weakness as design constraint; warning as care; strength without hype |
| **Fails when** | Blame language; fear marketing; empty flattery that hides risk |

### 3.9 Trustworthiness

| Aspect | Definition |
|--------|------------|
| **Meaning** | Customer can trust scope, confidence, and honesty about insufficient data |
| **Good looks like** | Clear when data is thin; provenance visible to reviewers; no overconfident guarantees |
| **Fails when** | Fake certainty; hides insufficient flags; invents evidence |

### 3.10 Decision Support

| Aspect | Definition |
|--------|------------|
| **Meaning** | Output helps a real life decision posture (prepare / prioritize / defer / align) |
| **Good looks like** | Customer can answer “what should I do this week?” with chart-bound guidance |
| **Fails when** | Pure description with no posture; decision language without chart binding |

---

## 4. Dimension groups (for review sessions)

| Group | Dimensions | Primary surfaces |
|-------|------------|------------------|
| **Truth & trust** | Accuracy, Trustworthiness, Consistency | All |
| **Voice & experience** | Professionalism, Naturalness, Readability, Empathy | Exec, Narrative, Warning |
| **Commercial outcome** | Actionability, Commercial Value, Decision Support | Recommendation, Exec priority |

Reviewers must score all ten dimensions; groups only aid discussion.

---

## 5. What this framework is not

| Not | Why |
|-----|-----|
| A replacement for Golden Knowledge Standard | That scores **units**; this scores **cases** |
| An automated Narrative validator | Human judgment required for commercial release |
| Permission to change Analysis | Accuracy means align with Analysis, not rewrite it |
| A UI/brand redesign brief | Foundation and Design System remain frozen |

---

## 6. Wave 1.1 constraint

Until Product expands knowledge:

- Only Wave 1.1 cores may supply commercial enrichment.  
- Missing domains (career depth, timing packs, etc.) must be handled as **insufficient / out of scope**, not invented.  
- Reviewers must not demand Wave 1.2 content as a pass condition for Sprint A cases.

---

## 7. Stop line

Framework dimensions defined. Scoring rules live in `04`. Release bar lives in `05`.

---

END
