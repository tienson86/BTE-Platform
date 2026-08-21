# G2-04 — Export error states

Customer-facing messages only. No stack traces in HTTP JSON. No silent empty file.

| Situation | HTTP / UI | Message | File? |
|-----------|-----------|---------|-------|
| Empty ResultStore / missing `data` | 422 `export_missing_result` · export bar copy | `Chưa có kết quả phân tích. Vui lòng nhập thông tin ngày giờ sinh để bắt đầu.` | No |
| Missing `analysis_id` | 422 `export_missing_analysis` | Same empty-result copy | No |
| Unversioned History / old contract | 409 `export_contract_mismatch` | `Kết quả này được tạo bởi phiên bản dữ liệu cũ. Vui lòng phân tích lại để cập nhật kết quả.` | No |
| `@1.5` but empty Dụng/Hỷ display | 409 `export_contract_mismatch` | `Kết quả phân tích chưa đủ hợp đồng hiển thị. Vui lòng phân tích lại.` | No |
| History URL id ≠ payload `analysis_id` | 409 `export_history_mismatch` | `Kết quả lịch sử không khớp với mã phân tích đang chọn. Vui lòng mở lại kết quả đã lưu.` | No |
| Playwright / python-docx / IO failure | 500 `export_renderer_failed` | `Không tạo được tệp xuất. Vui lòng thử lại.` Exception logged server-side | Temp cleaned |
| Empty output file | 500 `export_empty_file` | Same renderer copy | Temp cleaned |
| Missing temp after send | Background `cleanup_export_file` | — | Unlink best-effort |

Portal `/result` already gates contract mismatch **before** the export bar (G2-01R / G2-02). Official PDF/DOCX still re-check the contract so `/reports` cannot download a stale official file.

Renderer failures never stream a 0-byte PDF/DOCX. Temp names include analysis slug + UUID under `%TEMP%/bte_customer_export/` and are deleted after `FileResponse`.
