# Product Architecture Philosophy

| Field | Value |
|-------|-------|
| Document | PRODUCT_ARCHITECTURE_PHILOSOPHY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner |

This is product philosophy about structure.
It is not an implementation design.
It does not authorise new systems.

---

## 1. Why Truth is separated from Narrative

Truth answers: what is the chart.

Narrative answers: what may we say to this person about that chart.

If the same layer both calculates and writes, the product will eventually write whatever is easy to calculate, or calculate whatever is easy to write.

Separation protects two commercial properties:

- **Trust** — the reading can be rerun and still describe the same person.
- **Voice** — the reading can be improved without quietly changing the person.

Narrative may copy truth, explain truth, and refuse to overclaim.
Narrative may not invent a second chart.

---

## 2. Why Knowledge is separated from Editorial

Knowledge answers: what content is admissible in the tradition and the domain.

Editorial answers: may this sentence reach a paying customer.

A true, well-sourced paragraph can still be wrong as a product: too technical, too generic, too complete, too duplicated, or addressed to the wrong life stage.

If knowledge authors also act as the shipping editor, encyclopedias ship.
If editors also rewrite knowledge to sound better, tradition is falsified.

Knowledge expands coverage.
Editorial admits language.
Neither substitutes for the other.

---

## 3. Why Product decisions are separated from Architecture

Architecture answers: who owns which fact, and which path is allowed to run.

Product answers: what the customer is buying, and whether this artifact is worth the BTE name.

A sound architecture can still produce an unsellable consultation.
A desirable consultation that requires a new platform during Beta is still a refused product request.

If architecture teams decide commercial scope, the company ships systems.
If product teams redesign pipelines to win a wording argument, the company loses a single source of truth.

Beta 0 exists so that after freeze, architecture stays still while product quality moves.

---

## 4. Resulting operating model

```
Architecture holds the machine still.
Knowledge holds admissible content.
Truth is calculated once.
Narrative composes a reading.
Editorial admits the reading.
Product decides whether to sell it.
Release is permission to leave the company.
```

Each step has a different failure mode.
Collapsing any two steps recreates the failure this product was built to avoid: a calculator that talks, or a writer that calculates.

---

## 5. What this philosophy does not do

It does not add a layer, engine, framework, matrix, publisher, composer, or canon.
It forbids treating those additions as “philosophy work.”
Philosophy is how decisions are separated.
Architecture freeze is where those separations are locked for V1.
