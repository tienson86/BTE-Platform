# 04 — Capability Acceptance Standard

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  
Depends on: `01_CAPABILITY_REGISTRY.md`, `02_CAPABILITY_RELEASE_POLICY.md`  

---

## 1. Purpose

Every capability must satisfy this Acceptance Standard before Status may become **Released** and Production **Yes**.

No exceptions for “partial ship” marketed as Production Capability.

---

## 2. Mandatory gates

A capability **Passes** only when **all** gates below are Pass or Explicitly N/A (with Product sign-off).

| # | Gate | Question |
|---|------|----------|
| 1 | **Architecture** | Is the capability bounded, non-goals clear, and Domain-mapped? |
| 2 | **Knowledge** | Are required Knowledge Units approved and cover the capability slots? |
| 3 | **Golden Cases** | Do required Golden Cases PASS for the capability? |
| 4 | **Narrative** | Does Narrative enrich Exec / Rec / Decision Support without replacing Interpretation meaning? |
| 5 | **Commercial Quality** | Is wording consultant-grade, ethical, and free of technical leakage? |
| 6 | **Production Wiring** | Is the production path (allow-list → Bundle → Narrative → delivery) complete? |
| 7 | **Portal Verification** | Does the capability appear on the existing Result / delivery surface without layout redesign? |
| 8 | **Regression** | Do Wave 1.1 and prior Released capabilities still PASS? |
| 9 | **Documentation** | Are Domain / product docs updated (index, wiring, validation)? |
| 10 | **Release Notes** | Are customer-visible changes and non-goals published? |

---

## 3. Gate detail

### 3.1 Architecture

- Capability ID registered  
- Customer outcome and out-of-scope written  
- Dependencies listed (Wave, Domain, other capabilities)  
- No Foundation redesign required (or RFC approved)

### 3.2 Knowledge

- Slot coverage = 100% of **required** units for this capability version  
- Units `approved` (or equivalent review_status)  
- Allow-list candidates documented; unrelated Domain units excluded  
- Narrative never consumes raw KU rows

### 3.3 Golden Cases

- Official case set for this capability version defined  
- All required cases PASS checklist (direction, risks, mitigation, actions as applicable)  
- Failures logged; P0 blockers closed  

### 3.4 Narrative

- Enrich-only merge  
- Analytical Interpretation conclusions preserved  
- Bundle fields / evidence targets mapped to Exec, Recommendation, Decision Support  

### 3.5 Commercial Quality

- No engine tokens / mock markers / “kích hoạt khi…” style technical phrasing in customer text  
- Claims bounded (no guaranteed income, titles, medical promises where ethics apply)  
- Mitigate-first when weakness/risk fires  

### 3.6 Production Wiring

- Production allow-list includes only intended capability units (+ Wave cores as required)  
- Bundle exposes typed capability projection  
- Traceability chain intact  

### 3.7 Portal Verification

- Content visible in existing Result Page composition  
- No new screen/route required for V1 delivery unless Product explicitly plans one later  
- Design System / Visual Language unchanged  

### 3.8 Regression

- Prior Released capabilities unchanged in meaning  
- Wave 1.1 commercial cores still select correctly when intended  
- Module test suites for capability + commercial knowledge PASS  

### 3.9 Documentation

- Registry updated  
- Domain completion / wiring / validation docs linked  
- Roadmap status consistent  

### 3.10 Release Notes

- Version, changes, Golden Cases, regression note, production date  
- Changelog entry created  

---

## 4. Pass / Fail recording

| Result | Registry fields |
|--------|-----------------|
| **Pass** | Acceptance Status = Pass; may set Production = Yes after Release Policy exit |
| **Fail** | Acceptance Status = Fail; remain Integration or Golden Review |
| **Pending** | Not yet evaluated |

Evidence lives in Domain reports and/or `tests/<capability>/` — Registry records the verdict, not raw logs.

---

## 5. Reference: CAP-CAREER-SEL-001 v1.0.0

| Gate | Verdict |
|------|---------|
| Architecture | Pass (Domain 01 capability model) |
| Knowledge | Pass (11/11 SEL) |
| Golden Cases | Pass (3/3 P0) |
| Narrative | Pass (enrich-only) |
| Commercial Quality | Pass (acceptance + production validation) |
| Production Wiring | Pass (`20_PRODUCTION_WIRING_REPORT`) |
| Portal Verification | Pass (adapter slots; no layout change) |
| Regression | Pass (`tests/commercial_knowledge`) |
| Documentation | Pass (`20`–`23`, Registry) |
| Release Notes | Pass (`23_RELEASE_NOTES`, Changelog) |

**Overall: Pass → Production Capability V1**

---

## 6. Stop line

Acceptance Standard is mandatory for Release 2+.  

Promotion Readiness must not enter Production without a full Pass on this standard.

---

END
