# Role Model — V1.0

| Field | Value |
|-------|-------|
| Document | ROLE_MODEL |
| Version | 1.0.0 |
| Section | 4 — Role Model |

---

# 4.1 Frozen roles

| Role | Authority level |
|------|-----------------|
| Knowledge Author | Creates content |
| Cursor | Assists; **never final authority** |
| QA Assistant | Scores and recommends |
| Domain Reviewer | Accepts QA; promotes Reviewed/Validated |
| Chief Reviewer | Charter, freeze, waivers |
| Release Manager | Business release |
| Production Owner | Production config and rollback |

---

# 4.2 Knowledge Author

| Responsibility |
|----------------|
| Write Interpretation Knowledge (Library) prose |
| Convert Library → Catalog units |
| Complete Author checklists before submission |
| Fix FAIL/REVIEW items in authoring tasks |
| Declare duplicate clusters at catalog time |
| Never self-promote to Reviewed, Validated, or Frozen |

| May not |
|---------|
| Redefine Rule Database facts |
| Edit Interpretation Standard |
| Approve own QA |
| Skip quality gates |

---

# 4.3 Cursor

| Responsibility |
|----------------|
| Assist Author with catalog conversion |
| Act as QA Assistant when tasked |
| Generate phase reviews using QA_TEMPLATE |
| Draft checklists and documentation |

| May not |
|---------|
| Be final approval authority |
| Change catalog status unilaterally |
| Rewrite knowledge during QA-only tasks |
| Approve Freeze or Release |
| Modify frozen systems listed in factory constraints |

**Cursor output = input to human reviewers.**

---

# 4.4 QA Assistant

| Responsibility |
|----------------|
| Score twelve criteria per QA Standard |
| Assign PASS / REVIEW / FAIL |
| Write rationale for every non-PASS unit |
| Produce topic phase statistics |
| Archive review under `knowledge_qa/PACK_XX/` |

| May not |
|---------|
| Redefine QA criteria (see QA Standard) |
| Edit catalog claims during QA task |
| Promote lifecycle status |
| Waive FAIL without Chief Reviewer |

Human or AI may perform QA Assistant work. Human Domain Reviewer always accepts.

---

# 4.5 Domain Reviewer

| Responsibility |
|----------------|
| Accept or reject QA Assistant output |
| Resolve Borderline verdicts |
| Promote Draft → **Reviewed** |
| Promote Reviewed → **Validated** after validation |
| Sign phase reviews |
| Escalate cross-pack and golden conflicts |

| May not |
|---------|
| Skip QA gate |
| Freeze catalog (Chief Reviewer gate) |
| Edit production Frozen catalog directly |

Typically a senior BaZi consultant or domain lead.

---

# 4.6 Chief Reviewer

| Responsibility |
|----------------|
| Approve pack charter (QG0) |
| Approve Library (QG1) |
| Waive QA FAIL with written record |
| Approve pack **Freeze** (QG6) |
| Resolve duplicate cluster disputes |
| Own factory policy exceptions |

| May not |
|---------|
| Bypass Validation gate for golden-pinned units |
| Unfreeze without new version |

Platform governance role — one per platform or delegated per domain.

---

# 4.7 Release Manager

| Responsibility |
|----------------|
| Coordinate Release gate (QG7) |
| Publish release notes |
| Coordinate customer communication |
| Schedule release windows |

| May not |
|---------|
| Load unfrozen catalog to production |
| Override Production Owner rollback |

---

# 4.8 Production Owner

| Responsibility |
|----------------|
| Configure Reasoning to load Frozen catalog version |
| Run production smoke on golden cases |
| Execute rollback to prior Frozen version |
| Monitor production knowledge consumption |

| May not |
|---------|
| Edit Frozen catalog in place |
| Release without Release Manager sign-off |

Engineering / platform operations role.

---

# 4.9 Role × stage matrix

| Stage | Primary | Assists | Approves |
|-------|---------|---------|----------|
| Idea | Product | Author | Chief Reviewer |
| Library | Author | Cursor | Domain Reviewer |
| Catalog | Author | Cursor | Domain Reviewer |
| QA | QA Assistant | Cursor | Domain Reviewer (accepts) |
| Review | Domain Reviewer | — | Domain Reviewer |
| Validation | Domain Reviewer | Reasoning gov | Domain Reviewer |
| Freeze | Chief Reviewer | Author | Chief Reviewer |
| Production | Production Owner | Engineering | Production Owner |
| Release | Release Manager | Production Owner | Release Manager |

Detail: [APPROVAL_FLOW.md](APPROVAL_FLOW.md).

---

END
