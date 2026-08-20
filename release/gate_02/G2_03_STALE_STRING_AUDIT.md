# G2-03 — Stale string audit

**Rule:** do not delete historical docs. Only **ACTIVE CUSTOMER** is release-blocking.  
**Date:** 2026-08-20  
**Active customer result:** no release-blocking stale strings on live Analyze of the ten control cases.

## Classification key

| Class | Meaning |
|-------|---------|
| ACTIVE CUSTOMER | Live Analyze → `/result` interpretation, Full Report, Report model |
| TEST | Automated tests / fixtures used by tests |
| HISTORICAL REPORT | Saved captures, pilot snapshots, Gate-1 UI dumps |
| AUDIT DOC | Release / Gate markdown |
| BACKLOG | Known V1.1 work |
| DEAD CODE | Unreachable or explicit legacy |

## Gate-1 obsolete conclusions

| Phrase / conclusion | Where found | Class | Release block? |
|---------------------|-------------|-------|----------------|
| Dũng Overall `Thổ · Mậu · Thiên Ấn` | Not in live Dũng `narrative_result`. Tests assert absence. | TEST (negative assert) | No |
| `Chuyên cách ưu tiên Ấn` | `engines/useful_god_engine/reasoning.py` internal `spc_004` label; G2-02/G2-03 tests forbid customer copy when override is false | Internal mapping + TEST | No — does not appear in live Dũng/Mạnh narrative |
| Tuyền `Tòng Tài` / `Nhật chủ cực nhược theo Tài` | Live Tuyền: absent. Present in `applications/customer_portal/src/features/portal/fixtures/launch_08/case_007_response.json` and `knowledge/pilot/replay/snapshots/CASE-0007.json` | HISTORICAL REPORT / TEST fixture | No |
| Nhâm as Tuyền Overall | Live Tuyền Overall is `Mộc · Ất · Chính Quan` | — | No |
| Sơn CASE-0001 old Thực Thần winner | Live Sơn Overall is `Hỏa · Đinh · Chính Quan` | — | No |
| Old Hỷ = exact Dụng | HK-R1H customer Hỷ is insufficient or remainder-after-omit; live Dũng/Tuyền/Mạnh/Huyền do not reinsert Dụng as Hỷ | CLOSED | No |
| `Than nhược` CSV leak | Sanitized in narrative `normalize_text` and commercial presentation → `Thân nhược`. CSV unchanged | Presentation fix | No |
| Commercial `mỏng lực` on strong charts | Caused by treating 0–1 Strength as 0–100. Closed in `signal_projection`. Strong charts now `được nâng đỡ` | CLOSED (was ACTIVE CUSTOMER) | No |
| Launch-08 / G1_09 UI captures | Frozen JSON with old Tòng Tài / mỏng lực on historical cases | HISTORICAL REPORT | No |
| `?preview=1` fixture / mock | Explicit preview only | DEAD for production `/result` | No |
| Legacy `presenters/narrative.js` | `?legacy=1` | LEGACY | No |

## Placeholders / internals (spec 27)

Live ten-case blobs: no `{{...}}`, `${...}`, `None`, `null`, `undefined`, or internal rule IDs (`str_`, `pat_`, `spc_`, …).

Disclaimer `Không chẩn đoán` is **kept** (health framing). Operational “cửa lưu thông bắt buộc” is not treated as analytical certainty.

## Active-customer close-out

After presentation-only fixes, `python release/gate_02/_g2_03_narrative_probe.py` reports **fail: []** on all ten G1-FINAL cases.
