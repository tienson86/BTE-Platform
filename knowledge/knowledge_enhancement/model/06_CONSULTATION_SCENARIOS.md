# 06 — Consultation Scenarios

Version: 1.0  
Status: **SPRINT B — Consultation Scenario Model**  
Date: 2026-08-08  
Depends on: Sprint A (`00`–`05`) — **frozen**  
Scope: Documentation only — no records, no retrieval implementation  

---

## 1. Purpose

Define the official **scenario-based consultation model** for BTE.

Scenarios organize Commercial Knowledge around **real customer questions**, not academic BaZi folders (Five Elements, Ten Gods, Useful God, Patterns).

| Concept | Role |
|---------|------|
| **Scenario** | Business entry point — customer intent |
| **Consultation Domain (CK-*)** | Topic space from Sprint A |
| **Commercial Knowledge** | SSOT for advisory meaning |
| **Rule Database** | Analytical calculation only |
| **Narrative** | Delivery composition only |

**Principle:** Always ask *“What is the customer trying to solve?”* before *“What rule explains this?”*

---

## 2. Architectural thesis (Sprint B)

| Statement | Meaning |
|-----------|---------|
| Scenario is **not** Rule | Rules do not define customer intent |
| Scenario is **not** Knowledge | Knowledge remains advisory SSOT |
| Scenario **connects** intent → Commercial Knowledge | Routing / selection context |
| Pack 05 grammar stays fixed | Scenarios theme evidence; they do not add Narrative sections |

---

## 3. Official scenario catalog

IDs use prefix `CS-` (Consultation Scenario).

| ID | Scenario | Primary CK domains |
|----|----------|--------------------|
| CS-ID | Identity | CK-ID, CK-PE |
| CS-CA | Career | CK-CA, CK-DM, CK-LU |
| CS-CC | Career Change | CK-CA, CK-DM, CK-LU, CK-PG |
| CS-PR | Promotion | CK-CA, CK-LE, CK-LU, CK-DM |
| CS-BU | Business | CK-BU, CK-FI, CK-DM |
| CS-ST | Startup | CK-BU, CK-FI, CK-LU, CK-DM |
| CS-LE | Leadership | CK-LE, CK-CA, CK-PE |
| CS-IV | Investment | CK-FI, CK-DM, CK-LU |
| CS-FI | Finance | CK-FI, CK-LS, CK-LU |
| CS-PP | Property | CK-FI, CK-EN, CK-DM, CK-LU |
| CS-MA | Marriage | CK-MA, CK-RE, CK-LU |
| CS-DT | Dating | CK-MA, CK-RE, CK-PE |
| CS-CH | Children | CK-CH, CK-RE (ethics-gated) |
| CS-PA | Parents | CK-PA, CK-RE |
| CS-HE | Health | CK-HE, CK-LS (non-medical) |
| CS-LS | Lifestyle | CK-LS, CK-PG, CK-HE |
| CS-ED | Education | CK-ED, CK-PG, CK-LU |
| CS-PG | Personal Growth | CK-PG, CK-DM, CK-ID |
| CS-LT | Luck Timing | CK-LU, CK-DM |
| CS-MD | Major Decisions | CK-DM, CK-LU, + context domain |
| CS-EN | Environment | CK-EN, CK-LS |
| CS-TR | Travel | CK-EN, CK-LU, CK-LS |
| CS-RL | Relocation | CK-EN, CK-CA, CK-FI, CK-DM, CK-LU |
| CS-ENP | Entrepreneurship | CK-BU, CK-ST themes, CK-LE, CK-FI |
| CS-RT | Retirement | CK-PG, CK-FI, CK-LS, CK-LU |

---

## 4. Scenario definition template

Every official scenario uses:

| Field | Meaning |
|-------|---------|
| Purpose | Why the customer opens this consultation |
| Typical customer questions | Intent phrasing |
| Expected consultation outcome | What “done” looks like for the customer |
| Required knowledge domains | CK-* (Sprint A) |
| Required commercial kinds | From `02` |
| Required evidence | Pack 05 evidence kinds |
| Required interpretation | Interpretation focus (structural sections / themes) |
| Expected narrative components | Which Pack 05 sections must carry this scenario |

Cardinality of relationships: see `07_SCENARIO_RELATIONSHIP_MODEL.md`.

---

## 5. Scenario definitions

### 5.1 Identity (CS-ID)

| Field | Content |
|-------|---------|
| **Purpose** | Establish who the person is in consultant language |
| **Typical questions** | Tôi là người như thế nào? Cấu trúc cốt lõi của tôi ra sao? |
| **Expected outcome** | Clear identity briefing the customer can remember |
| **Required domains** | CK-ID; CK-PE (light) |
| **Required commercial kinds** | Analytical; (optional) Consultation light |
| **Required evidence** | identity, strength, weakness, grade |
| **Required interpretation** | overview / strength / pattern / summary framing |
| **Expected narrative** | Exec, Observation, Reasoning, Conclusion |

### 5.2 Career (CS-CA)

| Field | Content |
|-------|---------|
| **Purpose** | Advise work direction and role fit |
| **Typical questions** | Nghề nào hợp tôi? Tôi nên theo hướng nào? |
| **Expected outcome** | Role themes + timing posture + next work action |
| **Required domains** | CK-CA, CK-DM, CK-LU |
| **Required commercial kinds** | Consultation, Action, Analytical; Risk/Mitigation if indicated |
| **Required evidence** | identity, implication, action; risk if present |
| **Required interpretation** | useful_god, ten_gods, pattern, luck |
| **Expected narrative** | Exec, Impact, Recommendation, Conclusion; Warning if risk |

### 5.3 Career Change (CS-CC)

| Field | Content |
|-------|---------|
| **Purpose** | Support switching path without reckless timing |
| **Typical questions** | Có nên đổi việc không? Đổi lúc nào? |
| **Expected outcome** | Go / wait / prepare decision frame + mitigations |
| **Required domains** | CK-CA, CK-DM, CK-LU, CK-PG |
| **Required commercial kinds** | Action, Risk, Mitigation, Opportunity, Consultation |
| **Required evidence** | action, risk, implication, identity |
| **Required interpretation** | useful_god, luck, strength, pattern |
| **Expected narrative** | Exec, Reasoning, Impact, Recommendation, Warning, Conclusion |

### 5.4 Promotion (CS-PR)

| Field | Content |
|-------|---------|
| **Purpose** | Assess advancement readiness and strain |
| **Typical questions** | Tôi có đang ở cửa thăng tiến? Nên nhận thêm trách nhiệm? |
| **Expected outcome** | Advancement posture + leadership strain cautions |
| **Required domains** | CK-CA, CK-LE, CK-LU, CK-DM |
| **Required commercial kinds** | Opportunity, Action, Risk, Mitigation, Consultation |
| **Required evidence** | action, strength, risk, implication |
| **Required interpretation** | officer/ten_gods, strength, luck |
| **Expected narrative** | Exec, Impact, Recommendation, Warning, Conclusion |

### 5.5 Business (CS-BU)

| Field | Content |
|-------|---------|
| **Purpose** | Guide enterprise posture and partnership risk |
| **Typical questions** | Tôi hợp làm chủ không? Nên hợp tác thế nào? |
| **Expected outcome** | Business posture + partnership cautions + actions |
| **Required domains** | CK-BU, CK-FI, CK-DM |
| **Required commercial kinds** | Consultation, Action, Risk, Mitigation, Strategy |
| **Required evidence** | implication, action, risk |
| **Required interpretation** | useful_god, wealth/officer signals, clash/combine, luck |
| **Expected narrative** | Exec, Impact, Recommendation, Warning, Conclusion |

### 5.6 Startup (CS-ST)

| Field | Content |
|-------|---------|
| **Purpose** | Timing and risk for new ventures |
| **Typical questions** | Có nên khởi nghiệp bây giờ? Rủi ro nào cần giảm? |
| **Expected outcome** | Launch / defer / validate frame + mitigations |
| **Required domains** | CK-BU, CK-FI, CK-LU, CK-DM |
| **Required commercial kinds** | Opportunity, Risk, Mitigation, Action, Strategy |
| **Required evidence** | action, risk, implication, strength |
| **Required interpretation** | luck, useful_god, pattern, clash |
| **Expected narrative** | Full set emphasizing Recommendation + Warning |

### 5.7 Leadership (CS-LE)

| Field | Content |
|-------|---------|
| **Purpose** | Clarify authority style and influence conditions |
| **Typical questions** | Phong cách lãnh đạo của tôi? Khi nào dễ quá tải quyền lực? |
| **Expected outcome** | Leadership style + strain mitigations |
| **Required domains** | CK-LE, CK-CA, CK-PE |
| **Required commercial kinds** | Analytical, Consultation, Practical Guidance, Risk, Mitigation |
| **Required evidence** | identity, explanation, risk, action |
| **Required interpretation** | ten_gods (officer), strength, pattern |
| **Expected narrative** | Observation, Reasoning, Impact, Recommendation, Warning |

### 5.8 Investment (CS-IV)

| Field | Content |
|-------|---------|
| **Purpose** | Pace capital risk ethically (no return guarantees) |
| **Typical questions** | Có nên đầu tư mạnh giai đoạn này? |
| **Expected outcome** | Risk appetite posture + timing + mitigations |
| **Required domains** | CK-FI, CK-DM, CK-LU |
| **Required commercial kinds** | Risk, Mitigation, Action, Opportunity, Consultation |
| **Required evidence** | risk, action, implication |
| **Required interpretation** | wealth signals, luck, clash on wealth |
| **Expected narrative** | Exec, Impact, Recommendation, Warning, Conclusion |

### 5.9 Finance (CS-FI)

| Field | Content |
|-------|---------|
| **Purpose** | Money behavior and wealth pacing |
| **Typical questions** | Tôi kiếm / giữ / tiêu tiền thế nào thì hợp? |
| **Expected outcome** | Money posture + practical actions + cautions |
| **Required domains** | CK-FI, CK-LS, CK-LU |
| **Required commercial kinds** | Consultation, Practical Guidance, Action, Risk, Mitigation |
| **Required evidence** | implication, action, risk |
| **Required interpretation** | useful_god, wealth, luck |
| **Expected narrative** | Impact, Recommendation, Warning, Conclusion |

### 5.10 Property (CS-PP)

| Field | Content |
|-------|---------|
| **Purpose** | Property / asset commitment decisions |
| **Typical questions** | Có nên mua nhà / giữ tài sản cố định lúc này? |
| **Expected outcome** | Commit / wait / hedge frame |
| **Required domains** | CK-FI, CK-EN, CK-DM, CK-LU |
| **Required commercial kinds** | Action, Risk, Mitigation, Opportunity, Consultation |
| **Required evidence** | action, risk, implication |
| **Required interpretation** | luck, wealth, environment-support signals |
| **Expected narrative** | Exec, Recommendation, Warning, Conclusion |

### 5.11 Marriage (CS-MA)

| Field | Content |
|-------|---------|
| **Purpose** | Partnership themes with ethical care |
| **Typical questions** | Hôn nhân / gắn kết lâu dài của tôi có điểm nào cần lưu ý? |
| **Expected outcome** | Themes + cautions + constructive actions (non-fatalistic) |
| **Required domains** | CK-MA, CK-RE, CK-LU |
| **Required commercial kinds** | Consultation, Risk, Mitigation, Action (ethics-flagged) |
| **Required evidence** | implication, risk, action |
| **Required interpretation** | relation signals, clash/harm, luck |
| **Expected narrative** | Impact, Recommendation, Warning, Conclusion; Exec careful |

### 5.12 Dating (CS-DT)

| Field | Content |
|-------|---------|
| **Purpose** | Early-relationship patterns and self-awareness |
| **Typical questions** | Tôi thường chọn người thế nào? Nên chậm lại chỗ nào? |
| **Expected outcome** | Pattern awareness + healthy pacing actions |
| **Required domains** | CK-MA, CK-RE, CK-PE |
| **Required commercial kinds** | Consultation, Practical Guidance, Risk, Mitigation |
| **Required evidence** | identity, implication, action, risk |
| **Required interpretation** | ten_gods, personality framing, relation signals |
| **Expected narrative** | Observation, Impact, Recommendation, Warning |

### 5.13 Children (CS-CH)

| Field | Content |
|-------|---------|
| **Purpose** | Offspring / nurturing themes — ethics-first |
| **Typical questions** | Chủ đề con cái trong lá số nên hiểu thế nào? |
| **Expected outcome** | Careful thematic language + supportive actions only |
| **Required domains** | CK-CH, CK-RE |
| **Required commercial kinds** | Consultation, Practical Guidance (ethics-gated); Risk careful |
| **Required evidence** | implication, action; risk only if supported |
| **Required interpretation** | children-related signals when available |
| **Expected narrative** | Impact, Recommendation, Warning (soft); never medical fertility claims |

### 5.14 Parents (CS-PA)

| Field | Content |
|-------|---------|
| **Purpose** | Parental / elder dynamics |
| **Typical questions** | Quan hệ với cha mẹ / bề trên nên ứng xử thế nào? |
| **Expected outcome** | Duty/support framing + boundary actions |
| **Required domains** | CK-PA, CK-RE |
| **Required commercial kinds** | Consultation, Practical Guidance, Action, Mitigation |
| **Required evidence** | implication, action |
| **Required interpretation** | parental palace / relation signals |
| **Expected narrative** | Impact, Recommendation, Conclusion |

### 5.15 Health (CS-HE)

| Field | Content |
|-------|---------|
| **Purpose** | Lifestyle balance hints — **not medical advice** |
| **Typical questions** | Nhịp sống / cân bằng nào giúp tôi bền hơn? |
| **Expected outcome** | Pace/rest/element-balance lifestyle suggestions |
| **Required domains** | CK-HE, CK-LS |
| **Required commercial kinds** | Practical Guidance, Risk, Mitigation, Action |
| **Required evidence** | risk, action, implication |
| **Required interpretation** | temperature, five elements, selected shensha |
| **Expected narrative** | Impact, Recommendation, Warning (non-clinical) |

### 5.16 Lifestyle (CS-LS)

| Field | Content |
|-------|---------|
| **Purpose** | Daily rhythm aligned to structure |
| **Typical questions** | Tôi nên sống chậm / nhanh thế nào? Thói quen nào hợp? |
| **Expected outcome** | Habit set + energy management |
| **Required domains** | CK-LS, CK-PG, CK-HE |
| **Required commercial kinds** | Practical Guidance, Action, Analytical light |
| **Required evidence** | action, implication, identity |
| **Required interpretation** | strength, temperature, useful_god |
| **Expected narrative** | Recommendation, Impact, Conclusion |

### 5.17 Education (CS-ED)

| Field | Content |
|-------|---------|
| **Purpose** | Learning and skill investment |
| **Typical questions** | Nên học gì? Giai đoạn nào thuận học? |
| **Expected outcome** | Learning themes + timing + practice actions |
| **Required domains** | CK-ED, CK-PG, CK-LU |
| **Required commercial kinds** | Consultation, Opportunity, Action, Practical Guidance |
| **Required evidence** | implication, action, strength |
| **Required interpretation** | output/resource gods, useful_god, luck |
| **Expected narrative** | Impact, Recommendation, Conclusion |

### 5.18 Personal Growth (CS-PG)

| Field | Content |
|-------|---------|
| **Purpose** | Long-horizon development priorities |
| **Typical questions** | Tôi nên trưởng thành theo hướng nào? |
| **Expected outcome** | Growth themes + multi-year posture |
| **Required domains** | CK-PG, CK-DM, CK-ID |
| **Required commercial kinds** | Life Strategy, Analytical, Action, Opportunity |
| **Required evidence** | identity, implication, action |
| **Required interpretation** | pattern, useful_god, weaknesses |
| **Expected narrative** | Exec, Reasoning, Recommendation, Conclusion |

### 5.19 Luck Timing (CS-LT)

| Field | Content |
|-------|---------|
| **Purpose** | Decade/year posture and windows |
| **Typical questions** | Đại vận / năm này tôi nên nhấn gì? Tránh gì? |
| **Expected outcome** | Period narrative + priority + period risks |
| **Required domains** | CK-LU, CK-DM |
| **Required commercial kinds** | Consultation, Action, Risk, Mitigation, Opportunity |
| **Required evidence** | implication, action, risk, grade optional |
| **Required interpretation** | luck, clash/combine with natal, useful_god interaction |
| **Expected narrative** | Exec, Impact, Recommendation, Warning, Conclusion |

### 5.20 Major Decisions (CS-MD)

| Field | Content |
|-------|---------|
| **Purpose** | Generic high-stakes choice frame |
| **Typical questions** | Quyết định lớn này nên chọn thế nào? |
| **Expected outcome** | Decision criteria + go/wait/prepare + mitigations |
| **Required domains** | CK-DM, CK-LU, + context domain (career/finance/…) |
| **Required commercial kinds** | Action, Risk, Mitigation, Opportunity, Strategy |
| **Required evidence** | action, risk, implication, identity |
| **Required interpretation** | strength, useful_god, luck, conflict signals |
| **Expected narrative** | Full set; see `08_DECISION_SUPPORT_MODEL.md` |

### 5.21 Environment (CS-EN)

| Field | Content |
|-------|---------|
| **Purpose** | Supportive place/setting themes (hint-level) |
| **Typical questions** | Môi trường nào nâng đỡ tôi? |
| **Expected outcome** | Soft environment suggestions |
| **Required domains** | CK-EN, CK-LS |
| **Required commercial kinds** | Practical Guidance, Consultation, Action |
| **Required evidence** | implication, action |
| **Required interpretation** | useful_god elements, temperature |
| **Expected narrative** | Impact, Recommendation |

### 5.22 Travel (CS-TR)

| Field | Content |
|-------|---------|
| **Purpose** | Travel timing and recovery posture |
| **Typical questions** | Đi xa giai đoạn này có lợi / hại gì? |
| **Expected outcome** | Travel posture + pacing cautions |
| **Required domains** | CK-EN, CK-LU, CK-LS |
| **Required commercial kinds** | Opportunity, Risk, Mitigation, Practical Guidance |
| **Required evidence** | action, risk, implication |
| **Required interpretation** | luck, temperature/strength, environment |
| **Expected narrative** | Recommendation, Warning, Impact |

### 5.23 Relocation (CS-RL)

| Field | Content |
|-------|---------|
| **Purpose** | Moving city/country as a life decision |
| **Typical questions** | Có nên chuyển chỗ ở / định cư? |
| **Expected outcome** | Relocate / defer / prepare frame |
| **Required domains** | CK-EN, CK-CA, CK-FI, CK-DM, CK-LU |
| **Required commercial kinds** | Action, Risk, Mitigation, Opportunity, Strategy, Consultation |
| **Required evidence** | action, risk, implication, identity |
| **Required interpretation** | luck, useful_god, career/finance signals, environment |
| **Expected narrative** | Full decision set (Exec → Conclusion) |

### 5.24 Entrepreneurship (CS-ENP)

| Field | Content |
|-------|---------|
| **Purpose** | Broader founder path (beyond single startup event) |
| **Typical questions** | Con đường doanh chủ có hợp tôi dài hạn? |
| **Expected outcome** | Founder posture + capability gaps + timing |
| **Required domains** | CK-BU, CK-LE, CK-FI, CK-PG |
| **Required commercial kinds** | Strategy, Consultation, Action, Risk, Mitigation, Opportunity |
| **Required evidence** | identity, implication, action, risk |
| **Required interpretation** | pattern, useful_god, leadership/wealth, luck |
| **Expected narrative** | Exec, Reasoning, Impact, Recommendation, Warning, Conclusion |

### 5.25 Retirement (CS-RT)

| Field | Content |
|-------|---------|
| **Purpose** | Later-life pacing, purpose, and finance posture |
| **Typical questions** | Giai đoạn về sau tôi nên sống / sắp xếp thế nào? |
| **Expected outcome** | Pace + purpose + finance cautions |
| **Required domains** | CK-PG, CK-FI, CK-LS, CK-LU |
| **Required commercial kinds** | Strategy, Practical Guidance, Action, Risk, Mitigation |
| **Required evidence** | implication, action, risk |
| **Required interpretation** | luck arc, strength, wealth, lifestyle |
| **Expected narrative** | Impact, Recommendation, Warning, Conclusion |

---

## 6. Default scenario for general Result Page

When the customer has **no explicit scenario intent** (standard analyze → Result Page):

| Default | Composition |
|---------|-------------|
| Primary | CS-ID + CS-LT (light) + CS-MD (light) |
| Narrative | Full Pack 05 grammar with structural Analytical Knowledge |
| Life scenarios | Not forced; only if evidence/knowledge supports thematic Impact |

Scenario selection UX is product-owned; this model only defines the taxonomy.

---

## 7. Scenario tiers (commercial rollout)

| Tier | Scenarios | Note |
|------|-----------|------|
| T0 Core | CS-ID, CS-LT, CS-MD, CS-CA, CS-FI, CS-LS | Aligns Epic 1 P0/P1 |
| T1 Growth | CS-CC, CS-PR, CS-BU, CS-ST, CS-ENP, CS-IV, CS-PP, CS-RL, CS-PG, CS-ED | Decision-heavy |
| T2 Sensitive | CS-MA, CS-DT, CS-CH, CS-PA, CS-HE | Ethics-gated |
| T3 Adjacent | CS-EN, CS-TR, CS-LE, CS-RT | After core healthy |

---

## 8. Anti-patterns

| Forbidden | Why |
|-----------|-----|
| Scenario = Five Elements folder | Academic, not customer intent |
| Scenario invents Narrative sections | Breaks Pack 05 freeze |
| Scenario bypasses Commercial Knowledge | Breaks advisory SSOT |
| Scenario writes Rule thresholds | Wrong layer |

---

## 9. Stop line

Official scenario taxonomy defined.  
No knowledge records. No retrieval implementation.

---

END
