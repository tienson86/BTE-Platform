# FEEDBACK_FORM (execution)

| Field | Value |
|-------|-------|
| Form | **RC3-FF-1.0** — frozen |
| Spec | `../RC3/FEEDBACK_FORM.md` |
| This file | How to run it · not a second questionnaire |

Do not add, drop, or reword questions here.

---

## One form per slot

| Slot | Case | Persona | Package | Form file (offline) |
|------|------|---------|---------|---------------------|
| BU-01 | CASE_0001 | P01 | C | `RC3-FF-1.0 / BU-01` |
| BU-02 | CASE_0002 | P02 | C | `RC3-FF-1.0 / BU-02` |
| BU-03 | CASE_0003 | P03 | PARENT | `RC3-FF-1.0 / BU-03` |
| BU-04 | Pilot CASE-0006 | P04 | B | `RC3-FF-1.0 / BU-04` |
| BU-05…10 | after bind | P05…P10 | as assigned | after bind |

Store dated copies **offline** (or later `knowledge/beta/RC3/forms/` with no PII).  
Do not create the forms folder until the first session.

---

## Staff header (fill before the participant scores)

| Field | Source |
|-------|--------|
| Case | BETA_USERS chart id |
| Persona | P0n |
| Date | Session day |
| Reader role | SELF / PARENT / OTHER |
| Package shown | A / B / C / PARENT |
| Participant id | Offline only |

---

## Participant block (unchanged)

Open questions 1–6 and scores 0–10 as frozen:

What felt accurate · surprised · generic · most valuable · would you pay · would you recommend  

Trust · Clarity · Value · Actionability · Recommendation · Purchase Intent  

Optional probes only if time.

---

## Rules

| Rule | Detail |
|------|--------|
| Same sitting | Form the day they read the report |
| No coaching scores | Clarify vocabulary only |
| No polish | Keep their words |
| No mix | Never copy BU-01 answers onto BU-02 |
| Lab ≠ live | Do not paste ITERATION_002 lab 9.5 into this form |

---

## After the form

1. Score sheet → [FEEDBACK_SCORING.md](FEEDBACK_SCORING.md)  
2. Defects → [ISSUE_PIPELINE.md](ISSUE_PIPELINE.md)  
3. Do not fix during the session  

---

END
