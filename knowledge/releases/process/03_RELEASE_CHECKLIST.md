# 03 — Release Checklist

Version: 1.0.0  
Status: **OFFICIAL**  
Date: 2026-08-08  
Use: One checklist per Commercial version / RC cut  

---

## Header

| Field | Value |
|-------|-------|
| Commercial version | e.g. Commercial V1 |
| RC label | e.g. RC1 |
| Owner | |
| Date | |

Mark each item: ☐ Done · ☐ N/A · ☐ Open

---

## 1. Architecture

- [ ] Architecture freeze documents reviewed (`knowledge/releases/v1/` as applicable)  
- [ ] No unauthorized engine / layer boundary changes  
- [ ] Dependency direction respected  

---

## 2. Foundation

- [ ] Foundation / Design System / Visual Language not casually modified  
- [ ] Any Foundation change has explicit Product + architecture approval  

---

## 3. Capabilities

- [ ] In-scope Capabilities listed in Capability Registry  
- [ ] Capability stages accurate (Released / Frozen / etc.)  
- [ ] Out-of-scope Capabilities not silently enabled  

---

## 4. Knowledge

- [ ] Required Knowledge Units approved for in-scope Capabilities  
- [ ] Wave / Domain freezes respected (no unauthorized edits)  
- [ ] Allow-lists match intended Capabilities only  

---

## 5. Narrative

- [ ] Narrative enrich-only rules respected (no Interpretation replace)  
- [ ] Primary / secondary recommendation policy for this version documented  
- [ ] No Narrative Engine redesign without approval  

---

## 6. Portal

- [ ] Result delivery uses approved surfaces (no unauthorized new routes/layouts)  
- [ ] Capability framing present as required by version polish rules  
- [ ] Design System compliance checklist considered  

---

## 7. QA

- [ ] Module tests for touched areas PASS  
- [ ] Commercial / Domain QA reports attached  
- [ ] Known defects triaged (P0/P1/P2)  

---

## 8. Regression

- [ ] Prior Released Capabilities still PASS  
- [ ] Wave 1.1 / core commercial path regression PASS  
- [ ] No Golden Dataset mutation to force green  

---

## 9. Registry

- [ ] Capability Registry reflects truth  
- [ ] Product Changelog updated for capability events  
- [ ] Roadmap status consistent  

---

## 10. Release Notes

- [ ] Capability release notes exist for new/changed Capabilities  
- [ ] Commercial version release notes drafted (finalized only after GO)  
- [ ] Non-goals / exclusions listed  

---

## 11. Documentation

- [ ] Domain reports complete for in-scope work  
- [ ] RC human review package published  
- [ ] Release Management process followed (this pack)  

---

## Roll-up

| Field | Value |
|-------|-------|
| Open P0 checklist items | |
| Ready for Human Review? | Yes / No |
| Ready for Product Approval? | Yes / No |

---

END
