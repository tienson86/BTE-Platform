# 13 — Commercial V1 Release Package

Version: 1.0.0  
Date: 2026-08-08  
Owner: BTE Product  

| Field | Value |
|-------|-------|
| **Status** | **Release Candidate 1** |
| **Engineering** | **PASS** |
| **Golden Cases** | **PASS** |
| **Commercial QA** | **PASS** |
| **Human Consulting Review** | **PENDING** |
| **Product Decision** | **PENDING** |
| **Commercial Version** | **RC1** |

**Commercial V1 is NOT Released.**  
Final Product sign-off section is intentionally **blank**.

---

## 1. RC1 status

| Field | Value |
|-------|-------|
| Status | Release Candidate 1 |
| Engineering | PASS |
| Golden Cases | PASS |
| Commercial QA | PASS |
| Product documentation | PASS (this package) |
| Human Consulting Review | PENDING |
| Product Decision | PENDING |
| Commercial Version | RC1 |
| Commercial V1 Released? | No |

Supporting summary: `09_COMMERCIAL_V1_RELEASE_CANDIDATE_SUMMARY.md`

---

## 2. Capability Registry snapshot

Source of truth: `knowledge/product/01_CAPABILITY_REGISTRY.md`

| Registry ID | Name | Version | Status | Stage | Production |
|-------------|------|---------|--------|-------|------------|
| CAP-CAREER-SEL-001 | Career Selection Assessment | 1.0.0 | Released | Frozen | Yes |
| CAP-CAREER-PRO-001 | Promotion Readiness Assessment | 1.0.0 | Released | Production | Yes |
| CAP-CAREER-LED-001 | Leadership Assessment | — | Proposed | Proposed | No |

```
Capability Released  ≠  Commercial version Released
```

Both SEL and PRO may be live as Capabilities while Commercial V1 remains **RC1**.

Commercial version (product): **Commercial V1 RC1** — awaiting Human Consulting + Product GO.

---

## 3. Release checklist (RC1 cut)

Template source: `knowledge/releases/process/03_RELEASE_CHECKLIST.md`

| Field | Value |
|-------|-------|
| Commercial version | Commercial V1 |
| RC label | RC1 |
| Owner | BTE Product |
| Date | 2026-08-08 |

| Area | Status |
|------|--------|
| Architecture freeze reviewed | Done |
| Foundation / Design System not casually modified | Done |
| In-scope Capabilities in Registry | Done |
| Knowledge / allow-lists match SEL ∪ PRO ∪ Wave 1.1 | Done |
| Narrative enrich-only · primary/secondary Rec policy | Done |
| Portal — no unauthorized new routes/layouts | Done |
| Module QA (`tests/domain01` + `tests/commercial_knowledge`) | Done |
| Regression (Wave 1.1 / prior caps) | Done |
| Registry + Product Changelog consistent | Done |
| Known limitations documented (`11`) | Done |
| Human consulting package available | Done — reviews **PENDING** |
| Product Decision | **PENDING** (unsigned) |
| Product GO recorded | No |

---

## 4. Regression summary

| Surface | Result |
|---------|--------|
| Wave 1.1 Adapter default path | Preserved (adapter default remains Wave 1.1; production hook uses production allow-list) |
| CAP-CAREER-SEL-001 | Regression retained with PRO companion |
| CAP-CAREER-PRO-001 | Shipped with SEL Frozen companion |
| Commercial polish suite | `commercial_v1/07`–`09` |
| Automated | `tests/domain01` + `tests/commercial_knowledge` — **41 PASS** (as of P0 polish cut) |
| Golden Dataset / snapshots | **Not mutated** to force green |

---

## 5. Golden Case summary

| Capability | Cases | Result |
|------------|-------|--------|
| CAP-CAREER-SEL-001 | D1-GC-STRONG-EMP · WEAK-EMP · MIXED-EMP | **3/3 PASS** |
| CAP-CAREER-PRO-001 | D1-GC-PROMOTE-READY · PREPARE · MIXED | **3/3 PASS** |

Evidence: Domain reports `20`–`30`; Capability Acceptance Standard Pass.

---

## 6. Human Review status

| Item | Status |
|------|--------|
| RC1 review guide | `knowledge/product/release_candidate/01_RC1_REVIEW_GUIDE.md` |
| Case checklist | `02_CASE_REVIEW_CHECKLIST.md` |
| Scoring sheet | `03_CASE_SCORING_SHEET.md` |
| Consulting acceptance form | `04_CONSULTING_ACCEPTANCE_FORM.md` |
| RC1 release decision form | `05_RC1_RELEASE_DECISION.md` (**unsigned**) |
| Human Consulting Review | **PENDING** |
| Product Decision | **PENDING** |
| Consulting acceptance signed? | No |
| Archive folder | **INACTIVE** |

Human Consulting Review is the **final approval gate** before Product may mark GO.

---

## 7. Package inventory

| File | Role |
|------|------|
| `09_COMMERCIAL_V1_RELEASE_CANDIDATE_SUMMARY.md` | RC1 summary + recommendation |
| `10_COMMERCIAL_V1_FINAL_CHANGELOG.md` | Changelog inception → RC1 |
| `11_COMMERCIAL_V1_KNOWN_LIMITATIONS.md` | Deferred to V1.1 |
| `12_COMMERCIAL_V1_BASELINE.md` | Baseline inventory |
| `13_COMMERCIAL_V1_RELEASE_PACKAGE.md` | This package cover |

Related: `knowledge/releases/process/` · `knowledge/product/` · `knowledge/product/commercial_v1/` · `knowledge/product/release_candidate/`

---

## 8. Final Product sign-off

**Leave blank until Product Owner completes Human Consulting Review.**

| Field | Value |
|-------|-------|
| Decision | ☐ GO · ☐ GO WITH MINOR FIXES · ☐ NO GO |
| Decision date | ________________ |
| Product Owner | ________________ |
| Rationale | ________________ |
| Minor fix list (if any) | ________________ |
| Commercial V1 Released? | ☐ Yes · ☐ No *(must remain No until GO)* |
| Signature / recorded by | ________________ |

Also complete: `knowledge/product/release_candidate/05_RC1_RELEASE_DECISION.md`

---

## 9. Stop line

**Commercial V1 Release Package is complete and ready for final Product sign-off.**

Do not modify runtime, Knowledge, Portal, or Foundation as part of this package.  
**Do not declare Commercial V1 Released until section 8 is signed GO.**

---

END
