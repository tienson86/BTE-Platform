# Interpretation Composition & Assembly Engine

Version: 1.0.0  
Engine ID: `interpretation_composition_engine`  
Sprint: IE-3  
Status: Canonical assembly layer  
Foundation: v1.0.0 (frozen)

This engine assembles validated IE-2 Sentence Candidates into the canonical Interpretation Result.

It does **not** render reports or export PDF, HTML, DOCX, or Markdown.

It does **not** generate new knowledge or rewrite sentences.

---

## Composition lifecycle

```
InterpretationContext (IE-1)
CompositionResult + Sentence Candidates (IE-2)
CanonicalAnalysisResult / CanonicalDecisionResult / CanonicalLuckResult
        ↓
InterpretationAssemblyContext (append-only)
        ↓
Section Builder
        ↓
Chapter Builder
        ↓
Flow Optimizer (order / group only)
        ↓
Cross Reference Builder
        ↓
CanonicalInterpretationResult
```

Registry order:

`section_builder → chapter_builder → flow_optimizer → cross_reference_builder → assembly`

`InterpretationCompositionEngine.run()` never raises. Failures become diagnostics.

---

## Section model

A section is a structural grouping of sentence candidate identities.

| Field | Meaning |
|---|---|
| `section_id` | `SEC-{module_id}` |
| `module_id` | Registered interpretation module |
| `candidate_ids` | Consumed `SC-…` identifiers |
| `knowledge_ids` / `evidence_ids` / `reasoning_ids` | Copied identities |
| `status` | `assembled` |

No styling. No formatting. No prose.

---

## Chapter model

Registered chapters, deterministic order:

1. Overview  
2. Personality  
3. Career  
4. Wealth  
5. Relationship  
6. Health  
7. Children  
8. Luck  
9. Summary  

Empty registered chapters remain present with `status = empty`.

---

## Flow optimization

Allowed:

- ordering by canonical module rank
- grouping overview → body → summary
- declaring section dependencies

Forbidden:

- rewriting
- paraphrasing
- summarization

---

## Cross-reference model

Structured identity links only:

- chapter ↔ section
- section → knowledge / evidence / reasoning

No hyperlink rendering. No href. No anchors.

---

## Canonical Interpretation Result

The only official IE-3 Interpretation output:

- `sections`
- `chapters`
- `cross_references`
- `metadata`
- `interpretation_trace`
- `interpretation_audit`
- `diagnostics`
- `interpretation_version`

IE-1 `CanonicalInterpretationResult` remains the empty foundation shell and is unchanged.

---

## Diagnostics

| Code | Meaning |
|---|---|
| `SECTION-DUPLICATE` | Duplicate section id |
| `CHAPTER-DUPLICATE` | Duplicate chapter id |
| `REFERENCE-BROKEN` | Cross reference target missing |
| `FLOW-VIOLATION` | Illegal order or forbidden flow operation |
| `CONTRACT-VIOLATION` | Version / registry / contract failed |
| `PIPE-OK` | Assembly passed |
| `PIPE-FAIL` | Assembly stopped |

---

## Future IX-1 integration

IX-1 will orchestrate IE-1 → IE-2 → IE-3 as the Canonical Interpretation Pipeline.

IE-3 publishes the assembled result that IX-1 will bind as the pipeline output.

---

## Future Report Engine integration

Report Engine will consume this assembled result to render PDF / HTML / DOCX / Markdown.

IE-3 must not perform that rendering.

---

## Compliance

- Foundation v1.0.0 frozen
- AX-2 / AX-3 / AX-4 / IE-1 / IE-2 unchanged
- Ready for IX-1 Canonical Interpretation Pipeline
