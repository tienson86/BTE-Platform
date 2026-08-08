# 01 — Release Workflow

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Owner: BTE Product  

---

## 1. Purpose

Define the permanent workflow for every Commercial version release.

---

## 2. Official workflow

```
Development
    ↓
Release Candidate
    ↓
Human Review
    ↓
Release
    ↓
Maintenance
    ↓
Next Version
```

---

## 3. Stage definitions

### 3.1 Development

- Scope locked to Capability Registry + Product Roadmap.  
- Architecture / Foundation freezes respected.  
- Engineering implements wiring, tests, Domain content as authorized.  
- Capability stages follow `knowledge/product/02_CAPABILITY_RELEASE_POLICY.md`.  
- Exit: Engineering Gate + Golden Case Gate ready for RC cut.

### 3.2 Release Candidate

- Tag / label Commercial version as **RCn** (e.g. Commercial V1 RC1).  
- Freeze feature scope for that RC (no new Capability unless Product reopens scope).  
- Publish RC review package under `knowledge/product/release_candidate/` (or successor).  
- Exit: package complete; Human Review scheduled.

### 3.3 Human Review

- Consulting reviewers run Case Checklist + Scoring + Acceptance forms.  
- Commercial Quality Gate + Human Consulting Gate evaluated.  
- Exit: signed consulting acceptance (PASS / PASS WITH MINOR FIXES / REJECT).

### 3.4 Release

- Product Approval Gate records **GO** or **GO WITH MINOR FIXES**.  
- Changelog + Commercial version release notes updated.  
- Announce only after Product sign-off.  
- Exit: Commercial version marked **Released** in Product Changelog / decision form.

### 3.5 Maintenance

- Bug fix, quality improvement, knowledge revision per Post-Release Policy.  
- Hotfixes per Hotfix Policy.  
- Capability expansion is **not** casual maintenance — requires planning for next version or explicit minor scope.

### 3.6 Next Version

- Planning rules in `08_NEXT_RELEASE_PLANNING.md`.  
- Opens Development for V1.1 / V2 with new RC cycle.

---

## 4. Parallel tracks (do not confuse)

| Track | Question |
|-------|----------|
| **Capability track** | Is this consulting service Released on the Result path? |
| **Commercial version track** | Is the product bundle (e.g. Commercial V1) approved for announcement? |

Both must be green for a full commercial launch. Capability-only release without Commercial version GO is allowed for incremental wiring — announcement remains gated.

---

## 5. Roles in the workflow

| Role | Primary stages |
|------|----------------|
| Engineering | Development, RC prep, Maintenance/Hotfix |
| Knowledge / Domain | Development (authoring), Knowledge approval |
| Consulting Reviewer | Human Review |
| Product Owner | Scope lock, Product Approval, Next Version |

---

## 6. Commercial V1 position

```
Development ✓
    ↓
Release Candidate (RC1) ← current
    ↓
Human Review ← open
    ↓
Release ← not declared
    ↓
Maintenance
    ↓
Next Version (V1.1 / V2) ← do not start as substitute for RC1 sign-off
```

---

## 7. Stop line

Workflow is normative. Do not skip Human Review or Product Approval for Commercial version release.

---

END
