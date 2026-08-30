# UI-20 Binding audit

No adapter semantic changes. No Narrative / Presentation / Runtime edits.

| Issue | Status | Notes |
|-------|--------|--------|
| ResultStore empty vs current boot | Already correct | `resolveResultBoot(null)` → `resultSource: "empty"` gate. Stored payload with `data` → `current`. `?preview=1` remains explicit. |
| UI-11 live Interpretation | Bound | Production `/result` uses `selectNarrativePresentation` → InterpretationCard lead = consulting_flow. Report uses the same Presentation field once. |
| UI-12 Action warnings / expand | Bound | ActionPlanCard renders adapter `warnings` and `extraActions` behind the existing toggle. Copy is Presentation. |
| Identity solar date | Display format only | Header shows DD/MM/YYYY from ISO `solar_birth`. Adapter still stores the published string. |
| Analysis id in identity status | Accepted | Customer label "Mã phân tích". Not a rule/knowledge id. |

No binding defect required a semantic contract change. If a missing field is absent from Presentation, the UI omits or uses the approved empty state.
