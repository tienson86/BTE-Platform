# Appendix Mapping

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## Source

`report.appendix` ← `presentation.appendix`

Layout `appendix` status = availability only.  
Adapter does not invent scope/limits chrome as content (those would be i18n — PX-2 chooses **hide if empty** rather than static appendix filler).

---

## Fields

| ui_id | contract_path | type | required | nullable | default | visibility | format | owner |
|-------|---------------|------|----------|----------|---------|------------|--------|-------|
| Appendix.scope | report.appendix.scope | string | no | yes | null | hidden_if_empty | sentence | Appendix |
| Appendix.reread | report.appendix.reread | string | no | yes | null | hidden_if_empty | sentence | Appendix |
| Appendix.limits | report.appendix.limits | string | no | yes | null | hidden_if_empty | sentence | Appendix |

Title: `i18n.section.appendix.title` only if section visible.

---

## Visibility

All three null → **hidden**. No blank appendix card.

---

## Forbidden

- Dumping technical metadata here (belongs in Technical)  
- New Primary CTA  

END
