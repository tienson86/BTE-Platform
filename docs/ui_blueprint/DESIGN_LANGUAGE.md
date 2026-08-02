# DESIGN LANGUAGE — BTE Professional Analysis

| Field | Value |
|-------|--------|
| **Document** | `DESIGN_LANGUAGE.md` |
| **Version** | `1.1.0` |
| **Status** | Final Freeze — Blueprint V1.1 |
| **See also** | [15_VISUAL_GRAMMAR.md](15_VISUAL_GRAMMAR.md) (Addendum J) · [17_LOCALIZATION_CONTRACT.md](17_LOCALIZATION_CONTRACT.md) (Addendum L) |

---

## Purpose

Define the **BTE Design Language** so future UI cannot drift into Admin Dashboard / CMS / ERP aesthetics.

BTE Result is a **Professional Analysis Software** surface for BaZi interpretation.

---

## Positioning statement

BTE looks and feels like a **calm, high-trust analytical report workspace** — closer to a research terminal or analysis cockpit than a CRUD console.

**We are:** Insight → Structure → Evidence.  
**We are not:** Tables of everything, equal widgets, settings-first chrome.

---

## Explicit anti-targets

| Must not resemble | Why |
|-------------------|-----|
| **Admin Dashboard** | KPI tiles, identical cards, sidebar of modules, “systems online” as hero |
| **CMS** | Content lists, publish workflows as primary mental model |
| **ERP / back-office** | Dense forms, grids, operational tables as the product story |
| **Developer tool** | Raw JSON, debug tabs, equal-weight stage switchers |

If a reviewer can remove the BaZi words and still see “generic SaaS admin,” the design failed.

---

## Reference spirits (do not copy)

| Reference | Steal the *behavior*, not the skin |
|-----------|-------------------------------------|
| **TradingView** | Chart-forward analysis; focus on the instrument; panels support the read |
| **Bloomberg Terminal** | Information density with strict hierarchy; professionals know where eyes go |
| **Perplexity** | Answer first; sources beside/beneath; trust via traceability |
| **Notion** | Readable long-form sections; calm typography; whitespace as structure |
| **Linear** | Restraint, craft, neutral chrome, purposeful motion |
| **ChatGPT** | Conversational depth **after** grounding — not instead of the report |

BTE synthesizes: **Hero insight (Perplexity)** + **Structural canvas (TradingView)** + **Report readability (Notion)** + **Craft restraint (Linear)** + **Expert dialogue last (ChatGPT)**.

---

## Voice of the interface

| Attribute | Design language |
|-----------|-----------------|
| Calm | Neutrals dominate; motion quiet |
| Authoritative | Clear hierarchy; no playful clutter |
| Honest | Unavailable > fake completeness |
| Educational | Explain labels; avoid unexplained jargon dumps in hero |
| Non-fearful | Caution without doom red |

Copy and layout reinforce the Narrative / Terminology architecture docs — UI must not reintroduce “disaster” energy visually.

---

## Spatial language

1. **One spine** — vertical report stream  
2. **One guide** — sticky reading rail  
3. **One hero** — Executive Summary  
4. **Few accents** — Day Master / Useful / Helpful / Unfavorable / Strength  

---

## Density policy

| Zone | Density |
|------|---------|
| Hero | Low density, high meaning |
| Pillars / Charts | Medium |
| Analysis / Interpretation | Medium–high but sectioned |
| Knowledge expert panes | Higher density acceptable |

Never apply “high density everywhere” (terminal clone without hierarchy).

---

## Metaphor

Preferred metaphor: **“Bound analysis report with guided reading.”**  
Rejected metaphor: **“Module dashboard for chart objects.”**

---

## Design QA questions (pass/fail)

1. Does the first viewport answer the chart without clicking?  
2. Would a stranger know the next scroll step without instructions?  
3. Are accents scarce?  
4. Does anything look like a settings admin home?  
5. Are missing facts honest?

Any “no” → reject visual direction before coding.

---

## Version

`1.1.0`
