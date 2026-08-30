# UI-16 Section Matrix

| Section | Executive (A) | Detailed (B) | Render rule | Empty |
|---------|---------------|--------------|-------------|-------|
| Cover | Brand, title, name, birth, date, version | — | Published identity only | Omit unpublished fields |
| Identity | Compact profile | Same block | DD/MM/YYYY, 24-hour time | Omit missing rows |
| Executive Summary | headline, summary, identity, balance, conclusion | — | Overview fields only | Omit section if all empty |
| Chart Snapshot | Compact Tứ Trụ, ngũ hành bars, pattern, current luck | — | Canonical adapters | Omit empty modules |
| Key Findings | 3–5 compact facts | — | Headline / pattern / strength / top priority / current luck | Omit section if none |
| Interpretation | `consulting_flow` | Observation, Reasoning, Meaning, Impact, Recommendation, Closing | No concatenation; no overview.summary replay | Omit empty zones |
| Action Plan | Top Priority | Actions, warnings, current period | Presentation wording unchanged | Omit empty blocks |
| Luck | — | Khởi vận, current, timeline, next | No tốt/xấu inference | Omit if unavailable |
| Supporting | — | Bát Tự, Ngũ Hành, Thập Thần, Mệnh Cục, Thần Sát | UI-15 `data-viz` kinds | Omit empty modules |
| Appendix | — | Method, disclaimer, versions, date | No evidence/rule/source ids | Always present; omit unpublished meta |

## No-duplication

- `consulting_flow` appears once.
- Overview `summary` stays in Executive Summary.
- Full Action Plan is not copied into Key Findings except Top Priority title.
