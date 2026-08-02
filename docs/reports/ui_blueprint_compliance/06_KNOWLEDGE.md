# Tier 6 — Knowledge — Blueprint V1.1 Compliance

**Status:** REVIEW ONLY — no code changes  
**Blueprint refs:** Knowledge workspace wireframe, `19_BLUEPRINT_V1_1_FINAL_FREEZE.md`  
**UI sources:** `knowledge_workspace.js`, `presenters/discussion.js`, `report_render.js`, `report.css`, `vi.json`  
**Illustration:** [`../ui_sprint06_knowledge/preview/knowledge_light.html`](../ui_sprint06_knowledge/preview/knowledge_light.html) · [`knowledge_dark.html`](../ui_sprint06_knowledge/preview/knowledge_dark.html)

---

## Blueprint target

| Item | Requirement |
|------|-------------|
| Flow | Insight → Evidence → … → Related (workspace path) |
| Evidence | Expert sources as EvidenceRow components |
| i18n | Full VI; no hard-coded EN chrome |
| Forbidden | EN “Insight” / Expert labels; free-form EN in discussion presenter |

---

## Checklist by dimension

| Dimension | Verdict | Notes |
|-----------|---------|-------|
| Information Architecture | ⚠ | Workspace path mostly present; sources pane not EvidenceRow |
| Visual Hierarchy | ✓ | Insight primary then evidence |
| Reading Flow | ⚠ | Expert chrome wording breaks VI flow |
| Spacing | ✓ | Soft workspace |
| Typography | ⚠ | EN labels |
| Component Hierarchy | ⚠ | `knowledge_workspace.js` + `discussion.js` EN strings |
| Binding | ⚠ | Sources not normalized to EvidenceRow |
| Empty State | ✓ | Empty panes handled |
| Localization | ✗ | Hard-coded EN in discussion / Expert chrome |
| Visual Grammar | ✓ | Soft knowledge workspace |

---

## Findings

### T6-01 — Knowledge workspace shell (Insight → … → Related)
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `knowledge_workspace.js` |
| **File** | `applications/customer_portal/static/js/report/knowledge_workspace.js` |
| **Illustration** | Sprint06 preview |
| **Evidence** | Multi-pane knowledge flow implemented |

### T6-02 — Expert sources not EvidenceRow
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Major** |
| **Component** | Sources pane / Expert list |
| **File** | `knowledge_workspace.js` |
| **Illustration** | Sprint06 sources area |
| **Gap** | Blueprint: EvidenceRow for evidence/sources. UI uses ad-hoc Expert chrome |
| **Fix recommendation** | Render sources as EvidenceRow list consistent with Evidence pane |

### T6-03 — EN “Insight” / Expert chrome
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Major** |
| **Component** | Pane titles / Expert labels |
| **File** | `knowledge_workspace.js`, `vi.json` (missing keys) |
| **Illustration** | Sprint06 EN labels |
| **Gap** | Customer UI must be VI; English pane chrome violates localization freeze |
| **Fix recommendation** | Add `report.knowledge.*` VI keys; remove EN defaults |

### T6-04 — Hard-coded English in `discussion.js`
| | |
|--|--|
| **Symbol** | ✗ Sai Blueprint |
| **Severity** | **Critical** |
| **Component** | `presenters/discussion.js` |
| **File** | `applications/customer_portal/static/js/presenters/discussion.js` |
| **Illustration** | Knowledge/discussion copy when presenter used |
| **Gap** | Hard-coded EN strings in presenter path — not blueprint-localized |
| **Fix recommendation** | Route all user-visible strings through i18n; delete EN literals |

### T6-05 — Soft knowledge visual grammar
| | |
|--|--|
| **Symbol** | ✓ Đúng Blueprint |
| **Severity** | — |
| **Component** | `.bte-knowledge*` |
| **File** | `report.css` |
| **Illustration** | Sprint06 light/dark |
| **Evidence** | Soft workspace; restrained expert UI |

---

## Tier 6 scorecard

| Area | Score |
|------|-------|
| Workspace shell | PASS |
| EvidenceRow / i18n | FAIL |
| **Tier verdict** | **WARN** |

**Needs fix:** T6-04 (Critical); T6-02, T6-03 (Major).
