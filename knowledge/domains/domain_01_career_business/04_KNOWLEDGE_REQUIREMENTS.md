# 04 — Knowledge Requirements · Career & Business

Version: 1.0  
Status: **OFFICIAL — Domain 01 Knowledge Requirements**  
Date: 2026-08-08  
Depends on: `03` · Knowledge Catalog (`16`) · Wave 1.1 frozen  
Scope: **Slot inventory only** — no unit body content  

---

## 1. Purpose

Identify Knowledge Units **required** for Domain 01, prioritized P0 / P1 / P2.

This file reserves intent and priority. It does **not** author `modern_interpretation` or create CSV rows.

Wave 1.1 cores remain frozen and are **dependencies**, not Domain 01 units.

---

## 2. Dependency units (frozen — do not revise here)

| Id | Role for Domain 01 |
|----|--------------------|
| KU-ID-001 | Work identity spine |
| KU-ST-001 | Capacity for advance / load |
| KU-WK-001 | Caution / mitigate-first gate |
| KU-UG-001 | Career & business compass |
| KU-RC-001 | Generic action until domain Rec specializes |

---

## 3. P0 — Required to open Domain 01 commercially (light)

Minimum set so CS-CA / default-light career consultation is more than Wave 1.1 generic.

| Reserved id (catalog-aligned) | Intent title | Kind | Subdomain | Serves |
|-------------------------------|--------------|------|-----------|--------|
| KU-CN-CA-000001 | Career — work-direction implication | CN | CA-SEL | D-CA-SEL, Q-01 |
| KU-AC-CA-000001 | Career — role-fit next step | AC | CA-SEL / CA-DEV | D-CA-SEL, D-CA-DEV, Q-01, Q-07 |
| KU-CN-LE-000001 | Leadership — authority style (light) | CN | CA-LED | D-CA-LED, Q-05 |
| KU-AC-BU-000001 | Business — solo vs partner (light) **or** employment-vs-independent posture | AC | BU-PTR / BU-ENP | D-BU-PTR, D-BU-ENP, Q-03, Q-06, Q-09 |

**P0 count target:** 3–4 new units (exact ids may follow catalog; no content this sprint).

**P0 exit:** Customer gets work-direction + next step + light leadership/independence posture on top of Wave 1.1.

---

## 4. P1 — Decision depth (change / promote / found / partner)

| Reserved id | Intent title | Kind | Subdomain | Serves |
|-------------|--------------|------|-----------|--------|
| KU-CN-CA-000002 | Career — industry/role theme pack A | CN | CA-SEL | Q-01, Q-19 |
| KU-CN-CA-000003 | Career — industry/role theme pack B | CN | CA-SEL | Q-01, Q-19 |
| KU-AC-CA-000002 | Career change — Go posture | AC | CA-CHG | D-CA-CHG, Q-02 |
| KU-AC-CA-000003 | Career change — staged transition | AC | CA-CHG | D-CA-CHG, Q-11, Q-14 |
| KU-RK-CA-000001 | Career change — reckless switch risk | RK | CA-CHG | D-CA-CHG |
| KU-MT-CA-000001 | Mitigation — career change buffer | MT | CA-CHG | pair RK-CA-000001 |
| KU-OP-CA-000001 | Promotion — advancement window | OP | CA-PRO | D-CA-PRO, Q-08 |
| KU-AC-CA-000004 | Career — skill investment next step | AC | CA-DEV | D-CA-DEV, Q-18 |
| KU-CN-BU-000001 | Business — enterprise posture | CN | BU-ENP | D-BU-ENP, Q-03 |
| KU-AC-BU-000002 | Startup — launch / pilot / defer | AC | BU-ENP | D-BU-ENP, Q-14 |
| KU-RK-BU-000002 | Startup — premature launch risk | RK | BU-ENP | D-BU-ENP |
| KU-MT-BU-000002 | Mitigation — MVP / runway | MT | BU-ENP | pair RK-BU-000002 |
| KU-RK-BU-000001 | Partnership — trust/clash risk | RK | BU-PTR | D-BU-PTR, DS-BP |
| KU-MT-BU-000001 | Mitigation — partnership role clarity | MT | BU-PTR | pair RK-BU-000001 |
| KU-CN-LE-000002 | Management — manager vs IC | CN | CA-MGT | D-CA-MGT, Q-04 |
| KU-RK-LE-000001 | Leadership — authority strain risk | RK | CA-LED | D-CA-LED |
| KU-MT-LE-000001 | Mitigation — leadership load habits | MT | CA-LED | pair RK-LE |

**P1 count target:** ~15–18 units (catalog-aligned; author later).

**Mandatory pairing:** Every RK in P1 must ship with MT (never stop at risk).

---

## 5. P2 — Differentiation & long-horizon

| Reserved id | Intent title | Kind | Subdomain |
|-------------|--------------|------|-----------|
| KU-ST-BU-000001 | Entrepreneurship — long-horizon founder strategy | ST | BU-ENP |
| KU-CN-BU-000002 | Business — industry expansion themes | CN | BU-ENP |
| KU-OP-BU-000002 | Entrepreneurship — capability window | OP | BU-ENP |
| KU-RK-BU-000003 | Founder burnout risk | RK | BU-ENP |
| KU-MT-BU-000003 | Founder recovery / scope mitigation | MT | BU-ENP |
| KU-CN-TEM-000001 | Team — delegation & conflict themes | CN | BU-TEM |
| KU-AC-TEM-000001 | Team — next management habit | AC | BU-TEM |
| KU-OP-LU-000002 | Luck — career-favoring window (cross CK-LU) | OP | timing support |

**P2:** after P0/P1 quality proven on Golden Cases.

---

## 6. Priority rules

1. **Do not author P2 before P0 Golden Cases pass.**  
2. **Do not expand quantity to hide Wave 1.1 / Narrative gaps.**  
3. **Prefer pairs (RK+MT, CN+AC)** over orphan risks.  
4. **Reuse Wave 1.1** for structural weakness/strength — do not duplicate ID/ST/WK/UG/RC.  
5. **Ids follow** EPIC 2 catalog naming; Domain 01 may refine titles but not invent conflicting id schemes.

---

## 7. Explicit non-requirements (this domain)

| Not required in Domain 01 | Belongs to |
|---------------------------|------------|
| Deep wealth product / investment KU | Finance domain |
| Marriage timing KU | Marriage domain |
| Medical advice KU | Never |
| New Wave 1.1 structural cores | Frozen |

---

## 8. Population readiness gate

Before Sprint B (authoring):

- [ ] Product approves P0 slot list  
- [ ] Scenario activation policy (default vs CS-CA-only) decided  
- [ ] Golden Case plan `05` accepted  
- [ ] Cross-domain deps `08` accepted  

---

## 9. Stop line

Requirements inventoried — **no content written**. Journey/outcomes follow.

---

END
