# UI Contracts (Documentation)

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## 1. Contract set

| ID | Role |
|----|------|
| `bte.portal.result_ui.v2` | Portal Result UI Contract (this sprint) |
| `bte.portal.presentation_adapter.v2` | Adapter identity |
| `bte.report.pipeline.v1` | RX-1 pipeline (input root; not edited) |
| `bte.report.foundation.v1` | RE-1 foundation (not edited) |

UI components depend only on `bte.portal.result_ui.v2`.

---

## 2. Compatibility

- Additive optional fields: allowed in a future minor PX contract  
- Removing/renaming `ui_id` or `contract_path`: major  
- Changing Vietnamese chrome: product copy change, same key preferred  

PX-2 does not bump Report pipeline versions.

---

## 3. Component ownership

Ownership tables in `FIELD_CATALOG.md` are normative.  
A PR that binds the same `report.*` path into two visible components fails review.

Domain sections may **display** recommendation cards by id reference without owning the source fields.

---

## 4. Field ownership vs experience ownership

PX-1 owns reading order and voice.  
PX-2 owns how fields arrive.  
Neither owns Engine truth.

---

## 5. Stop line

Contracts are the product–engineering handshake. Keep them small and strict.

END
