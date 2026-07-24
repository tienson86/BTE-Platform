# Portal i18n

UI strings for the Customer Portal live in locale JSON files here.

| File | Locale |
|------|--------|
| `vi.json` | Vietnamese (default) |
| `en.json` | English (add later) |
| `zh.json` | Chinese (add later) |

## Usage

- Server embeds the active catalog as `window.__BTE_I18N__` (default `vi`).
- Client helper: `BteI18n.t("nav.dashboard")`, `BteI18n.apply()`, `BteI18n.setLocale("en")`.
- Templates use `data-i18n="…"`, `data-i18n-placeholder="…"`, `data-i18n-aria-label="…"`, etc.

Do **not** translate brand names: **BTE Platform**, **BTE Portal**.
Keep technical format labels: **HTML**, **Markdown**, **PDF**.
