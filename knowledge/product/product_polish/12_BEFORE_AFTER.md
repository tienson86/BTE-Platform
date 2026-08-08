# 12 — Before / After · Result Consulting Experience

---

## Before (metadata / dashboard posture)

```
[ Context: profile | birth | chart id | status | timestamp ]  ← hero = metadata
[ Exec | Indicators | Destiny ]  ← equal weight, technical middle
[ Five Elements | Strength | Ten Gods ]
[ Radar | Timeline ]
[ Recommendations ]  ← late
[ Interpretation ]
[ Knowledge ]
```

First 15s risk: customer sees chart IDs and indicators before advice.

---

## After (consulting posture)

```
[ Identity: Who am I + name + birth ]
      └ technical meta collapsed
[ Executive Summary (hero) | Career direction ]
      └ CTAs: Read consultation · View analysis
[ Recommendations ]  ← What / Why / Outcome (+ expand How/When)
[ Strength → Elements → Ten Gods ]  ← strength first
[ Interpretation evidence ]
[ Charts / Timeline ]  ← reference
[ Knowledge ]
```

First 15s target: **Who** → **Situation** → **Career** → **What to do**.

---

## Screenshot capture

Live screenshots are environment-dependent. Capture with:

```bash
cd applications/customer_portal
npm run build:result
# open Result screenshot entry / Portal Result with sample analyze payload
```

Entry: `src/entries/resultPageScreenshotApp.tsx`

Recommended frames:

1. **Before-equivalent** — document prior composition (this file)  
2. **After · desktop** — Identity + Exec + Career + Rec in first scroll  
3. **After · mobile** — stacked, no horizontal overflow  
4. **After · meta expanded** — technical fields not in hero  

Store captures under:

`knowledge/product/product_polish/screenshots/`

Included concept frame: `screenshots/product_polish_v1_before_after.png`

---

## Visual diff (intent)

| Area | Before | After |
|------|--------|-------|
| Hero | Metadata grid | Identity statement |
| Summary | 3 equal cards | Exec dominant + Career |
| Rec position | After charts | Before analysis/charts |
| Empty | Possible blank cards | Hidden |
| CTA | Weak / late | Primary + Secondary in-page |

---

END
