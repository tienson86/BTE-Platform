# UI Review Checklist — PX-2 Binding

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Date: 2026-08-09  
Sprint: Phase X · PX-2  
Use: Future implementation reviews

Also run PX-1 `UI_REVIEW_CHECKLIST.md` and Foundation compliance.

---

## 1. Contract

| Item | Status |
|------|--------|
| Consumes only `bte.portal.result_ui.v2` / PortalResultModel | □ |
| No Analysis / Decision / Luck / Interpretation types in UI | □ |
| No Artifact `content` on Result Page | □ |
| Every visible content field in FIELD_CATALOG | □ |
| One contract_path per ui_id | □ |
| One component_owner per field | □ |

---

## 2. Adapter

| Item | Status |
|------|--------|
| Formatting only — no business logic | □ |
| Does not reconstruct envelope from engine snapshots | □ |
| `module_id` / `source_refs` never rendered | □ |
| Summary clamped to 5 | □ |

---

## 3. State / visibility

| Item | Status |
|------|--------|
| Page states per machine | □ |
| Technical + Knowledge collapsed by default | □ |
| Charts hidden if empty | □ |
| Warnings hidden if empty | □ |
| Appendix hidden if empty | □ |
| No blank cards | □ |
| Domains keep order with Empty cards | □ |

---

## 4. CTA / language

| Item | Status |
|------|--------|
| Exactly one Primary | □ |
| Disabled/loading rules | □ |
| All chrome Vietnamese from i18n catalog | □ |
| No English labels | □ |

---

## 5. Lifecycle

| Item | Status |
|------|--------|
| Receive → Validate → Bind → Format → Render → Expand → Dispose | □ |
| Expand does not fetch engines | □ |

---

## 6. Stop line

Use when PX-2 is implemented. This sprint is design only.

END
