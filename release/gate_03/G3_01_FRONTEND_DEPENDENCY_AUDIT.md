# G3-01 — Frontend dependency audit

Working directory: `applications/customer_portal`

| Item | Value |
|------|--------|
| Manifest | `package.json` (`@bte/commercial-ui-v3` 3.0.0) |
| Lock | `package-lock.json` lockfileVersion 3 — **present and used** |
| `engines` field | none |
| Proven Node / npm | v24.18.0 / 11.16.0 |
| Clean install | `npm ci` **PASS** (154 packages) |
| Production build | `npm run build:result` → `vite build --mode production` **PASS** |
| Output | `static/dist/result.js`, `result.css`, `report.js`, hashed chunks |
| Result.js SHA256 after rebuild | `114A1761F94FF3EE4B8135F1E3B2D7C88C63D233E17B19B60472730D7DF4ECE5` |
| package-lock SHA256 | `EEB6C40C3A0A93953D51DB112C1B36712E828A2A366F6D450032FD4FD1EC8B21` |

G1-FINAL hashed an older `result.js` (`DE5BA497…`). Gate 2 rebuilt the customer Result bundle; G3-01 freeze hash is the post-G2 file. Rebuild in this gate matched that hash (deterministic for current source).

All npm dependencies are **devDependencies** (Vite/Vitest/React). Production serving is FastAPI static files, not a Node process.

`npm audit` reported 1 high severity. **Do not `npm audit fix` in G3-01** (would upgrade). Track as a G3-02 ops note.

Do not use `npm install` for production rebuild.
