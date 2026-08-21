# G2-06 — History acceptance

G2-05 persistence architecture is unchanged. This gate only verified the customer journey against that freeze.

## Write once

Successful Analyze → exactly one History row for that `analysis_id`.

Refresh / Report / PDF / DOCX / Print do **not** append (G2-05 ResultStore).

Failed Analyze (422) never calls `saveLastResult`.

## Isolation

Sequence under test:

1. Analyze Dũng → A = `g2-06-9`
2. Analyze Tuyền → B = `g2-06-4` (current)
3. Open History A → Dụng Thủy · Nhâm · Thực Thần
4. History PDF/DOCX filenames `Ngo_Dac_Dung_19850918` — not Tuyen
5. Normal `/result` remains B

Vitest: History Dũng UI does not contain Tuyền Dụng; current Tuyền has no History banner.

## Immutable + re-analyze

Re-analyze Dũng birth created `g2-06-reanalyze-dung` (C). Snapshot A still holds Dũng Dụng. A was not overwritten.

## Safety states (reconfirmed)

| State | Customer |
|-------|----------|
| Missing id | Không tìm thấy hồ sơ — not current |
| Corrupt snapshot | Safe error — not current, not mock |
| Old / unversioned contract | Version notice + Re-analyze — no silent migration |
| Empty current | Empty gate + Analyze CTA |

## Persistence behavior (documented, not redesigned)

Current + History live in browser `localStorage` / `sessionStorage`. `HISTORY_LIMIT = 30`, newest first. A page/session restart keeps History if the origin store is intact. Session view pointer may reset as designed. No server History was added.
