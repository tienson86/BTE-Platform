# G2-05 — Current / History precedence

G2-01R order remains:

```
fresh current → explicit history → empty
```

This freeze clarifies lookup and isolation. It does not add “set as current”.

## Frozen order

1. **Fresh current** (`bte_last_result` + `bte_current_analysis_id`) on normal `/result`
2. **Explicit History** only when the URL is `?from=history&id=<canonical-id>` **and** that id matches a stored snapshot (`bte_view_result` **or** a `bte_history` row)
3. **Empty / missing / corrupt / contract** gates — never a silent substitute analysis

`?from=history` without `id` is not explicit History. Current wins.

## Isolation (required)

| Action | Current store | Display |
|--------|---------------|---------|
| Analyze A | A becomes current; A appended to History | `/result` shows A |
| Analyze B | B becomes current; A History row unchanged | `/result` shows B |
| Open History A | Current stays B | `/result?from=history&id=A` shows A |
| Refresh History URL | Current stays B | Still A (snapshot lookup by id) |
| Normal `/result` | Current still B | B |
| Back / Forward | No rewrite | Browser honors route/context. No SPA navigation rewrite |
| Report / PDF / DOCX / Print of History A | Current stays B | File/UI is A |
| Missing History id | Current stays B | “Không tìm thấy hồ sơ.” — not B |
| Corrupt History row | Current stays B | Safe error — not B |

Opening History must **not** replace `bte_last_result` or `bte_current_analysis_id`.

## Resolve APIs

- `load()` / `loadCurrent()` — current only
- `resolveForDisplay(fromHistory, expectedId)` — History snapshot or `null`; **never current** when `fromHistory` and `expectedId` are set
- `findHistoryById(id)` — view pointer, then History list
- `selectForView()` — session pointer only
- `loadForView()` — **legacy only** (`/result?legacy=1`)

## Visual state (G2-02 coherent)

| Mode | Banner / gate |
|------|----------------|
| Current ready | No History banner |
| Explicit History ready | “Đang xem kết quả đã lưu. Kết quả phân tích hiện tại không đổi.” |
| Old / incompatible History | Version gate only (no History banner) |
| Missing History | “Không tìm thấy hồ sơ.” + Về lịch sử |
| Corrupt History | “Không tải được kết quả đã lưu.” |

No simultaneous conflicting banners.

## Re-analyze

Creates a new current analysis and a new History row. Old History remains. Birth is taken from the stored snapshot (`/analyze?reanalyze=1&...`). Analyze is not invoked by opening History.
