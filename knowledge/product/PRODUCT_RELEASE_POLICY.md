# Product Release Policy

| Field | Value |
|-------|-------|
| Document | PRODUCT_RELEASE_POLICY |
| Version | 1.0.0 |
| Status | **OFFICIAL** |
| Date | 2026-08-17 |
| Owner | Product Owner |
| Current V1 state | **Beta0 Freeze** |

A release is permission for a build to leave the company at a stated state.
Engineering completion does not create that permission.

---

## 1. Release states

| State | Meaning | Customer exposure |
|-------|---------|-------------------|
| **Research** | Questions and constitutions. No product claim. | None |
| **Internal** | Used inside the company. May be incomplete. | Staff only |
| **Alpha** | Limited internal or appointed review of a consultation shape. Not a sales state. | Appointed reviewers only |
| **Beta0 Freeze** | Platform locked. Official V1 governance state as of 2026-08-17. | None as sale |
| **Beta** | Stabilisation of the consultation on the frozen platform. | Invited cases / appointed review, not general sale |
| **Release Candidate** | Intended commercial consultation, pending final acceptance | Appointed commercial and consulting review |
| **Production** | Sold under the BTE name | Paying customers |
| **Emergency Patch** | Production-only repair of a severe defect on the frozen path | Existing Production customers |
| **Hotfix** | Narrow Production repair, smaller than Emergency Patch, same controls | Existing Production customers |

V1 did not run a public Alpha programme.
Alpha remains a defined state for any future limited review that is not yet Beta.

Capability stages in `02_CAPABILITY_RELEASE_POLICY.md` (Proposed → Production → Frozen) describe capability maturity.
They do not override these product release states.

---

## 2. Approval requirements

| State | Engineering | Editorial | Commercial | Product Owner | Customer Pilot |
|-------|-------------|-----------|------------|---------------|----------------|
| Research | Not required as ship gate | Not required | Not required | Optional | No |
| Internal | Required for anything demoed as “working” | Required if shown as a reading | No | No for private drafts; **Yes** if called customer-ready | No |
| Alpha | Yes | Yes if customer language is shown | No | Yes to open Alpha | Appointed only |
| Beta0 Freeze | No code required to declare freeze | Baseline recorded | Baseline recorded | **Yes** to accept freeze pack | No |
| Beta | Yes | Yes on regenerated artifacts | Yes on anchors | **Yes** each Beta issue | Named real cases; not public sale |
| Release Candidate | Yes | **PASS** | **PASS** | **Yes** | Required as consulting review |
| Production | Yes | **PASS** | **PASS** | **Yes** | **PASS** |
| Emergency Patch | Yes, scoped | Yes if prose or PDF changes | Yes if customer meaning changes | **Yes** before issue | No new pilot if scope is repair-only |
| Hotfix | Yes, scoped | Yes if prose or PDF changes | Yes if customer meaning changes | **Yes** before issue | No |

No skip from Internal or Alpha to Production.
No Production without Product Owner signoff.
No Emergency Patch or Hotfix that introduces Architecture change without a prior Architecture approval.

---

## 3. Mandatory evidence (Beta and later)

Before issue:

1. Golden Dataset regenerated for frozen cases
2. Executive PDFs regenerated
3. Professional PDFs regenerated for production anchors
4. No engine language, glossary dump, duplicate recommendations, or broken fragments
5. Editorial review PASS
6. Commercial review PASS
7. Product Owner approval recorded

Checklist: `beta/BETA0_RELEASE_CHECKLIST.md`
Signoff: `beta/BETA0_SIGNOFF.md`

---

## 4. Emergency Patch and Hotfix

Both are Production repair states.

| | Emergency Patch | Hotfix |
|--|-----------------|--------|
| Use | Severe incorrect truth, broken artifact, or harmful customer language already in Production | Narrow defect, same class, smaller blast radius |
| Allowed work | Bug, Editorial, Knowledge, Engine-within-owner | Same |
| Forbidden | New subsystem; Golden Dataset rewrite to hide drift | Same |
| Done | Still Artifact First if the customer artifact changed | Same |

If the repair needs a new system, it is not a patch.
It is Architecture, and it is not issued as Emergency or Hotfix.

---

## 5. Naming

A build’s product state is the state the Product Owner signed.
A branch name, a document title, or a test job name does not set the state.
