# UX PRINCIPLES — BTE

| Field | Value |
|-------|--------|
| **Document** | `UX_PRINCIPLES.md` |
| **Version** | `1.1.0` |
| **Status** | Final Freeze — Blueprint V1.1 |

---

## Purpose

Ten non-negotiable UX principles for BTE commercial UI.  
Every future UI sprint is reviewed against this list.

---

## The 10 principles

### 1. Insight First

The first viewport must deliver the chart’s core insight (Day Master + guidance axis + pattern cue).  
**Fail:** User must click around to learn the Day Master.

### 2. Facts before Narrative

Structural facts (pillars, strength, useful gods, pattern) precede long interpretation prose.  
**Fail:** Essay first, pillars buried.

### 3. Never overload users

Prefer one dominant surface and progressive disclosure over walls of equal cards.  
**Fail:** 40 same-size cards.

### 4. Executive Summary first

Tier order is fixed: Executive → Bazi → Charts → Analysis → Interpretation → Knowledge.  
**Fail:** Charts or chat as homepage.

### 5. Progressive Disclosure

Secondary detail collapses; primary path stays open.  
**Fail:** Everything expanded forever or everything hidden in accordions-as-nav.

### 6. Explain before Details

Short plain-language framing before dense catalogues (ten gods lists, shensha).  
**Fail:** Raw checklists with no orientation.

### 7. Every conclusion must have evidence

Recommendations and expert answers must map to earlier facts or explicit payload evidence.  
**Fail:** Orphan advice inventing gods/luck.

### 8. Knowledge is always traceable

Citations/status/confidence appear when available; absence is labeled Unavailable — not faked.  
**Fail:** Decorative “sources” without data.

### 9. Charts support narrative

Visual encodings reinforce Executive/Analysis; they do not replace meaning.  
**Fail:** Chart zoo with no hero insight.

### 10. Report is readable without training

A new user can complete a meaningful read by scrolling once, guided by the rail.  
**Fail:** Requires knowing which admin tab hides “Cách cục.”

---

## Operating rules derived from principles

| Rule | From principles |
|------|-----------------|
| No primary tier tabs | 1, 4, 10 |
| Sticky rail + scroll spy | 4, 10 |
| Accent scarcity | 3, Design Language |
| Unavailable honesty | 7, 8 |
| Expert last | 2, 4 |
| Desktop/laptop/tablet first | Product constraint |

---

## Review checklist (per PR / sprint)

- [ ] Insight visible in first viewport  
- [ ] Facts before long narrative  
- [ ] No equal-card overload  
- [ ] Tier order intact  
- [ ] Collapse used for disclosure, not navigation  
- [ ] Conclusions evidence-linked  
- [ ] Knowledge traceable or honestly empty  
- [ ] Charts subordinate to meaning  
- [ ] Stranger test: readable without training  

---

## Version

`1.1.0`
