/**
 * Bind canonical analysis.can_xuong for header, S10, and workspace.
 * Presentation copy only — no weight calculation.
 */

import type { AnalysisDataDto } from "../models";

export const CAN_XUONG_DETAIL_HREF = "#sec-can-xuong";

export const CAN_XUONG_EMPTY_COPY = "Chưa có dữ liệu Cân Xương";

export type CanXuongView = {
  readonly available: boolean;
  readonly displayWeight: string;
  readonly classification: string;
  readonly rating: string;
  readonly summary: string;
  readonly interpretation: string;
  readonly source: string;
  readonly version: string;
  readonly detailHref: string;
};

const EMPTY: CanXuongView = {
  available: false,
  displayWeight: "",
  classification: "",
  rating: "",
  summary: "",
  interpretation: "",
  source: "",
  version: "",
  detailHref: CAN_XUONG_DETAIL_HREF,
};

function text(value: unknown): string {
  if (value == null) return "";
  return String(value).trim();
}

function asRecord(value: unknown): Record<string, unknown> {
  if (!value || typeof value !== "object" || Array.isArray(value)) return {};
  return value as Record<string, unknown>;
}

function firstText(...values: unknown[]): string {
  for (const value of values) {
    const next = text(value);
    if (next) return next;
  }
  return "";
}

/**
 * Prefer analysis.can_xuong; fall back to identity.bone_weight for old payloads.
 */
export function adaptCanXuong(data: AnalysisDataDto | null | undefined): CanXuongView {
  const payload = asRecord(data);
  const canonical = asRecord(payload.can_xuong);
  const identity = asRecord(asRecord(payload.identity).bone_weight);
  const displayWeight = firstText(
    canonical.display_weight,
    canonical.weight,
    canonical.total,
    identity.weight,
  );
  if (!displayWeight) return EMPTY;
  return {
    available: true,
    displayWeight,
    classification: firstText(canonical.classification, identity.classification),
    rating: firstText(canonical.rating, identity.rating),
    summary: firstText(canonical.summary, identity.summary),
    interpretation: firstText(canonical.interpretation, canonical.poem, identity.summary),
    source: firstText(canonical.source, "can_xuong"),
    version: firstText(canonical.version),
    detailHref: CAN_XUONG_DETAIL_HREF,
  };
}
