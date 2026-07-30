# BTE Analysis Console

React + TypeScript + TailwindCSS frontend for the Analysis Engine API.

## Features

- Dashboard
- Chart Input
- Chart Viewer
- Analysis Viewer
- Interpretation Viewer
- Luck Viewer
- PDF Download
- Dark Mode
- Responsive layout

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
