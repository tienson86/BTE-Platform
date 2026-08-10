# Discrepancy Report

Only cases with runtime executed and mismatch against expert_expected (or boundary soft mismatch).
Expected was not overwritten. Engines were not patched to fit Expected.

## CASE-0001 — DISCREPANCY

- **First divergence:** strength
- **Pillars:** PASS (Bính Dần / Tân Sửu / Canh Ngọ / Mậu Dần)
- **expert_expected.strength:** Thân trung bình / thiên nhược
- **actual:** `strength_level=strong`, `reasoning=Thân vượng`, `strength_score=0.87`
- **Classification:** ENGINE (Strength polarity opposite expert)
- **Downstream:** Pattern/Interpretation/Report still execute; not treated as root cause.

## CASE-0002 — DISCREPANCY

- **First divergence:** strength
- **Pillars:** PASS
- **expert_expected.strength:** Thân rất vượng
- **actual:** `strong` / `Thân vượng` / `0.89`
- **Classification:** CONTRACT / ENGINE taxonomy (no `very_strong` band)
- **Note:** Directionally strong, but cannot claim exact PASS vs “rất vượng”.

## CASE-0003 — BOUNDARY

- **First divergence:** strength
- **Pillars:** PASS
- **expert_expected.strength:** Thân hơi nhược
- **actual:** `strong` / `Thân vượng` / `0.66` (barely over strong threshold 0.65)
- **Follow actual:** Tòng Nhi detected
- **Classification:** BOUNDARY — do not force engine toward expert soft label

## CASE-0005 — DISCREPANCY

- **First divergence:** strength
- **Pillars:** PASS
- **Gender:** `None` / unspecified preserved (schema allows)
- **expert_expected.strength:** Thân trung bình thiên vượng
- **actual:** `strong` / `Thân vượng` / `0.66`
- **Classification:** ENGINE taxonomy + threshold edge (near-band to balanced preference)

## CASE-0006 — DISCREPANCY

- **First divergence:** calendar_bazi
- **Pillars:**
  - expected month: Đinh Tỵ
  - actual month: Mậu Ngọ
  - year/day/hour match
- **Birth input used:** 1988-06-07 20:45 Asia/Ho_Chi_Minh, female
- **Strength (secondary):** expert thiên nhược vs actual balanced / Trung hòa 0.50 — also taxonomy gap, but not first divergence
- **Classification:** ENGINE / DATA (Calendar→BaZi month stem vs expert-confirmed pillar)

## Non-discrepancy notes (not PASS claims for content)

- CASE-0004 / CASE-0007: strength PASS at Thân vượng band; Interpretation/Report only EXECUTED.
- Follow EXECUTED_NEGATIVE means detector ran and did not emit a Tòng label (tong_cach fell back to main pattern text).
