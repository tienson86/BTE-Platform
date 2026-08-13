# ISSUE_TRIAGE

| Field | Value |
|-------|-------|
| Program | RC3 Internal Beta |
| Rule | Discovery issues are classified, not silently fixed |

Do not modify engines, Knowledge, CLL, or Golden Dataset inside this program.

---

## Intake

Every form line that is a defect becomes one row:

| Column | Values |
|--------|--------|
| Beta ID | `BETA-00nn` |
| Case | CASE_0001–0010 |
| Persona | P01–P10 |
| Quote / symptom | Participant words |
| Severity | S0 blocker · S1 high · S2 medium · S3 low |
| Category | Identity · Career · Executive · Composer · Knowledge · Reasoning · Context · Regression · Commercial |
| Disposition | HOLD (RC3) · LATER (post-RC3 epic) · WONTFIX · WAIVE |

---

## Severity for discovery

| Level | Meaning |
|-------|---------|
| S0 | Would refuse to pay; unsafe; ethics; Golden regression risk |
| S1 | Trust break; wrong-person advice; child given adult Career |
| S2 | Generic feel; thin value; missing depth they would still buy around |
| S3 | Polish, wish-list |

S0/S1 on a bound Golden (CASE_0001) → stop-the-line for any later engineering proposal.

---

## Register (empty at program create)

| Beta ID | Case | Persona | Severity | Category | Disposition | Note |
|---------|------|---------|----------|----------|-------------|------|
| BETA-0001 | RC3-P04 | P04 | S1 | Context | LATER | Adult pass_through; conservation is child-only |
| BETA-0002 | RC3-P04 | P04 | S1 | Language | LATER | “Bạn mạnh hơn” + trách nhiệm close |
| BETA-0003 | RC3-P04 | P04 | S1 | Language | LATER | Output/speed residue on BALANCE_DIRECTION |
| BETA-0004 | RC3-P04 | P04 | S2 | Language | LATER | Empty “khung lá số” / kênh đã công bố |
| BETA-0005 | RC3-P04 | P04 | S2 | Product | LATER | No stop-list |
| BETA-0006 | RC3-P04 | P04 | S2 | Reasoning | HOLD | body:balanced vs Nhược / 0.50 — no engine change |
| BETA-0007 | RC3-P04 | P04 | S3 | Knowledge | WONTFIX | Split band vs pattern — not this program |
| BETA-0008 | RC3-P04 | P04 | S3 | Language | LATER | Duplicate avoid |

---

## Routing after RC3 close

| Disposition | Next |
|-------------|------|
| HOLD | Blocks RC3 success until waived or later epic |
| LATER | Backlog for Commercial V1 / V1.1 |
| WONTFIX | Out of scope (e.g. luck forecast demand) with note |
| WAIVE | Product written waiver + expiry |

---

END
