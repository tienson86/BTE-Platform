# Adapter Design

Version: 2.0.0  
Status: **OFFICIAL — Design Only**  
Sprint: Phase X · PX-2

---

## 1. Single adapter

`bte.portal.presentation_adapter.v2`

One function conceptually: Report in → PortalResultModel out.

No per-engine Portal adapters for Result V2.

---

## 2. Why not PACK_04 engine ViewModels directly

PACK_04 allows engine presentation adapters. Those historically risk leaking Analysis/Score types into screens.

PX-2 tightens Result:

```
Engines → (already finished) → CanonicalReportResult
        → Portal Presentation Adapter
        → PortalResultModel
        → Components
```

React does not call Report Engine either. It consumes the model.

---

## 3. Internal steps

```
1 Receive CanonicalReportResult
2 Read success / errors / layout section status / artifact metadata
3 Read presentation envelope if present
4 Validate required Hero + Summary
5 Bind catalog 1:1
6 Resolve i18n chrome
7 Apply visibility + collapse defaults
8 Emit page.state
9 Return PortalResultModel
```

---

## 4. Extensibility

New life domain → new `report.domains.{key}` + i18n key + DomainSection instance.  
Do not add a side channel from Luck engine to UI.

New chart type → new item in `report.charts[]` with same card API.

---

## 5. Failure

Fail closed to user-safe Vietnamese. Never throw pipeline diagnostics at the reader.

---

## 6. Stop line

The adapter is a formatter and a gate — not a second Report Builder.

END
