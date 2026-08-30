# N-IMP-10A NARRATIVE STUDIO REPORT

Sprint: N-IMP-10A
Module: `applications.narrative_studio`
Mode: Shadow Mode — INTERNAL ONLY
Status: READY FOR PRODUCT OWNER REVIEW

---

## Status

PASS

Narrative Studio is an internal, read-only review workspace for Product Owner, Knowledge Author, and Developers. It is **not** part of the customer Portal. It does not modify Narrative, Knowledge, Pack05, astrology engines, or production routing.

Run:

```
uvicorn applications.narrative_studio.app:app --host 127.0.0.1 --port 8090
```

Open `http://127.0.0.1:8090/studio`

---

## Architecture

Standalone FastAPI app on loopback (`127.0.0.1:8090`).

```
CASE catalog
  → OrchestratorService.analyze (read)
  → NarrativeRuntime.run (isolated, shadow)
  → StudioReview snapshot
  → HTML panels (read-only)
```

- Not mounted on `applications.customer_portal`
- Not mounted on public `/result`
- `X-Robots-Tag: noindex, nofollow`
- Banner: **INTERNAL · SHADOW MODE · NOT CUSTOMER PORTAL**
- Approval records go to a Studio JSON file, never to Knowledge CSVs or Narrative builders

---

## Workspace

Case selector: **CASE-0001**, **CASE-0002**.

Default case: CASE-0001 (Nguyễn Tiến Sơn).

Sidebar panels:

| Key | Panel |
| --- | --- |
| overview | Overview |
| consulting | Consulting |
| structured | Structured |
| trace | Trace |
| decision | Decision |
| knowledge | Knowledge |
| compare | Compare |
| contract | Contract |
| quality | Quality |
| golden | Golden |
| approval | Approval |

URL: `/studio?case=CASE-0001&panel=overview`

The workspace never writes Presentation, Evidence, Knowledge, or Pack05.

---

## Review Panels

**Overview** — Presentation status, version `bte.presentation.v2.1`, Summary, Interpretation `consulting_flow`, Action top priority, Commercial null.

**Consulting** — `consulting_flow` exactly as packaged. No rewrite.

**Structured** — Observation, Reasoning, Meaning, Impact, Recommendation, Closing. Copied independently.

**Trace** — Expandable Evidence → Reasoning → Knowledge → Rewrite → Conversation → Consulting → Presentation.

**Decision** — Decision → Priority → Actions, with action traces (`decision_id`, rewrite/knowledge ids).

**Knowledge** — ids, status, approved, unresolved, contract gaps.

**Contract** — schema `bte.presentation.v2.1`, version, status, validation pass/reject, root fields.

**Quality** — validation, conversation/consulting status, meaning-preservation segment counts, contract gaps (identity/balance/conclusion null, commercial null, current_period null, closing duplicate).

---

## Comparison

Side-by-side, no editing:

- **Pack05** — `pack05_narrative_result_v1` identity + priority_recommendation
- **Narrative V2** — Overview headline + consulting_flow

CASE-0001 shows different customer wording between Pack05 (“Người định khung”) and V2 (stability / foundation consulting register). Expected in shadow mode.

---

## Trace

Trace is diagnostic and internal. Evidence records, knowledge ids, and rewrite ids are visible **only** inside Studio. They are not rendered on customer Portal.

Studio re-runs NarrativeRuntime against the Analyze payload to obtain context. It does not mutate that context.

---

## Approval

Internal panel: PASS / REVIEW / REJECT, comment, reviewer, timestamp.

Stored in `implementation/narrative_v2/studio_reviews/approvals.json` when used.

This is Studio metadata. It does **not** change Narrative content or Knowledge assets.

---

## Tests

`py -m pytest tests/narrative_v2/test_narrative_studio.py -q`

**5 passed**

- Catalog CASE-0001 / CASE-0002
- Load Presentation, Trace, Knowledge, Decision, Pack05 compare, Golden snapshot
- No mutation of Knowledge tree or frozen Presentation JSON
- HTTP internal banner + panels + approval record in tmp store
- Customer Portal `app.py` does not reference Studio

Remaining failures in this module: **none**.

---

## Screenshots

`implementation/narrative_v2/n_imp_10a/`

| File | Panel |
| --- | --- |
| `01_overview.png` | Overview |
| `02_consulting.png` | Consulting |
| `03_trace.png` | Trace (Evidence expanded) |
| `04_compare.png` | Pack05 vs Narrative V2 |
| `05_approval.png` | Approval |

---

## Out-of-scope

Customer Portal modified: **NO**

Pack05 modified: **NO**

Production switch: **NO**

Astrology engines modified: **NO**

Internal diagnostics exposed publicly: **NO**

Golden Dataset modified: **NO**

PDF/DOCX integration: **NO**

N-IMP-11 started: **NO**

---

## Files created

- `applications/narrative_studio/app.py`
- `applications/narrative_studio/catalog.py`
- `applications/narrative_studio/service.py`
- `applications/narrative_studio/golden.py`
- `applications/narrative_studio/approvals.py`
- `applications/narrative_studio/renderer.py`
- `applications/narrative_studio/static/studio.css`
- `applications/narrative_studio/scripts/capture_n_imp_10a_screenshots.py`
- `applications/narrative_studio/README.md`
- `tests/narrative_v2/test_narrative_studio.py`
- `implementation/narrative_v2/n_imp_10a/*.png`
- `implementation/narrative_v2/N_IMP_10A_REPORT.md`

## Files modified

None in customer Portal, Pack05, astrology engines, or Golden Dataset.

---

## Verdict

**READY FOR PRODUCT OWNER REVIEW**
