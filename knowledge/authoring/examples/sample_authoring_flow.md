# Sample Authoring Flow

**Status:** Pedagogical example — not a real package and not Golden Dataset content.

Illustrates KD-4 states for a fictional analytical package `bz_99_demo_strength` (do not create this package in the Rule Database).

---

## 1. Idea

Author notes a gap: “document seasonal root heuristics as a future package.”  
No `package_id` collision with `01_strength_rules`. Reserve `bz_99_demo_strength`.

## 2. Draft

1. Copy `package_template/` → `bz_99_demo_strength/`.
2. Fill `PACKAGE.json` / `MANIFEST.json` from templates (`status=draft`, `package_type=analytical`, `domain_id=DOM-STRENGTH`).
3. Add rule objects from `RULE_TEMPLATE.json` with `enabled=false` until review.
4. Complete `checklists/draft_checklist.md`.

## 3. Internal Review

Peer checks README clarity and manifest exports.  
Approve → `technical_validation`. Findings would return to `draft`.

## 4. Technical Validation

Technical Reviewer specifies `PVP-STANDARD` stages 1–6 (+ quality technical floor).  
Assume pass. Author is not the technical approver.

## 5. Knowledge Review

Domain Reviewer checks claims vs sources / `TODO_REVIEW`.  
Target quality: Silver. Approve → `release_candidate` (`validated`).

Stop here for this sample. Release is in `sample_release_flow.md`.

---

## Parallel authoring note

Another author may draft `bz_98_demo_season` at the same time. Identifier ranges must not overlap. Publication order later sorts by `package_id`.
