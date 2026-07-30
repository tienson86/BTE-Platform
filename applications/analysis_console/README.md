# BTE Analysis Console

React + TypeScript + TailwindCSS frontend for the Analysis Engine API.

## Sprint 2 Features

- Project Dashboard
- Recent / Favorite / Pinned Charts
- Search Charts
- Customer History
- Analysis Timeline
- Export / Import
- Settings
- User Profile
- Visual BaZi Chart (SVG, hover, tooltip, highlight, dark mode)
- Responsive layout
- Dark mode
- Accessibility (skip link, focus rings, ARIA)
- Performance (lazy routes, deferred search)

## Prerequisites

1. Analysis API on port 8001:

```bash
uvicorn engines.analysis_engine.api.app:app --reload --port 8001
```

2. Node.js 20+

## Setup

```bash
cd applications/analysis_console
npm install
npm run dev
```

Open http://127.0.0.1:5173

Vite proxies `/api` and `/health` to the Analysis API.

## Build

```bash
npm run build
npm run preview
```

## Notes

- Chart library, timeline, customers, settings, and profile persist in `localStorage`.
- Creating a chart (with auto-save enabled) adds it to the project library.
