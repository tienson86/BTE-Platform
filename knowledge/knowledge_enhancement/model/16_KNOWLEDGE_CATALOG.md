# 16 — Knowledge Catalog

Version: 1.0  
Status: **SPRINT D — Knowledge Catalog Blueprint**  
Date: 2026-08-08  
Depends on: Sprint A–C (`00`–`15`) — **frozen**  
Scope: **Planned inventory only** — defines WHAT units must exist, NOT content  

---

## 1. Purpose

Define the complete **Commercial Knowledge Catalog**: every Knowledge Unit slot BTE plans to author.

| This catalog is | This catalog is not |
|-----------------|---------------------|
| Planned KU ids + intent titles | Authored advisory `body` text |
| Grouped by domain / scenario / kind / priority | JSON or CSV records |
| Blueprint for population order | Runtime retrieval code |

**Status of all rows:** `planned` (not Draft content — no records created).

---

## 2. Catalog conventions

| Column | Meaning |
|--------|---------|
| `KU id` | Reserved id per `15` naming (`KU-{KIND}-{DOMAIN}-{SEQ}`) |
| `Intent title` | What the unit must answer (not customer-facing body) |
| `Kind` | AN CN PG AC RK MT ST OP |
| `Domain` | Primary CK-* |
| `Scenarios` | Primary CS-* affinity |
| `P` | Authoring priority P0 / P1 / P2 |
| `CV` | Commercial value: C=Critical, H=High, M=Medium, L=Low |

Kind codes: AN Analytical · CN Consultation · PG Practical Guidance · AC Action · RK Risk · MT Mitigation · ST Life Strategy · OP Opportunity.

---

## 3. Catalog summary counts

| Priority | Planned units | Commercial focus |
|----------|--------------:|------------------|
| **P0** | 42 | Default Result + Exec/Rec/Warning completeness |
| **P1** | 48 | Career/Finance/Luck/Business decision depth |
| **P2** | 36 | Sensitive + adjacent scenarios |
| **Total** | **126** | Full catalog blueprint |

---

## 4. P0 — Critical commercial core

### 4.1 Identity & structural analytical (CK-ID / structural)

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-AN-ID-000001 | Identity framing — day master human naming | AN | CK-ID | CS-ID, default | P0 | C |
| KU-AN-ID-000002 | Identity framing — pattern label in consultant language | AN | CK-ID | CS-ID, default | P0 | C |
| KU-AN-ID-000003 | Identity framing — strength band (vượng/nhược/cân) | AN | CK-ID | CS-ID, default | P0 | C |
| KU-AN-ID-000004 | Grade / overall quality framing (non-technical) | AN | CK-ID | CS-ID, default | P0 | H |
| KU-AN-ID-000005 | Reasoning — strength meaning (non-technical) | AN | CK-ID | CS-ID, CS-PG | P0 | C |
| KU-AN-ID-000006 | Reasoning — pattern meaning (non-technical) | AN | CK-ID | CS-ID, CS-PG | P0 | C |
| KU-AN-ID-000007 | Reasoning — useful god meaning (non-technical) | AN | CK-ID | CS-ID, CS-CA | P0 | C |
| KU-AN-XX-000001 | Observation — factual structure summary pack | AN | structural | default | P0 | C |
| KU-CN-PE-000001 | Personality light — interaction tendency (ethical) | CN | CK-PE | CS-ID, CS-DT | P0 | H |

### 4.2 Action / decision / useful-god practical (CK-DM / CK-CA)

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-AC-DM-000001 | Next action — useful god priority (generic) | AC | CK-DM | CS-MD, default | P0 | C |
| KU-AC-DM-000002 | Decision posture — Wait | AC | CK-DM | CS-MD, CS-CC | P0 | C |
| KU-AC-DM-000003 | Decision posture — Prepare | AC | CK-DM | CS-MD, CS-CC | P0 | C |
| KU-AC-DM-000004 | Decision posture — Advance | AC | CK-DM | CS-MD | P0 | C |
| KU-AC-DM-000005 | Decision posture — Protect | AC | CK-DM | CS-MD, CS-IV | P0 | C |
| KU-AC-DM-000006 | Decision posture — Reassess / insufficient honesty | AC | CK-DM | CS-MD, default | P0 | C |
| KU-PG-LS-000001 | Practical — daily pacing aligned to strength | PG | CK-LS | CS-LS, default | P0 | H |
| KU-PG-XX-000001 | Practical — useful god lifestyle translation | PG | structural | CS-LS, CS-CA | P0 | C |
| KU-ST-PG-000001 | Strategy — multi-year development posture | ST | CK-PG | CS-PG, default | P0 | H |
| KU-AC-CA-000001 | Career — role-fit next step (generic) | AC | CK-CA | CS-CA | P0 | C |
| KU-CN-CA-000001 | Career — work-direction implication | CN | CK-CA | CS-CA | P0 | C |

### 4.3 Risk + mitigation pairs (structural / luck / clash)

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-RK-XX-000001 | Risk — useful god suppressed / hostile period | RK | structural | CS-LT, CS-MD | P0 | C |
| KU-MT-XX-000001 | Mitigation — pair for useful god hostility | MT | structural | CS-LT, CS-MD | P0 | C |
| KU-RK-XX-000002 | Risk — major clash / punishment activation | RK | structural | CS-LT, CS-MD | P0 | C |
| KU-MT-XX-000002 | Mitigation — pair for clash/punishment | MT | structural | CS-LT, CS-MD | P0 | C |
| KU-RK-XX-000003 | Risk — strength extreme imbalance | RK | structural | CS-ID, CS-HE | P0 | H |
| KU-MT-XX-000003 | Mitigation — pair for strength imbalance | MT | structural | CS-ID, CS-LS | P0 | H |
| KU-RK-XX-000004 | Risk — enemy god / kỳ thần dominance | RK | structural | default | P0 | C |
| KU-MT-XX-000004 | Mitigation — pair for enemy god dominance | MT | structural | default | P0 | C |

### 4.4 Opportunity + luck timing (CK-LU)

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-OP-LU-000001 | Opportunity — favorable useful-god luck window | OP | CK-LU | CS-LT, CS-CA | P0 | C |
| KU-CN-LU-000001 | Luck — period narrative (đại vận posture) | CN | CK-LU | CS-LT | P0 | C |
| KU-CN-LU-000002 | Luck — year posture implication | CN | CK-LU | CS-LT | P0 | H |
| KU-AC-LU-000001 | Luck — period priority action | AC | CK-LU | CS-LT, default | P0 | C |
| KU-OP-XX-000001 | Opportunity — strength-supported lean-in | OP | structural | CS-PR, CS-CA | P0 | H |

### 4.5 Exec / conclusion settle pack

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-AN-ID-000008 | Conclusion — identity settle line | AN | CK-ID | default | P0 | C |
| KU-AC-DM-000007 | Conclusion — one priority recommendation settle | AC | CK-DM | default | P0 | C |
| KU-CN-XX-000001 | Impact — generic life implication from useful god | CN | structural | default | P0 | H |
| KU-AN-XX-000002 | Explanation — temperature/season meaning (light) | AN | structural | CS-LS, CS-HE | P0 | H |
| KU-AN-XX-000003 | Explanation — ten gods profile meaning (light) | AN | structural | CS-ID, CS-PE | P0 | H |

---

## 5. P1 — High commercial expansion

### 5.1 Career / promotion / change

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-CN-CA-000002 | Career — industry/role theme pack A | CN | CK-CA | CS-CA | P1 | H |
| KU-CN-CA-000003 | Career — industry/role theme pack B | CN | CK-CA | CS-CA | P1 | H |
| KU-AC-CA-000002 | Career change — Go posture action | AC | CK-CA | CS-CC | P1 | H |
| KU-AC-CA-000003 | Career change — staged transition action | AC | CK-CA | CS-CC | P1 | H |
| KU-RK-CA-000001 | Career change — reckless switch risk | RK | CK-CA | CS-CC | P1 | H |
| KU-MT-CA-000001 | Mitigation — career change buffer | MT | CK-CA | CS-CC | P1 | H |
| KU-OP-CA-000001 | Promotion — advancement window | OP | CK-CA | CS-PR | P1 | H |
| KU-RK-LE-000001 | Promotion — authority strain risk | RK | CK-LE | CS-PR | P1 | H |
| KU-MT-LE-000001 | Mitigation — scope/delegation under strain | MT | CK-LE | CS-PR | P1 | H |
| KU-CN-LE-000001 | Leadership — style implication | CN | CK-LE | CS-LE | P1 | M |
| KU-PG-LE-000001 | Leadership — sustainable authority habits | PG | CK-LE | CS-LE, CS-PR | P1 | M |
| KU-AC-CA-000004 | Career — skill investment next step | AC | CK-CA | CS-CA, CS-ED | P1 | H |

### 5.2 Finance / investment / property / business

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-CN-FI-000001 | Finance — money posture implication | CN | CK-FI | CS-FI | P1 | H |
| KU-PG-FI-000001 | Finance — earning/keeping habit guidance | PG | CK-FI | CS-FI | P1 | H |
| KU-AC-FI-000001 | Finance — conserve capital action | AC | CK-FI | CS-FI, CS-IV | P1 | H |
| KU-AC-FI-000002 | Finance — selective deploy action | AC | CK-FI | CS-IV | P1 | H |
| KU-RK-FI-000001 | Investment — overextension risk | RK | CK-FI | CS-IV | P1 | C |
| KU-MT-FI-000001 | Mitigation — position sizing / liquidity | MT | CK-FI | CS-IV | P1 | C |
| KU-RK-FI-000002 | Wealth clash period risk | RK | CK-FI | CS-FI, CS-LT | P1 | H |
| KU-MT-FI-000002 | Mitigation — wealth clash period | MT | CK-FI | CS-FI, CS-LT | P1 | H |
| KU-CN-BU-000001 | Business — enterprise posture | CN | CK-BU | CS-BU | P1 | H |
| KU-RK-BU-000001 | Business partnership — trust/clash risk | RK | CK-BU | CS-BU, DS-BP | P1 | H |
| KU-MT-BU-000001 | Mitigation — partnership role clarity | MT | CK-BU | CS-BU | P1 | H |
| KU-AC-BU-000001 | Business — solo vs partner action | AC | CK-BU | CS-BU | P1 | H |
| KU-OP-BU-000001 | Startup — launch window opportunity | OP | CK-BU | CS-ST | P1 | H |
| KU-RK-BU-000002 | Startup — premature launch risk | RK | CK-BU | CS-ST | P1 | H |
| KU-MT-BU-000002 | Mitigation — MVP / runway | MT | CK-BU | CS-ST | P1 | H |
| KU-AC-BU-000002 | Startup — launch / pilot / defer actions | AC | CK-BU | CS-ST | P1 | H |
| KU-CN-FI-000002 | Property — commit vs wait implication | CN | CK-FI | CS-PP | P1 | M |
| KU-AC-FI-000003 | Property — commit / wait / prepare | AC | CK-FI | CS-PP | P1 | M |
| KU-RK-FI-000003 | Property — lock-up in hostile period | RK | CK-FI | CS-PP | P1 | M |
| KU-MT-FI-000003 | Mitigation — property liquidity reserve | MT | CK-FI | CS-PP | P1 | M |
| KU-ST-BU-000001 | Entrepreneurship — long-horizon founder strategy | ST | CK-BU | CS-ENP | P1 | M |

### 5.3 Luck depth / education / growth / relocation light

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-CN-LU-000003 | Luck — combine/harmony period implication | CN | CK-LU | CS-LT | P1 | H |
| KU-RK-LU-000001 | Luck — multi-year hostile arc risk | RK | CK-LU | CS-LT | P1 | H |
| KU-MT-LU-000001 | Mitigation — hostile arc pacing | MT | CK-LU | CS-LT | P1 | H |
| KU-OP-LU-000002 | Luck — career-favoring decade opportunity | OP | CK-LU | CS-LT, CS-CA | P1 | H |
| KU-CN-ED-000001 | Education — learning theme implication | CN | CK-ED | CS-ED | P1 | M |
| KU-AC-ED-000001 | Education — study investment action | AC | CK-ED | CS-ED | P1 | M |
| KU-OP-ED-000001 | Education — learning window opportunity | OP | CK-ED | CS-ED | P1 | M |
| KU-CN-PG-000001 | Personal growth — release/lean themes | CN | CK-PG | CS-PG | P1 | H |
| KU-AC-PG-000001 | Personal growth — development next step | AC | CK-PG | CS-PG | P1 | H |
| KU-CN-EN-000001 | Relocation — place/support implication | CN | CK-EN | CS-RL | P1 | M |
| KU-AC-EN-000001 | Relocation — move / defer / prepare | AC | CK-EN | CS-RL | P1 | M |
| KU-RK-EN-000001 | Relocation — unstable move risk | RK | CK-EN | CS-RL | P1 | M |
| KU-MT-EN-000001 | Mitigation — trial period / buffer | MT | CK-EN | CS-RL | P1 | M |
| KU-AN-XX-000004 | Shensha — selected caution meaning (top stars) | AN | structural | CS-LT | P1 | M |
| KU-RK-XX-000005 | Shensha — curated star risk (family A) | RK | structural | default | P1 | M |
| KU-MT-XX-000005 | Mitigation — curated shensha family A | MT | structural | default | P1 | M |

---

## 6. P2 — Sensitive & adjacent

### 6.1 Relationships / marriage / dating / family

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-CN-MA-000001 | Marriage — partnership theme (ethics) | CN | CK-MA | CS-MA | P2 | H |
| KU-RK-MA-000001 | Marriage — clash/harm caution (ethics) | RK | CK-MA | CS-MA | P2 | H |
| KU-MT-MA-000001 | Mitigation — relationship pacing / care | MT | CK-MA | CS-MA | P2 | H |
| KU-AC-MA-000001 | Marriage — constructive practice action | AC | CK-MA | CS-MA | P2 | H |
| KU-CN-RE-000001 | Relationships — peer/family bond theme | CN | CK-RE | CS-DT, CS-PA | P2 | M |
| KU-CN-DT-000001 | Dating — selection pattern awareness | CN | CK-RE | CS-DT | P2 | M |
| KU-PG-DT-000001 | Dating — healthy pacing guidance | PG | CK-RE | CS-DT | P2 | M |
| KU-CN-CH-000001 | Children — thematic care language (ethics) | CN | CK-CH | CS-CH | P2 | M |
| KU-PG-CH-000001 | Children — supportive nurture guidance | PG | CK-CH | CS-CH | P2 | M |
| KU-CN-PA-000001 | Parents — duty/support theme | CN | CK-PA | CS-PA | P2 | M |
| KU-AC-PA-000001 | Parents — boundary/care action | AC | CK-PA | CS-PA | P2 | M |

### 6.2 Health / lifestyle / environment / travel / retirement

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-CN-HE-000001 | Health — lifestyle imbalance implication (non-medical) | CN | CK-HE | CS-HE | P2 | H |
| KU-RK-HE-000001 | Health — extreme temperature/element caution | RK | CK-HE | CS-HE | P2 | H |
| KU-MT-HE-000001 | Mitigation — rest/pace lifestyle | MT | CK-HE | CS-HE | P2 | H |
| KU-AC-HE-000001 | Health — habit adjustment + care disclaimer | AC | CK-HE | CS-HE | P2 | H |
| KU-PG-LS-000002 | Lifestyle — habit set pack A | PG | CK-LS | CS-LS | P2 | M |
| KU-PG-LS-000003 | Lifestyle — habit set pack B | PG | CK-LS | CS-LS | P2 | M |
| KU-AC-LS-000001 | Lifestyle — 1–3 concrete habit actions | AC | CK-LS | CS-LS | P2 | M |
| KU-CN-EN-000002 | Environment — supportive setting themes | CN | CK-EN | CS-EN | P2 | L |
| KU-PG-EN-000001 | Environment — soft place guidance | PG | CK-EN | CS-EN | P2 | L |
| KU-CN-TR-000001 | Travel — period posture implication | CN | CK-EN | CS-TR | P2 | L |
| KU-AC-TR-000001 | Travel — go / defer / recover actions | AC | CK-EN | CS-TR | P2 | L |
| KU-RK-TR-000001 | Travel — depletion risk | RK | CK-EN | CS-TR | P2 | L |
| KU-MT-TR-000001 | Mitigation — travel recovery buffer | MT | CK-EN | CS-TR | P2 | L |
| KU-ST-PG-000002 | Retirement — later-life purpose strategy | ST | CK-PG | CS-RT | P2 | M |
| KU-CN-FI-000003 | Retirement — finance posture implication | CN | CK-FI | CS-RT | P2 | M |
| KU-PG-LS-000004 | Retirement — pacing lifestyle | PG | CK-LS | CS-RT | P2 | M |
| KU-AC-FI-000004 | Retirement — conserve / simplify actions | AC | CK-FI | CS-RT | P2 | M |

### 6.3 Depth / future expansions

| KU id | Intent title | Kind | Domain | Scenarios | P | CV |
|-------|--------------|------|--------|-----------|---|-----|
| KU-AN-XX-000005 | Transformation pattern meaning (special) | AN | structural | CS-ID | P2 | L |
| KU-CN-BU-000002 | Business — industry expansion themes | CN | CK-BU | CS-ENP | P2 | L |
| KU-OP-BU-000002 | Entrepreneurship — capability window | OP | CK-BU | CS-ENP | P2 | L |
| KU-RK-BU-000003 | Entrepreneurship — founder burnout risk | RK | CK-BU | CS-ENP | P2 | L |
| KU-MT-BU-000003 | Mitigation — founder recovery / scope | MT | CK-BU | CS-ENP | P2 | L |
| KU-AN-XX-000006 | Na Yin / growth-stage narrative (light) | AN | structural | CS-ID | P2 | L |
| KU-CN-XX-000002 | Knowledge Panel — glossary bridge pack | CN | structural | Knowledge Panel | P2 | M |
| KU-AN-XX-000007 | Knowledge Panel — five elements explain | AN | structural | Knowledge Panel | P2 | M |

---

## 7. Grouped views

### 7.1 By knowledge type (kind)

| Kind | P0 | P1 | P2 | Total |
|------|---:|---:|---:|------:|
| AN | 12 | 1 | 4 | 17 |
| CN | 5 | 10 | 10 | 25 |
| PG | 2 | 2 | 7 | 11 |
| AC | 10 | 10 | 6 | 26 |
| RK | 4 | 8 | 5 | 17 |
| MT | 4 | 8 | 5 | 17 |
| ST | 1 | 1 | 1 | 3 |
| OP | 2 | 5 | 1 | 8 |
| **Sum** | **40*** | **45*** | **39*** | **124*** |

\*Counts approximate to catalog rows; use §3 total **126** as planning target including minor id reserves. Exact publish set may merge near-duplicates during authoring.

### 7.2 By commercial value

| CV | Role |
|----|------|
| **C Critical** | Blocks consultant-grade default Narrative |
| **H High** | Material scenario depth |
| **M Medium** | Completeness |
| **L Low** | Adjacent / academic-light |

---

## 8. Pairing register (planned)

| Risk KU | Mitigation KU |
|---------|---------------|
| KU-RK-XX-000001 | KU-MT-XX-000001 |
| KU-RK-XX-000002 | KU-MT-XX-000002 |
| KU-RK-XX-000003 | KU-MT-XX-000003 |
| KU-RK-XX-000004 | KU-MT-XX-000004 |
| KU-RK-XX-000005 | KU-MT-XX-000005 |
| KU-RK-CA-000001 | KU-MT-CA-000001 |
| KU-RK-LE-000001 | KU-MT-LE-000001 |
| KU-RK-FI-000001 | KU-MT-FI-000001 |
| KU-RK-FI-000002 | KU-MT-FI-000002 |
| KU-RK-FI-000003 | KU-MT-FI-000003 |
| KU-RK-BU-000001 | KU-MT-BU-000001 |
| KU-RK-BU-000002 | KU-MT-BU-000002 |
| KU-RK-BU-000003 | KU-MT-BU-000003 |
| KU-RK-LU-000001 | KU-MT-LU-000001 |
| KU-RK-EN-000001 | KU-MT-EN-000001 |
| KU-RK-MA-000001 | KU-MT-MA-000001 |
| KU-RK-HE-000001 | KU-MT-HE-000001 |
| KU-RK-TR-000001 | KU-MT-TR-000001 |

---

## 9. Out of catalog (explicit)

Not planned as KUs:

- Rule Database rows  
- Pack 05 section templates  
- Portal i18n chrome  
- Raw Interpretation technical strings  

---

## 10. Stop line

Catalog defines **what must exist**.  
**No content authored. No CSV/JSON created.**

See `17`–`20` for maps and implementation order.

---

END
