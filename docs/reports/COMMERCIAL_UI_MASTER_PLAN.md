# COMMERCIAL UI V2.0 — MASTER PLAN

| Field | Value |
|-------|--------|
| **Document** | `COMMERCIAL_UI_MASTER_PLAN.md` |
| **Status** | **APPROVED — V2 PRESENTATION IMPLEMENTED** |
| **Date** | 2026-08-02 |
| **Scope** | Customer Portal **Result** presentation layer only |
| **Stack** | Jinja + vanilla JS + CSS (no React; no new framework) |
| **Forbidden** | Backend · Engine · API · Database · Binding Index · new business logic |

---

## 0. Product verdict (why this exists)

Sprint 01–06 each shipped a valid **module**.  
Assembled together, the Result page still reads as **six dashboards stitched together**.

**Rejected feeling:** admin panel · widget wall · developer layout · tier chrome competition  
**Target feeling:** one premium BaZi consultation report — calm, elegant, readable, continuous

This redesign is **presentation only**. Same data. Same bindings. New reading experience.

**Do not implement until this plan is explicitly approved.**

---

## 1. Whole page hierarchy

### 1.1 Mental model

```
ONE REPORT DOCUMENT
├── Cover (Hero)           → identity + verdict + action in ≤3s
├── Chart Heart (Pillars)  → visual BaZi centerpiece
├── Insight Support        → metrics as prose-first, charts secondary
├── Reasoning              → analysis as conclusion→evidence essays
├── Narrative Book         → interpretation as chapters
└── Appendix               → knowledge / evidence library
```

Tiers 1–6 remain **anchor IDs** for navigation and Binding Index compatibility.  
They must **not** look like six products. They share one canvas, one type system, one rhythm.

### 1.2 Page chrome (outside the report body)

| Layer | Role | Visual weight |
|-------|------|----------------|
| App header | Brand + account only | Minimal |
| Navigation rail | Jump links + scroll spy | **Secondary** (see § sidebar) |
| Report stream | The product | **Primary** — max ~720–820px measure for prose; wider only for pillars/charts |
| Footer / actions | Print / save / back (if exist) | Quiet |

### 1.3 Stream order (unchanged product order, new visual merge)

1. **Hero** — cover page energy, still first viewport  
2. **Pillars** — no “Tier 2 card wall”; soft chapter break only  
3. **Metrics** — insight strip + small visuals  
4. **Analysis** — long-form reasoning blocks  
5. **Interpretation** — book chapters  
6. **Knowledge** — appendix tone  

### 1.4 What disappears from hierarchy

- Per-tier “large card shells” competing as separate apps  
- Heavy `rpt-tier-head` bands that announce “module starts here”  
- Repeated KPI tiles already shown in Hero  
- Badge rows as primary decoration  
- Nested card → card → accordion → card stacks  

### 1.5 Dominance ladder (what the eye must find first)

| Rank | Element | Where |
|------|---------|--------|
| 1 | Day Master / identity | Hero |
| 2 | Quality verdict | Hero |
| 3 | First recommendation | Hero (above fold) |
| 4 | Day Pillar | Pillars |
| 5 | Analysis conclusions | Analysis |
| 6 | Chapter titles | Interpretation |
| 7 | Charts | Metrics (support only) |
| 8 | Rail labels | Sidebar |

---

## 2. Spacing system

### 2.1 Principle

**Whitespace is structure.**  
If content feels compressed, spacing is wrong — not “add another border.”

### 2.2 Token scale (V2 — presentation tokens only)

Propose additive tokens in presentation CSS (names illustrative; exact values locked at implementation after approval):

| Token | Role | Direction vs V1 |
|-------|------|-----------------|
| `--rpt-space-xs` | Inline gaps | Keep tight |
| `--rpt-space-sm` | Label → value | Slightly open |
| `--rpt-space-md` | Paragraph gap | **+** |
| `--rpt-space-lg` | Block gap inside section | **++** |
| `--rpt-space-xl` | Subsection break | **++** |
| `--rpt-space-2xl` | Section → section (merged stream) | **+++** (replaces “card margin stack”) |
| `--rpt-space-3xl` | Chapter / major narrative break | Book-like pause |
| `--rpt-pad-block` | Section body padding | Prefer vertical > horizontal chrome |
| `--rpt-measure` | Prose max-width | ~65–72ch |

### 2.3 Vertical rhythm rules

1. **Section breath:** major sections get `--rpt-space-2xl`–`3xl` before the next heading — not a boxed divider.  
2. **Inside Analysis blocks:** Conclusion / Explanation / Evidence / Rule / Confidence / Knowledge separated by consistent `--rpt-space-md`–`lg`, never packed.  
3. **Hero:** Extra air under identity and under verdict; metrics as a single quiet row; recommendation with clear isolation.  
4. **No density stacking:** forbid “card padding + nested card padding + accordion padding” compounding. One padding owner per surface.

### 2.4 Horizontal rhythm

- Report stream centered with generous side margins.  
- Rail does **not** steal optical center; content remains the page’s gravity.  
- Pillars may use full stream width; prose sections stay on `--rpt-measure`.

---

## 3. Typography hierarchy

Typography becomes the **primary** hierarchy system. Borders/backgrounds/badges become optional accents.

### 3.1 Type roles

| Role | Use | Feel |
|------|-----|------|
| **Display** | Day Master / Hero identity | Immediate impact |
| **Title L** | Major section titles (once per section) | Calm chapter mark |
| **Title M** | Analysis block conclusion / chapter title | Readable authority |
| **Title S** | Subheads (Explanation, Evidence…) | Quiet structure |
| **Body L** | Interpretation narrative | Book comfort |
| **Body** | Analysis explanation | Default reading |
| **Body S** | Evidence, rule refs, captions | Secondary |
| **Meta** | Dates, place, confidence, rail | Lowest contrast still accessible |
| **Numeric** | Strength / scores (sparse) | Tabular, restrained |

### 3.2 Hierarchy rules

1. **One Display element per viewport** (Hero identity).  
2. Section titles use type + spacing — **not** icon+badge+border+shadow.  
3. Line height: body ≥ 1.6; book narrative ≥ 1.65–1.75.  
4. Paragraphs: short–medium; break walls of text into breathing blocks.  
5. Prefer VI-first labels already in i18n; no EN developer chrome.

### 3.3 Font direction (presentation)

Keep portal stack unless a later approved pass adds a report-specific family.  
V2 emphasis is **scale, weight, measure, and leading** — not a font fashion rewrite.

Avoid: Inter-as-everything dashboard look via tiny caps labels + pill badges.

---

## 4. Visual hierarchy

### 4.1 Surface stack (simplified)

| Level | Name | Allowed |
|-------|------|---------|
| **S0** | Page canvas | Flat, calm background |
| **S1** | Continuous report sheet | Optional single soft sheet OR open canvas — **not** six sheets |
| **S2** | Rare emphasis surface | Hero wash · Day pillar · First recommendation only |
| **S3** | Overlay | Modals only (unchanged product chrome) |

**Forbidden:** Every module at S2 (current “tile wall”).

### 4.2 Accent scarcity

Keep Blueprint accent grammar (Day / Dụng / Hỷ / Kỵ / Thân / rail active) but **scarcer**:

- Accents mark meaning, not decoration.  
- Default everything else neutral ink on calm ground.  
- No rainbow borders on metric tiles.

### 4.3 Elevation & shadow

- Cut soft shadows aggressively; prefer flat + type.  
- At most: Hero recommendation · Day pillar · (optional) one appendix panel.  
- Shadow must not define every block.

### 4.4 Icon policy

- Rail: small, monochrome, secondary.  
- Section heads: icon optional or removed if title is clear.  
- No emoji product chrome.  
- No “status badge festival.”

---

## 5. Section transitions

### 5.1 Goal

User scrolls one document. Transitions feel like **chapter turns**, not **app switches**.

### 5.2 Transition grammar

| From → To | Transition |
|-----------|------------|
| Hero → Pillars | Soft title + increased space; no heavy tier card frame |
| Pillars → Metrics | Thin hairline **or** space-only; metrics open with a one-line insight sentence before charts |
| Metrics → Analysis | Clearer pause (`--rpt-space-3xl`); Analysis starts with first **Conclusion** |
| Analysis → Interpretation | Book shift: measure, leading, quieter chrome; TOC as marginalia |
| Interpretation → Knowledge | Appendix tone: smaller titles, denser but still calm; “Phụ lục / Tri thức” voice |

### 5.3 Remove “tier product chrome”

Current `rpt-tier` + large bordered shell + tier hint chip stack will be redesigned to:

- Anchor `id` retained for rail / Binding Index  
- Visual: section title + optional one-line purpose — **no** module dashboard frame  
- Tier hints demoted to meta or removed from primary path  

### 5.4 Motion

Keep Blueprint motion limits (short fade/rise).  
No parallax, no KPI carousels, no looping pulses.  
Scroll-spy rail updates calmly.

---

## 6. Card reduction plan (≥40% fewer visible cards)

### 6.1 Definition

A **visible card** = bordered and/or shadowed rectangle that frames a content group as a widget.

### 6.2 Inventory intent (current → V2)

| Area | Current tendency | V2 target |
|------|------------------|-----------|
| Hero metric tiles | Many small cards | **0–1** surfaces: text/metric row, not tile grid |
| Hero recommendation | Card | Keep **one** emphasis surface (allowed) |
| Pillars | Column cards + badge rows | **One** composition; Day emphasized; no per-cell cards |
| Metrics | Chart cards + summary grid cards | **≤2** light panels OR open layout; drop unbound SummaryMetricGrid chrome |
| Analysis | Card-per-block + nested | **Open blocks** with typographic sections; card only if interaction needs containment |
| Interpretation | Chapter cards | **Book pages** — headings + prose; TOC not a card stack |
| Knowledge | Multi-pane cards | **Appendix panels** minimized; prefer list/prose |

### 6.3 Hard rules

1. **Only important information gets a card.**  
2. **No nested cards.**  
3. **No card-inside-card.**  
4. Duplicate metric cards already in Hero → **delete from later sections** (presentation dedupe; same binding may feed Hero only on Result stream).  
5. Unbound / empty card chrome → **do not render** (Unavailable as quiet text, not empty widget).

### 6.4 Success metric

Count bordered/shadowed content frames on a typical populated Result:

- Baseline: current production CSS patterns (`rpt-large-card`, metric tiles, pillar cards, chart cards, analysis cards, etc.)  
- Target: **≥40% reduction** in visible card count on the same payload  

---

## 7. Border reduction plan (≥50%)

### 7.1 Principle

Borders are the loudest “dashboard” signal in the current `report.css`.  
Replace most borders with **spacing + typography + rare hairlines**.

### 7.2 Replace map

| Current pattern | V2 replacement |
|-----------------|----------------|
| 1px border on every section shell | Space + title |
| Border on every metric tile | Plain text / soft divider |
| Border on every pillar column | Column gutter + Day emphasis only |
| Border on every analysis accordion | Open block; optional top hairline |
| Badge pill borders | Text meta or remove |
| Dashed “unavailable” bordered boxes | Quiet em dash / muted sentence |
| Nested border stacks | Single optional hairline max |

### 7.3 Allowed borders (scarce)

- Optional **one** hairline under section titles  
- Day pillar subtle outline **or** wash (pick one, not both heavy)  
- Focus rings (a11y) — keep  
- Form controls outside Result — unchanged  

### 7.4 Success metric

On representative Result screenshot / DOM audit:

- Count `border:` / visible box edges around content  
- Target: **≥50% fewer** decorative borders vs current report styles  

---

## 8. Component merge plan

Presentation merges only — **no new business widgets**, no Binding Index changes.

### 8.1 Merge / demote

| Current | V2 action |
|---------|-----------|
| Six `rpt-tier` mega-cards | Merge into **one report stream**; keep IDs |
| Hero 2×3 metric cards + later metric repeats | **Single glance row** in Hero; Metrics section interprets, doesn’t re-tile |
| SummaryMetricGrid (unbound / noisy) | **Remove from Result presentation** (or hide until bound — prefer remove chrome) |
| Pillars DayMasterRelation extra block | **Out of Pillars surface** (avoid duplicate narrative; Analysis/Knowledge already own reasoning) |
| Pillar badge rows | Collapse metadata; progressive disclosure |
| Analysis nested cards + essay dumps | **One block template:** Conclusion → Explanation → Evidence → Rule → Confidence → Knowledge |
| Interpretation exec duplicate of Ch.1 | **One opening** — teaser XOR chapter body |
| Knowledge multi-card Expert chrome | Appendix list; Evidence rows as clean lines, not widget kit |
| Heavy rail “product panel” | Slim secondary nav |

### 8.2 Keep (structure, restyle)

| Module | Keep why |
|--------|----------|
| `report_model.js` | Binding / model — do not change contracts |
| `report_render.js` | Orchestration — restyle wrappers |
| `pillars.js` / `metrics.js` / `analysis.js` / `interpretation_doc.js` / `knowledge_workspace.js` | Same data regions; new markup/CSS density |
| Rail + scroll spy | Navigation aid, quieter CSS |
| i18n keys | Prefer existing VI; fix EN leaks in presentation strings only if needed for calm UI |

### 8.3 Explicit non-goals

- No new chart types  
- No new badge systems  
- No new KPI widgets  
- No React migration in this redesign  
- No Engine/API/DB work  

### 8.4 Compliance carry-forward (presentation fixes that serve V2)

From Blueprint compliance audit — absorb only as **presentation** work aligned with this plan (not a separate bug sprint mindset):

- Hero FirstRecommendation above fold  
- Pillars missing → `--`  
- Metrics calm layout (not dashboard 2×2 fetish if it fights report feel — **report feel wins**; charts smaller)  
- Analysis default primary blocks + no pattern-rules wall  
- Interpretation B.3 alignment / dedupe  
- Knowledge VI + clean evidence lines  

> Note: Commercial V2 may **supersede** “dashboard ChartBand 2×2” if that layout recreates admin feeling. Product priority: **consultation report continuity** over sprint wireframe literalism.

---

## 9. Responsive strategy

### 9.1 Breakpoints (presentation)

| Viewport | Layout |
|----------|--------|
| **Desktop (≥1100)** | Slim rail + continuous report stream |
| **Tablet** | Rail collapses to top/horizontal jump or drawer; stream full width |
| **Mobile** | Single column; Hero stacked for ≤3s comprehension; Pillars horizontal scroll **or** stacked with Day first; charts reduced height; book measure full width with comfortable padding |

### 9.2 Rules

1. Never recover density by adding borders on small screens.  
2. Prefer collapse/hide secondary metadata over wrapping badge clouds.  
3. Touch targets for rail/TOC remain accessible; visuals stay quiet.  
4. Print (if supported later): stream-first, rail hidden — plan assumes print-friendly document structure.

### 9.3 Above-the-fold contract (desktop)

Hero must deliver within first viewport:

- Who (identity / Day Master)  
- Strong/weak quality signal  
- Overall quality verdict  
- Main recommendation  

Metrics glance may remain if it does **not** push recommendation below fold — otherwise demote glance below recommendation.

---

## 10. Reading journey

### 10.1 Emotional arc

| Time | User should feel | Sees |
|------|------------------|------|
| 0–3s | “This is about me; I know the verdict.” | Hero impact |
| 3–20s | “This is my chart — beautiful, clear.” | Day-dominant pillars |
| 20–45s | “I understand balance without studying charts.” | Short metric insight + small visuals |
| 45–120s | “Someone reasoned this carefully.” | Analysis conclusion→evidence |
| 2–6 min | “I’m reading a consultation.” | Interpretation book |
| Later | “I can verify sources calmly.” | Knowledge appendix |

### 10.2 Anti-journey (forbidden)

- Jumping between six admin modules  
- Re-reading the same KPIs four times  
- Hunting meaning inside chart chrome  
- Exhaustion from borders/badges/cards  
- Feeling like a developer inspecting JSON/markdown  

### 10.3 Continuity checklist (acceptance for V2)

- [ ] Page feels like **one** report, not six apps  
- [ ] Sidebar never optically competes with stream  
- [ ] Hero answers who / quality / recommendation in ≤3s  
- [ ] Day pillar is visual heart; metadata quiet  
- [ ] Charts smaller than insight text  
- [ ] Analysis readable as Conclusion→…→Knowledge blocks  
- [ ] Interpretation feels book-like  
- [ ] Knowledge feels appendix, not docs site  
- [ ] Visible cards ≤ −40%  
- [ ] Decorative borders ≤ −50%  
- [ ] No nested cards  
- [ ] No new widgets / badge systems  
- [ ] Binding Index untouched  
- [ ] Backend/Engine/API/DB untouched  

---

## 11. Implementation gates (after approval only)

### Phase A — Foundation (CSS / shell)

- Report stream wrapper; demote rail  
- Spacing + type tokens  
- Strip tier mega-card chrome  

### Phase B — Cover & Heart

- Hero redesign (fold contract)  
- Pillars as composition (Day dominant)  

### Phase C — Insight & Reasoning

- Metrics prose-first + smaller charts  
- Analysis block template restyle  

### Phase D — Book & Appendix

- Interpretation book measure  
- Knowledge appendix calm  

### Phase E — Proof

- Side-by-side screenshots (before/after)  
- Card/border counts  
- Reading journey QA on desktop + mobile  

**No Phase starts without written approval of this Master Plan.**

---

## 12. Open decisions for Product Owner

Please confirm or adjust before coding:

1. **Single sheet vs open canvas** — one soft report panel, or fully open page with space-only sections?  
2. **Metrics vs Blueprint 2×2** — confirm Commercial V2 may prioritize smaller supportive charts over literal ChartBand dashboard.  
3. **Rail** — always visible slim rail on desktop, or auto-hide until hover/scroll?  
4. **Dark theme** — restyle in lockstep, or light-first then dark pass?  
5. **Approval** — reply **APPROVE** (optionally with edits) to unlock implementation.

---

## Document control

| Version | Note |
|---------|------|
| 0.1 | Initial Commercial UI V2.0 Master Plan — awaiting approval |

**END — NO CODE UNTIL APPROVED**
