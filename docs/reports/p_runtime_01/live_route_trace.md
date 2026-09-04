# P-RUNTIME-01 live route trace

Confirmed production path for `http://localhost:8081/result`.

```
POST http://127.0.0.1:8000/api/v1/analyze
  (portal customers use POST /backend/api/v1/analyze → Applications API)

↓

Analyze JSON body: { input fields..., data: AnalysisDataDto, analysis_id }

↓

applications/customer_portal/static/js/analyze.js
  BtePortal.post("/api/v1/analyze", payload)
  BtePortal.saveLastResult({ input, data, analysis_id })

↓

applications/customer_portal/static/js/result_store.js
  LAST_KEY = "bte_last_result"
  ResultStore.save → sessionStorage + localStorage

↓

window.location.assign("/result")

↓

applications/customer_portal/app.py
  GET /result
  if ?legacy=1 → result_legacy.html (explicit only)
  else → result_desktop.html

↓

templates/result_desktop.html
  /static/js/result_store.js?v=NREL03
  /static/js/api.js
  /static/js/ui/shell.js
  /static/dist/result.css?v=PRUNTIME01
  /static/dist/result.js?v=PRUNTIME01
  mount: #canonical-desktop-root

↓

src/entries/resultApp.tsx
  ResultStore.resolveForDisplay / loadCurrent
  resolveResultBoot
    resolveCurrentStoredResult (drops calendar ≠ G1-10C)
    customerContractStatus (UsefulGodView@1.5)
  if pathname /result and surface production
    → CommercialDashboardPage
  if ?narrative=v2-shadow|v2-compare
    → NarrativeV2ShadowPage (not production)
  /interpretation
    → PortalPage (not the customer /result dashboard)

↓

CommercialDashboardPage
  adaptIdentityHeader                    Identity + Cân Xương Region C
  selectNarrativePresentation            Overview / Interpretation / Action
    attachExecutiveFacts                 P-001
  adaptTenGodsCard                       P-003 + P-003B
  adaptLifeConsulting                    P-004
  DashboardGrid
    OverviewCard
    LifeConsultingSection (not a data-card)
    InterpretationCard
    ActionPlanCard
    TenGodsCard (commercial + combination)
    evidence cards

↓

browser DOM
  [data-dashboard="commercial-v1"]
  [data-narrative-surface="production"]
  [data-overview-section="facts"]
  [data-life-consulting]
  [data-tg-section="commercial"]
  [data-tg-combination]
  #sec-can-xuong (header only)
```

Vite entry: `applications/customer_portal/src/entries/resultApp.tsx`  
Vite output: `applications/customer_portal/static/dist/result.js` + `result.css`  
Command: `npm run build:result` in `applications/customer_portal`.
