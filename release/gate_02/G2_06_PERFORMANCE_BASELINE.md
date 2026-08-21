# G2-06 — Performance baseline

Observed on 2026-08-21, local TestClient + Playwright PDF, Windows. **Do not optimize from this gate.** Values are a release baseline only.

Cold first Analyze is slower (engine/rule load). Later cases use a warm process.

## Analyze (`POST /api/v1/analyze`)

| Case | Seconds |
|------|---------|
| Nguyễn Tiến Sơn (first / cold) | 1.599 |
| Lương Ngọc Huỳnh | 0.470 |
| Đặng Thị Dung | 0.422 |
| Đoàn Quang Hưng | 0.418 |
| Vũ Thị Thanh Tuyền | 0.531 |
| Cao Xuân Trường | 0.437 |
| Lưu Hoàng Sơn | 0.434 |
| Phạm Thị Huyền | 0.527 |
| Lương Văn Mạnh | 0.659 |
| Ngô Đắc Dũng | 1.337 |

Warm typical Analyze: **0.4–0.7 s**. Report model build: **≤ 0.01 s**.

## Official export (primary four)

| Case | PDF s | DOCX s | PDF bytes | DOCX bytes |
|------|-------|--------|-----------|------------|
| Sơn | 3.543 | 0.441 | 173284 | 39526 |
| Tuyền | 2.393 | 0.184 | 172162 | 39519 |
| Dũng | 3.101 | 0.177 | 174719 | 39435 |
| Trường | 2.319 | 0.168 | 169723 | 39334 |

PDF generation is Playwright Chromium (~2.3–3.5 s). DOCX is sub-second after the first run.

## Result / Full Report render

Portal Result boot in vitest (four cases + gates): **~1.5 s** for the file (includes React render, not production bundle). Full Report HTML `render_html` is included in the ~0.01 s report-build window above plus HTML write.

## Not measured as blocking

Live network latency, cold Chromium outside TestClient, and production reverse-proxy time are outside this baseline. No release-blocking slowness was observed.
