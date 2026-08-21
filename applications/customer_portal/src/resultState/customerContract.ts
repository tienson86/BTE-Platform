/**
 * Frozen customer Useful God contract for Portal binding.
 * Presentation / routing only — does not recompute engines.
 */

import type { AnalysisDataDto } from "../models";

export const CUSTOMER_USEFUL_GOD_CONTRACT = "analysis_result.UsefulGodView@1.5";
export const GATE_CORE_FREEZE = "G1";
export const MONTH_PILLAR_STANDARD = "BTE-MONTH-PILLAR-LUNAR-V1.0";

export const EMPTY_RESULT_MESSAGE =
  "Chưa có kết quả phân tích. Vui lòng nhập thông tin ngày giờ sinh để bắt đầu.";

export const CONTRACT_MISMATCH_MESSAGE =
  "Kết quả này được tạo bởi phiên bản dữ liệu cũ. Vui lòng phân tích lại để cập nhật kết quả.";

export const CONTRACT_INCOMPLETE_MESSAGE =
  "Kết quả phân tích chưa đủ hợp đồng hiển thị. Vui lòng phân tích lại.";

export const MISSING_HISTORY_MESSAGE = "Không tìm thấy hồ sơ.";

export const CORRUPT_HISTORY_MESSAGE = "Không tải được kết quả đã lưu.";

export type CustomerContractStatus = "ok" | "mismatch" | "unversioned" | "incomplete";

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function text(value: unknown): string {
  return typeof value === "string" ? value.trim() : "";
}

/**
 * Published customer contract string, if any.
 */
export function readCustomerContract(
  data: AnalysisDataDto | null | undefined,
): string | null {
  if (!data || typeof data !== "object") return null;
  const source = asRecord(data.useful_god_source);
  const meta = asRecord(data.result_meta);
  const contract = text(source.contract) || text(meta.customer_contract);
  return contract || null;
}

/**
 * Classify stored/API payload against UsefulGodView@1.5.
 */
export function customerContractStatus(
  data: AnalysisDataDto | null | undefined,
): CustomerContractStatus {
  if (!data || typeof data !== "object") return "incomplete";
  const contract = readCustomerContract(data);
  if (!contract) {
    if (data.useful_god || data.pattern || data.calendar || data.bazi) {
      return "unversioned";
    }
    return "incomplete";
  }
  if (contract !== CUSTOMER_USEFUL_GOD_CONTRACT) return "mismatch";
  const useful = asRecord(data.useful_god);
  if (useful.overall_incomplete) return "ok";
  const hasDisplay = Boolean(text(useful.useful_display) || text(useful.favorable_display));
  if (!hasDisplay) return "incomplete";
  return "ok";
}

export function customerContractMessage(status: CustomerContractStatus): string {
  if (status === "ok") return "";
  if (status === "incomplete") return CONTRACT_INCOMPLETE_MESSAGE;
  return CONTRACT_MISMATCH_MESSAGE;
}

export function isCompatibleCustomerContract(
  data: AnalysisDataDto | null | undefined,
): boolean {
  return customerContractStatus(data) === "ok";
}
