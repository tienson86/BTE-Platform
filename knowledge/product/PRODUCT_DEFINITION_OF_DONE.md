# Product Definition of Done

| Field | Value |
|-------|-------|
| Document | PRODUCT_DEFINITION_OF_DONE |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner |

This is the official definition of Done for BTE product work.

---

## 1. What is not Done

A Completion Report is **not** Done.

Tests PASS is **not** Done.

A design note, a freeze document, a metric JSON, or a verbal review is **not** Done.

Those may be necessary.
They never close the work.

---

## 2. Official Done

```
Artifact
    ↓
Editorial Review
    ↓
Product Review
    ↓
Product Owner Approval
    ↓
Done
```

All four steps are required for customer-facing work.
Skipping a step leaves the work **not Done**.

---

## 3. Meaning of each step

| Step | Meaning |
|------|---------|
| **Artifact** | The customer-facing object exists: typically Executive PDF, Professional PDF, or the approved consultation surface for that work. Birth data are real. The artifact is reproducible from the frozen path. |
| **Editorial Review** | Editorial Standard V1 has admitted the language. No engine leakage, glossary dump in consultation, duplicate recommendations, or broken fragments. |
| **Product Review** | The artifact is judged as a consultation: recognition, understanding, action, commercial honesty. Tests and architecture review do not substitute. |
| **Product Owner Approval** | Recorded signoff. No implied approval. |

---

## 4. Scope of application

This definition applies to:

- features
- editorial repairs
- knowledge changes that reach the customer
- engine fixes that change the consultation
- releases
- commercial packaging that customers will see

Internal research notes may exist without this chain.
They must not be described as shipped, complete, or customer-ready.

---

## 5. Release overlay

A Beta or later release is not Done until the release checklist in `beta/BETA0_RELEASE_CHECKLIST.md` is also complete, including:

- Golden Dataset regenerated
- Executive PDFs regenerated
- Professional PDFs regenerated
- Editorial PASS
- Commercial PASS
- Product Owner approval

See `PRODUCT_ACCEPTANCE_POLICY.md` and `PRODUCT_RELEASE_POLICY.md`.
