# COMMERCIAL_LANGUAGE_ARCHITECTURE

Version: 1.2.0

---

## 1. Position in the platform

```
Engines (facts)
    ↓
Domain composers (domain conclusions)
    ↓
Cross-Domain Reasoning (claims, relations, themes, claim plans)
    ↓
Commercial Language Layer  ← YOU ARE HERE
    ↓
Feature packaging (Identity / Career / Executive / future)
    ↓
Customer Mode deliverable
```

Higher layers win on **truth**. This layer wins on **how truth is said**.

---

## 2. Hard boundary

| Allowed | Forbidden |
|---------|-----------|
| Rephrase claim-plan slots into paragraphs | Change strength / pattern / TG / UG values |
| Choose safer customer phrasing for unresolved tension | Hide TRUE_CONFLICT / unresolved without safe language |
| Map keys → Vietnamese consulting sentences | Invent new themes not in the claim plan |
| Add recognition + action framing | Add job titles, income, luck timing, diagnoses |
| One memorable closing line | Copy CASE-0001 master prose into other cases |

**Input is authoritative. Output is interpretive language only.**

---

## 3. Input contracts (consumed, not owned)

Minimum supported inputs:

- `ExecutiveClaimPlan`
- `IdentityClaimPlan` (feature-local or derived from ExecutiveClaimPlan)
- `CareerClaimPlan` (feature-local or derived from ExecutiveClaimPlan with CAREER salience)

Writers must not require raw `claim_id`, relation enums, scores, or reason codes in Customer Mode.

---

## 4. Output contract

| Unit | Definition |
|------|------------|
| Paragraph | 2–5 sentences; one idea; answers So what / Care / Do |
| Section body | Ordered paragraphs for one feature section |
| Closing line | Optional Layer 5 memory line (≤ 20 words preferred) |

No claim keys (`balance:Nhâm`, `align_operating_role:…`) in customer text.

---

## 5. Five-layer pipeline (per paragraph)

```
Claim slot value
  → L1 Plain Language
  → L2 Consulting Style
  → L3 Recognition (when identity/self is in scope)
  → L4 Action (when priorities/avoidances/change in scope)
  → L5 Memorable Closing (section or report end only)
```

Not every paragraph uses all five layers. Minimum: **L1 + L2**. Feature sections that advise must include **L4**. Opening “who” sections should include **L3**.

---

## 6. Ownership

| Artifact | Owner |
|----------|-------|
| Facts / classifications | Engines |
| Cross-domain relations / themes | Reasoning (CDR) |
| Claim plans | Reasoning / feature planners |
| Writing rules | **This package** |
| Sentence rendering in code | Feature composers (implementation follows this guide) |
| Brand feel | `BTE_BRAND_LANGUAGE` / Experience Principles |

---

## 7. Quality gate (commercial readiness)

A paragraph is commercially ready only if:

1. Traceable to a claim-plan slot or published safe conclusion  
2. Free of internal keys and enum names  
3. Passes So what / Care / Do  
4. Matches chart-specific theme (no foreign-case leakage)  
5. Does not invent unsupported outcomes  

---

## 8. Non-goals (V1.2)

- LLM authorship as source of truth  
- Literary fiction  
- Full Master Consulting package redesign  
- New BaZi knowledge content  
